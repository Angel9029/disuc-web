const API_BASE = '';
const isPredictionPage = !!document.getElementById('predict-form');

if (isPredictionPage) {
const productoInput = document.getElementById('producto-input');
const autocompleteList = document.getElementById('autocomplete-list');
const fechaInput = document.getElementById('fecha-input');
const predictForm = document.getElementById('predict-form');
const btnPredict = document.getElementById('btn-predict');
const errorMsg = document.getElementById('error-msg');
const resultCard = document.getElementById('result-card');

let selectedProduct = null;
let searchTimeout = null;

async function searchProductos(query) {
    if (query.length < 1) {
        autocompleteList.classList.remove('active');
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/productos/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        renderAutocomplete(data, query);
    } catch (_) {
        autocompleteList.classList.remove('active');
    }
}

function renderAutocomplete(items, query) {
    autocompleteList.innerHTML = '';
    if (!items.length) {
        autocompleteList.innerHTML = '<li style="color:var(--color-text-secondary);cursor:default;">Sin resultados</li>';
        autocompleteList.classList.add('active');
        return;
    }
    items.forEach((item, idx) => {
        const li = document.createElement('li');
        const idx2 = item.nombre.toLowerCase().indexOf(query.toLowerCase());
        if (idx2 >= 0) {
            const before = item.nombre.slice(0, idx2);
            const match = item.nombre.slice(idx2, idx2 + query.length);
            const after = item.nombre.slice(idx2 + query.length);
            li.innerHTML = `${before}<span class="highlight">${match}</span>${after}`;
        } else {
            li.textContent = item.nombre;
        }
        li.dataset.nombre = item.nombre;
        li.addEventListener('click', () => selectProduct(item.nombre));
        autocompleteList.appendChild(li);
    });
    autocompleteList.classList.add('active');
}

function selectProduct(nombre) {
    productoInput.value = nombre;
    selectedProduct = nombre;
    autocompleteList.classList.remove('active');
    btnPredict.disabled = false;
}

productoInput.addEventListener('input', function() {
    selectedProduct = null;
    btnPredict.disabled = true;
    clearTimeout(searchTimeout);
    const val = this.value.trim();
    if (val.length >= 1) {
        searchTimeout = setTimeout(() => searchProductos(val), 200);
    } else {
        autocompleteList.classList.remove('active');
    }
});

productoInput.addEventListener('blur', function() {
    setTimeout(() => autocompleteList.classList.remove('active'), 150);
});

productoInput.addEventListener('focus', function() {
    if (this.value.trim().length >= 1 && !selectedProduct) {
        searchProductos(this.value.trim());
    }
});

productoInput.addEventListener('keydown', function(e) {
    const items = autocompleteList.querySelectorAll('li');
    if (!items.length) return;
    let activeIdx = Array.from(items).findIndex(li => li.classList.contains('active'));
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIdx = Math.min(activeIdx + 1, items.length - 1);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIdx = Math.max(activeIdx - 1, 0);
    } else if (e.key === 'Enter') {
        e.preventDefault();
        if (activeIdx >= 0) {
            selectProduct(items[activeIdx].dataset.nombre);
        }
        return;
    } else if (e.key === 'Escape') {
        autocompleteList.classList.remove('active');
        return;
    } else {
        return;
    }
    items.forEach((li, i) => li.classList.toggle('active', i === activeIdx));
    if (activeIdx >= 0) {
        items[activeIdx].scrollIntoView({ block: 'nearest' });
    }
});

fechaInput.addEventListener('input', function() {
    const val = this.value;
    if (val && !val.endsWith('-01')) {
        const parts = val.split('-');
        if (parts.length === 3) {
            this.value = parts[0] + '-' + parts[1] + '-01';
        }
    }
});

predictForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    errorMsg.classList.remove('visible');
    resultCard.classList.remove('visible');

    const producto = selectedProduct || productoInput.value.trim();
    const fecha = fechaInput.value;

    if (!producto) { showError('Busca y selecciona un producto'); return; }
    if (!fecha) { showError('Selecciona una fecha'); return; }
    if (!fecha.endsWith('-01')) { showError('La fecha debe ser el primer dia del mes (YYYY-MM-01)'); return; }

    const selectedDate = new Date(fecha + 'T12:00:00');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const nextMonth = new Date(today.getFullYear(), today.getMonth() + 1, 1);
    if (selectedDate < nextMonth) {
        showError('La fecha debe ser un mes futuro (a partir del proximo mes)');
        return;
    }

    const dataOk = await checkData();
    if (!dataOk) {
        showError('No hay datos cargados. Sube archivos CSV desde la pagina principal.');
        return;
    }

    btnPredict.classList.add('loading');
    btnPredict.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/pronosticar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ producto, fecha })
        });
        const data = await res.json();

        if (!res.ok) {
            showError(data.detail || 'Error en la prediccion');
            return;
        }

        document.getElementById('result-producto').textContent = data.producto;
        document.getElementById('result-fecha').textContent = data.fecha;
        document.getElementById('result-pronostico').textContent = data.pronostico.toFixed(2);
        document.getElementById('result-modelo').textContent = data.modelo;
        document.getElementById('result-mape').textContent = data.mape.toFixed(2) + '%';
        resultCard.classList.add('visible');

    } catch (err) {
        showError('Error de conexion con el servidor');
    } finally {
        btnPredict.classList.remove('loading');
        btnPredict.disabled = false;
    }
});

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.add('visible');
}
}

