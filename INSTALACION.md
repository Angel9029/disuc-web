# 🔧 Guía de Instalación

## Requisitos previos

- **Python 3.8 o superior** instalado
- **pip** (administrador de paquetes de Python)
- Un **navegador web** moderno (Chrome, Firefox, Safari, Edge)

---

## Verificar que Python está instalado

### En Linux/Mac:
```bash
python3 --version
pip3 --version
```

### En Windows:
```bash
python --version
pip --version
```

Si no está instalado, descárgalo desde: https://www.python.org/downloads/

---

## 1️⃣ Descargar o clonar el proyecto

```bash
# Opción A: Si tienes git
git clone <url-del-repositorio>
cd DISUC_WEB

# Opción B: Descargar manualmente y extraer
# Luego entra a la carpeta en terminal
cd /ruta/a/DISUC_WEB
```

---

## 2️⃣ Crear entorno virtual

### Linux/Mac:
```bash
# Crear entorno
python3 -m venv venv

# Activar
source venv/bin/activate
```

### Windows (PowerShell):
```bash
# Crear entorno
python -m venv venv

# Activar
venv\Scripts\Activate.ps1
```

### Windows (CMD):
```bash
# Crear entorno
python -m venv venv

# Activar
venv\Scripts\activate
```

**Resultado esperado:** Verás `(venv)` al inicio de tu línea de comandos

```
(venv) usuario@pc ~/DISUC_WEB $
```

---

## 3️⃣ Instalar dependencias

Con el entorno virtual **activado**:

### Linux/Mac:
```bash
pip3 install -r requirements.txt
```

### Windows:
```bash
pip install -r requirements.txt
```

**Deberías ver:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 ...
```

---

## 4️⃣ Ejecutar la aplicación

Con el entorno virtual **activado**:

### Linux/Mac:
```bash
uvicorn app.main:app --reload
```

### Windows:
```bash
uvicorn app.main:app --reload
```

**Deberías ver algo como:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
🔄 Inicializando base de datos...
📂 Cargando archivos CSV automáticamente...
  - categorias.csv no encontrado (se puede cargar luego)
  [...]
✅ Inicialización completada
```

---

## 5️⃣ Abrir en el navegador

Abre tu navegador y ve a:

```
http://localhost:8000
```

Deberías ver la interfaz web con 8 secciones de carga.

---

## 🎯 Próximos pasos

### Opción A: Cargar archivos CSVs que ya tienes

1. Copia tus archivos CSV a la carpeta `/data/`:
   - `clientes.csv`
   - `categorias.csv`
   - `productos.csv`
   - etc.

2. Reinicia el servidor (presiona `Ctrl+C` y ejecuta `uvicorn` de nuevo)

3. Los CSVs se cargarán automáticamente

### Opción B: Usar los archivos de ejemplo

1. Los ejemplos ya están en `/data/`:
   - `ejemplo_clientes.csv`
   - `ejemplo_categorias.csv`
   - `ejemplo_productos.csv`
   - `ejemplo_ventas.csv`

2. Copia el contenido a nombres sin `ejemplo_`:
   ```bash
   # Linux/Mac
   cp data/ejemplo_clientes.csv data/clientes.csv
   cp data/ejemplo_categorias.csv data/categorias.csv
   cp data/ejemplo_productos.csv data/productos.csv
   cp data/ejemplo_ventas.csv data/ventas.csv
   
   # Windows (PowerShell)
   Copy-Item "data/ejemplo_clientes.csv" "data/clientes.csv"
   Copy-Item "data/ejemplo_categorias.csv" "data/categorias.csv"
   Copy-Item "data/ejemplo_productos.csv" "data/productos.csv"
   Copy-Item "data/ejemplo_ventas.csv" "data/ventas.csv"
   ```

3. Reinicia el servidor

### Opción C: Cargar manualmente en la web

1. En http://localhost:8000
2. Selecciona un archivo CSV en cada sección
3. Haz clic en "Cargar"
4. El sistema procesará el archivo

---

## 🛑 Detener la aplicación

En la terminal donde corre el servidor:

```bash
Ctrl+C
```

---

## ⚠️ Problemas comunes

### Error: "python: command not found"
```bash
# En Mac/Linux, intenta:
python3 --version

# Si sigue sin funcionar, instala Python desde:
# https://www.python.org/downloads/
```

### Error: "No module named 'fastapi'"
```bash
# Asegúrate de que el entorno virtual esté ACTIVADO
# Deberías ver (venv) al inicio de tu línea de comandos

# Si no está activado:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Luego instala de nuevo:
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# El puerto 8000 está en uso
# Usa un puerto diferente:
uvicorn app.main:app --reload --port 8001
# Luego accede a: http://localhost:8001
```

### Error: "Permission denied"
```bash
# En Mac/Linux, intenta:
chmod +x venv/bin/activate
```

---

## 🧪 Pruebas

Ejecutar el script de prueba:

### Linux/Mac:
```bash
# Primero asegúrate de que el servidor está corriendo
# (en otra terminal)

# Luego:
python3 test_upload.py
```

### Windows:
```bash
python test_upload.py
```

---

## 📂 Estructura de archivos esperada

Después de la instalación deberías tener:

```
DISUC_WEB/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── services.py
│   └── routers/
│       ├── __init__.py
│       └── csv_upload.py
├── data/
│   ├── ejemplo_*.csv
│   └── disuc.db (se crea al ejecutar)
├── templates/
│   └── index.html
├── static/
│   ├── script.js
│   └── style.css
├── venv/
│   └── [archivos de entorno virtual]
├── requirements.txt
├── INICIO.md
├── API.md
├── README.md
├── RESUMEN.md
├── INSTALACION.md (este archivo)
└── test_upload.py
```

---

## ✅ Checklist de instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado (`venv/`)
- [ ] Entorno virtual activado (`(venv)` visible en terminal)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Servidor corriendo (`uvicorn app.main:app --reload`)
- [ ] Acceso a http://localhost:8000 en navegador
- [ ] Interfaz web visible con 8 secciones

---

## 🚀 ¡Listo!

Si todo funcionó correctamente, tienes la aplicación DISUC CSV Manager completamente instalada y operativa.

Para documentación adicional:
- 📖 `README.md` - Documentación completa
- ⚡ `INICIO.md` - Guía rápida
- 🌐 `API.md` - Endpoints REST
- 📋 `RESUMEN.md` - Resumen del proyecto

---

## 💬 Ayuda adicional

### Si necesitas verificar que todo funciona:

```bash
# 1. Asegúrate de que el servidor esté corriendo
# 2. En otra terminal, ejecuta:
curl http://localhost:8000/api/health

# Deberías ver:
# {"status":"ok"}
```

### Para cargar datos de prueba:

```bash
# Ejecuta este script:
python test_upload.py

# Verás un resumen de lo que se cargó
```

---

**¡Bienvenido al sistema DISUC CSV Manager!** 🎉
