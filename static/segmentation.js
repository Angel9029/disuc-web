const API_BASE = '';
const btnSegmentar = document.getElementById('btn-segmentar');
const btnDownload = document.getElementById('btn-download');
const errorMsg = document.getElementById('error-msg');
const segResult = document.getElementById('seg-result');
const searchInput = document.getElementById('search-input');
const segTbody = document.getElementById('seg-tbody');
const tableCount = document.getElementById('table-count');
const detailBody = document.getElementById('detail-body');

let segmentData = null;
let downloadToken = null;

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.add('visible');
}

function hideError() {
    errorMsg.classList.remove('visible');
}

function riesgoKey(riesgo) {
    if (riesgo === 'Riesgo Alto' || riesgo === 'Alto') return 'Riesgo Alto';
    if (riesgo === 'Riesgo Medio' || riesgo === 'Medio') return 'Riesgo Medio';
    if (riesgo === 'Riesgo Bajo' || riesgo === 'Bajo') return 'Riesgo Bajo';
    return riesgo;
}

function riesgoShort(riesgo) {
    if (riesgo === 'Riesgo Alto') return 'Alto';
    if (riesgo === 'Riesgo Medio') return 'Medio';
    if (riesgo === 'Riesgo Bajo') return 'Bajo';
    return riesgo;
}

async function checkData() {
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        return data.productos > 0 && data.lotes > 0;
    } catch (_) {
        return false;
    }
}

btnSegmentar.addEventListener('click', async function () {
    hideError();
    const hasData = await checkData();
    if (!hasData) {
        showError('No hay datos cargados. Sube archivos CSV desde la página principal.');
        return;
    }
    btnSegmentar.classList.add('loading');
    btnSegmentar.disabled = true;
    try {
        const res = await fetch(`${API_BASE}/segmentation/execute`, { method: 'POST' });
        const data = await res.json();
        if (!res.ok) {
            showError(data.detail || 'Error en la segmentacion');
            return;
        }
        segmentData = data;
        downloadToken = data.download_token;
        renderResults(data);
        btnDownload.disabled = false;
    } catch (err) {
        showError('Error de conexion con el servidor');
    } finally {
        btnSegmentar.classList.remove('loading');
        btnSegmentar.disabled = false;
    }
});

btnDownload.addEventListener('click', function () {
    if (downloadToken) {
        window.location.href = `${API_BASE}/segmentation/download/${downloadToken}`;
    }
});

