const productoInput = document.getElementById('producto-input');
const autocompleteList = document.getElementById('autocomplete-list');
const fechaInput = document.getElementById('fecha-input');
const predictForm = document.getElementById('predict-form');
const btnPredict = document.getElementById('btn-predict');
const errorMsg = document.getElementById('error-msg');
const resultCard = document.getElementById('result-card');

const API_BASE = '';
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

async function loadCounts() {
    try {
        const res = await fetch(`${API_BASE}/api/upload/status`);
        const data = await res.json();
        document.getElementById('clientes-count').textContent = `${data.clientes} clientes`;
        document.getElementById('productos-count').textContent = `${data.productos} productos`;
        document.getElementById('ventas-count').textContent = `${data.ventas} ventas`;
        document.getElementById('pedidos-count').textContent = `${data.pedidos} pedidos`;
    } catch (_) {}
}

document.querySelectorAll('.upload-btn input[type="file"]').forEach(input => {
    input.addEventListener('change', async function() {
        const file = this.files[0];
        if (!file) return;
        const endpoint = this.dataset.endpoint;
        const label = this.closest('.upload-btn');
        const fd = new FormData();
        fd.append('file', file);
        label.classList.add('uploaded');
        label.querySelector('span').textContent = 'Subiendo...';
        try {
            const res = await fetch(`${API_BASE}/api/upload/${endpoint}`, { method: 'POST', body: fd });
            const data = await res.json();
            if (data.mensaje) {
                label.querySelector('span').textContent = '\u2713 ' + (data.cargados || 'OK');
                loadCounts();
            } else {
                label.querySelector('span').textContent = 'Error';
                label.classList.remove('uploaded');
            }
        } catch (_) {
            label.querySelector('span').textContent = 'Error';
            label.classList.remove('uploaded');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    loadCounts();
});