async function loadCounts() {
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        document.getElementById('clientes-count').textContent = `${data.clientes} clientes`;
        document.getElementById('productos-count').textContent = `${data.productos} productos`;
        if (document.getElementById('lotes-count')) {
            document.getElementById('lotes-count').textContent = `${data.lotes} lotes`;
        }
        document.getElementById('ventas-count').textContent = `${data.ventas} ventas`;
        document.getElementById('pedidos-count').textContent = `${data.pedidos} pedidos`;
    } catch (_) {}
}

const REQUIRED_TABLES = ['clientes', 'productos', 'lotes', 'pedidos', 'ventas', 'dim_tiempo'];
const TABLE_LABELS = {
    clientes: 'clientes', productos: 'productos', lotes: 'lotes',
    pedidos: 'pedidos', ventas: 'ventas', dim_tiempo: 'dim. tiempo',
};

const LOADER_MAP = {
    'clientes': 'clientes', 'categorias': 'categorias',
    'productos': 'productos', 'ventas': 'ventas',
    'pedidos': 'pedidos', 'lotes': 'lotes',
    'dim_tiempo': 'dim_tiempo', 'mejores_modelos': 'mejores_modelos',
    'dimtiempo': 'dim_tiempo', 'mejoresmodelos': 'mejores_modelos',
};

function detectEndpoint(filename) {
    const name = filename.replace(/\.csv$/i, '').toLowerCase();
    return LOADER_MAP[name] || null;
}

function addUploadItem(container, name, status, cls) {
    const div = document.createElement('div');
    div.className = 'upload-item';
    div.innerHTML = `<span class="upload-item-name">${name}</span><span class="upload-item-status ${cls}">${status}</span>`;
    container.appendChild(div);
    return div;
}

function updateUploadItem(el, status, cls) {
    el.querySelector('.upload-item-status').textContent = status;
    el.querySelector('.upload-item-status').className = 'upload-item-status ' + cls;
}

async function uploadSingleFile(file, progressContainer, summaryContainer) {
    const name = file.name;
    const isZip = name.toLowerCase().endsWith('.zip');
    const fd = new FormData();
    fd.append('file', file);
    const item = addUploadItem(progressContainer, name, 'Subiendo...', 'loading');
    try {
        let url;
        if (isZip) {
            url = `${API_BASE}/api/upload/zip`;
        } else {
            const ep = detectEndpoint(name);
            if (!ep) {
                updateUploadItem(item, 'Ignorado', 'err');
                return;
            }
            url = `${API_BASE}/api/upload/${ep}`;
        }
        const res = await fetch(url, { method: 'POST', body: fd });
        const data = await res.json();
        if (res.ok) {
            if (isZip && data.resultados) {
                const parts = Object.entries(data.resultados).map(([k, v]) => `${k}: ${v}`);
                updateUploadItem(item, '\u2713 ' + parts.join(', '), 'ok');
            } else {
                updateUploadItem(item, '\u2713 OK', 'ok');
            }
        } else {
            updateUploadItem(item, 'Error: ' + (data.detail || 'desconocido'), 'err');
        }
    } catch (_) {
        updateUploadItem(item, 'Error de conexión', 'err');
    }
    loadCounts();
    showDataBanner();
}

async function handleFiles(files) {
    const container = document.getElementById('upload-progress');
    const summary = document.getElementById('upload-summary');
    container.innerHTML = '';
    summary.innerHTML = '';
    for (const file of files) {
        await uploadSingleFile(file, container, summary);
    }
}

function setupDropZone() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    if (!dropZone || !fileInput) return;

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function () {
        if (this.files.length) {
            handleFiles(this.files);
            this.value = '';
        }
    });

    ['dragenter', 'dragover'].forEach(ev => {
        dropZone.addEventListener(ev, e => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(ev => {
        dropZone.addEventListener(ev, e => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length) handleFiles(files);
    });
}

async function checkData() {
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        return data.productos > 0 && data.lotes > 0 && data.clientes > 0;
    } catch (_) {
        return false;
    }
}

async function showDataBanner() {
    const banner = document.getElementById('data-banner');
    const text = document.getElementById('data-banner-text');
    if (!banner || !text) return;
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        banner.className = 'data-banner';
        if (data.completo) {
            const parts = REQUIRED_TABLES.filter(t => data[t] > 0).map(t => `${data[t]} ${TABLE_LABELS[t]}`);
            text.textContent = `Datos completos: ${parts.join(', ')}`;
            banner.classList.add('data-banner-ok');
        } else if (data.faltantes && data.faltantes.length > 0) {
            const missing = data.faltantes.map(t => TABLE_LABELS[t]);
            const loadedParts = REQUIRED_TABLES.filter(t => data[t] > 0).map(t => `${data[t]} ${TABLE_LABELS[t]}`);
            const loadedText = loadedParts.length ? ` — Cargados: ${loadedParts.join(', ')}` : '';
            text.textContent = `Faltan: ${missing.join(', ')}.${loadedText}`;
            banner.classList.add('data-banner-warn');
        } else {
            text.textContent = 'No hay datos cargados. Arrastra archivos CSV o ZIP para comenzar.';
            banner.classList.add('data-banner-info');
        }
        banner.style.display = 'flex';
    } catch (_) { }
}

document.addEventListener('DOMContentLoaded', async () => {
    loadCounts();
    setupDropZone();
    showDataBanner();
    const hasData = await checkData();
    if (hasData) {
        document.querySelectorAll('.no-data-msg').forEach(el => el.remove());
    }
});