function renderResults(data) {
    document.getElementById('ind-total').textContent = data.total_lotes;
    document.getElementById('ind-alto').textContent = data.resumen[riesgoKey('Riesgo Alto')] || 0;
    document.getElementById('ind-medio').textContent = data.resumen[riesgoKey('Riesgo Medio')] || 0;
    document.getElementById('ind-bajo').textContent = data.resumen[riesgoKey('Riesgo Bajo')] || 0;
    renderScatter(data.datos, data.centroides);
    renderHeatmap(data.centroides);
    renderTable(data.datos);
    segResult.style.display = 'block';
    segResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderScatter(datos, centroides) {
    const colors = { 'Riesgo Alto': '#dc2626', 'Riesgo Medio': '#d97706', 'Riesgo Bajo': '#059669' };
    const traces = [];
    const riesgos = ['Riesgo Alto', 'Riesgo Medio', 'Riesgo Bajo'];
    riesgos.forEach(riesgo => {
        const pts = datos.filter(d => d.Nivel_Riesgo === riesgo);
        if (!pts.length) return;
        traces.push({
            x: pts.map(d => d.Dias_Para_Vencer),
            y: pts.map(d => d.Rotacion),
            text: pts.map(d => `${d.Producto}<br>Lote: ${d.Lote_ID}<br>Valor: S/ ${d.Valor_Lote.toFixed(2)}<br>Dias: ${d.Dias_Para_Vencer}<br>Rotacion: ${d.Rotacion}`),
            hoverinfo: 'text',
            mode: 'markers',
            marker: {
                size: pts.map(d => Math.max(6, Math.min(30, d.Valor_Lote / 5000))),
                color: colors[riesgo],
                line: { color: '#fff', width: 1 },
                opacity: 0.85,
            },
            name: riesgoShort(riesgo),
            type: 'scatter',
        });
    });
    centroides.forEach(c => {
        traces.push({
            x: [c.Dias_Para_Vencer],
            y: [c.Rotacion],
            mode: 'markers',
            marker: {
                size: 16,
                color: colors[riesgoKey(c.riesgo)] || '#666',
                symbol: 'x',
                line: { color: '#1a1d23', width: 2 },
            },
            name: `Centroide ${riesgoShort(c.riesgo)}`,
            showlegend: false,
            hoverinfo: 'text',
            text: `Centroide ${c.riesgo}<br>Dias: ${c.Dias_Para_Vencer}<br>Rotacion: ${c.Rotacion}<br>Valor: S/ ${c.Valor_Lote.toFixed(2)}`,
        });
    });
    const layout = {
        margin: { l: 50, r: 20, t: 20, b: 50 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            title: { text: 'Días para vencer' },
            gridcolor: '#e8eaee',
            zeroline: false,
        },
        yaxis: {
            title: { text: 'Rotación' },
            gridcolor: '#e8eaee',
            zeroline: false,
        },
        legend: {
            orientation: 'h',
            y: 1.08,
            x: 0,
            font: { family: "'Sora', sans-serif", size: 12 },
        },
        font: { family: "'Sora', sans-serif" },
        hovermode: 'closest',
    };
    Plotly.newPlot('scatter-plot', traces, layout, {
        responsive: true,
        displayModeBar: false,
    });
}

function renderHeatmap(centroides) {
    const features = ['Dias_Para_Vencer', 'Valor_Lote', 'Rotacion'];
    const labels = ['Días', 'Valor', 'Rotación'];
    const table = document.getElementById('heatmap-table');
    const thead = table.querySelector('thead tr');
    const tbody = table.querySelector('tbody');
    thead.innerHTML = '<th>Riesgo</th>' + labels.map(l => `<th>${l}</th>`).join('');
    tbody.innerHTML = '';
    centroides.forEach(c => {
        const tr = document.createElement('tr');
        const riesgoClass = `cell-${riesgoShort(c.riesgo).toLowerCase()}`;
        tr.innerHTML = `<td class="cell-riesgo ${riesgoClass}">${riesgoShort(c.riesgo)}</td>`;
        features.forEach(f => {
            const val = c[f];
            const maxVal = Math.max(...centroides.map(c2 => Math.abs(c2[f])));
            const norm = maxVal > 0 ? val / maxVal : 0;
            const r = norm >= 0 ? Math.round(200 * (1 - Math.abs(norm))) : 255;
            const g = norm >= 0 ? 255 : Math.round(200 * (1 - Math.abs(norm)));
            const b = norm >= 0 ? Math.round(200 * (1 - Math.abs(norm))) : Math.round(200 * (1 - Math.abs(norm)));
            const bg = `rgba(${r},${g},${b},0.6)`;
            const formatted = f === 'Rotacion' ? val.toFixed(4) : 'S/ ' + val.toFixed(2);
            tr.innerHTML += `<td style="background:${bg};font-weight:600;">${formatted}</td>`;
        });
        tbody.appendChild(tr);
    });
}

function renderTable(datos) {
    segTbody.innerHTML = '';
    datos.forEach((d, idx) => {
        const tdClass = `td-risk-${riesgoShort(d.Nivel_Riesgo).toLowerCase()}`;
        const tr = document.createElement('tr');
        tr.dataset.idx = idx;
        const valorStr = 'S/ ' + d.Valor_Lote.toFixed(2);
        tr.innerHTML = `
            <td>${d.Producto}</td>
            <td>${d.Lote_ID}</td>
            <td>${d.Cluster_ID}</td>
            <td class="${tdClass}">${d.Nivel_Riesgo}</td>
            <td>${d.Dias_Para_Vencer}</td>
            <td>${d.Cantidad_Disponible}</td>
            <td>${d.Rotacion.toFixed(2)}</td>
            <td>${valorStr}</td>
        `;
        tr.addEventListener('click', () => showDetail(d, tr));
        segTbody.appendChild(tr);
    });
    updateTableCount(datos.length, datos.length);

    searchInput.addEventListener('input', function () {
        filterTable(this.value, datos);
    });
}

function filterTable(query, datos) {
    const q = query.toLowerCase().trim();
    const rows = segTbody.querySelectorAll('tr');
    let visible = 0;
    rows.forEach((tr, i) => {
        const d = datos[i];
        const match = !q ||
            d.Producto.toLowerCase().includes(q) ||
            String(d.Lote_ID).includes(q) ||
            String(d.Producto_ID).includes(q);
        tr.style.display = match ? '' : 'none';
        if (match) visible++;
    });
    updateTableCount(visible, datos.length);
}

function updateTableCount(visible, total) {
    tableCount.textContent = `Mostrando ${visible} de ${total} lotes`;
}

function showDetail(d, tr) {
    document.querySelectorAll('#seg-tbody tr').forEach(r => r.classList.remove('selected-row'));
    tr.classList.add('selected-row');
    const riesgoClass = `td-risk-${riesgoShort(d.Nivel_Riesgo).toLowerCase()}`;
    detailBody.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Producto</span>
            <span class="detail-value">${d.Producto}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Lote ID</span>
            <span class="detail-value">${d.Lote_ID}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Cluster</span>
            <span class="detail-value">${d.Cluster_ID}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Riesgo</span>
            <span class="detail-value"><span class="${riesgoClass}" style="padding:0.2rem 0.55rem;border-radius:100px;font-size:0.72rem;">${d.Nivel_Riesgo}</span></span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Stock Disponible</span>
            <span class="detail-value">${d.Cantidad_Disponible}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Rotación</span>
            <span class="detail-value">${d.Rotacion.toFixed(2)}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Valor del Lote</span>
            <span class="detail-value">S/ ${d.Valor_Lote.toFixed(2)}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Días para Vencer</span>
            <span class="detail-value">${d.Dias_Para_Vencer}</span>
        </div>
    `;
}

async function loadCounts() {
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        for (const [key, label] of Object.entries({
            clientes: 'clientes', productos: 'productos', lotes: 'lotes',
            ventas: 'ventas', pedidos: 'pedidos'
        })) {
            const el = document.getElementById(`${key}-count`);
            if (el) el.textContent = `${data[key]} ${label}`;
        }
    } catch (_) { }
}

async function toggleButtons() {
    const hasData = await checkData();
    btnSegmentar.disabled = !hasData;
}

document.addEventListener('DOMContentLoaded', async () => {
    loadCounts();
    await toggleButtons();
});
