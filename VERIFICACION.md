# ✅ Checklist de Verificación

## 📋 Antes de usar la aplicación

### Requisitos del sistema
- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] Navegador web actualizado
- [ ] Terminal/CMD disponible

### Instalación
- [ ] Carpeta `/DISUC_WEB` descargada
- [ ] `requirements.txt` presente
- [ ] `venv/` creado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas: `pip install -r requirements.txt`

### Archivo de configuración
- [ ] `app/` existe con archivos Python
- [ ] `app/main.py` presente
- [ ] `app/models.py` presente
- [ ] `app/services.py` presente
- [ ] `app/database.py` presente
- [ ] `app/routers/csv_upload.py` presente

### Frontend
- [ ] `templates/index.html` existe
- [ ] `static/script.js` existe
- [ ] `static/style.css` existe
- [ ] Bootstrap CDN accesible

### Datos
- [ ] `data/` carpeta existe (vacía es OK)
- [ ] `data/ejemplo_*.csv` presentes (archivos de ejemplo)

---

## 🚀 Prueba de ejecución

### Iniciar servidor
```bash
cd /ruta/a/DISUC_WEB
source venv/bin/activate      # Linux/Mac
# o
venv\Scripts\activate         # Windows

uvicorn app.main:app --reload
```

### Verificaciones esperadas

```
✓ [INFO]     Uvicorn running on http://127.0.0.1:8000
✓ 🔄 Inicializando base de datos...
✓ 📂 Cargando archivos CSV automáticamente...
✓ ✅ Inicialización completada
```

- [ ] Server inicia sin errores
- [ ] No hay excepciones en la consola
- [ ] Servidor responde en puerto 8000

### Acceso a la web

```bash
# En otra terminal
curl http://localhost:8000/api/health
```

Respuesta esperada:
```json
{"status":"ok"}
```

- [ ] Puedo acceder a http://localhost:8000
- [ ] La interfaz se ve completa
- [ ] Ver las 8 secciones de carga

---

## 🧪 Pruebas de funcionalidad

### Prueba 1: Health Check
```bash
curl http://localhost:8000/api/health
```
- [ ] Responde `{"status":"ok"}`
- [ ] Status HTTP 200

### Prueba 2: Status inicial
```bash
curl http://localhost:8000/api/upload/status
```
- [ ] Responde con JSON
- [ ] Contiene: `clientes`, `productos`, `ventas`, `pedidos`
- [ ] Valores iniciales son 0

### Prueba 3: Cargar archivo de prueba

**Opción A: Con cURL**
```bash
curl -X POST \
  -F "file=@data/ejemplo_clientes.csv" \
  http://localhost:8000/api/upload/clientes
```

**Opción B: En la web**
1. Ir a http://localhost:8000
2. Seleccionar `data/ejemplo_clientes.csv`
3. Hacer clic en "Cargar"

Resultado esperado:
```json
{"mensaje":"✓ Se cargaron 5 clientes exitosamente"}
```

- [ ] Carga se completa exitosamente
- [ ] Se muestra mensaje de éxito
- [ ] No hay errores en la consola

### Prueba 4: Verificar datos cargados
```bash
curl http://localhost:8000/api/upload/status
```

Resultado esperado:
```json
{"clientes":5,"productos":0,"ventas":0,"pedidos":0}
```

- [ ] `clientes` cambió de 0 a 5
- [ ] Otros campos siguen en 0 (no cargamos esos)

### Prueba 5: Validación de referencias

1. Cargar categorías
2. Cargar productos
3. Cargar clientes
4. Cargar ventas (con cliente y producto válidos)

Resultado esperado:
- [ ] Ventas se cargan sin errores
- [ ] Se muestra: "✓ Se cargaron X ventas"

Ahora intenta con una venta inválida:
- [ ] Muestra advertencia si falta cliente/producto
- [ ] Muestra detalles del error

---

## 📊 Script de prueba automática

```bash
python test_upload.py
```

Verifica que:
- [ ] Servidor está activo
- [ ] Estado inicial es correcto
- [ ] Archivos de ejemplo existen
- [ ] Los archivos se cargan correctamente
- [ ] El estado se actualiza

Resultado esperado:
```
🧪 DISUC - Script de Prueba de Carga de CSV
============================================================
🔍 Verificando servidor...
✅ Servidor activo

📥 Estado inicial:
  • Clientes: 0
  • Productos: 0
  • Ventas: 0
  • Pedidos: 0

📤 Cargando archivos de ejemplo...
  📤 CLIENTES... ✓ Se cargaron 5 clientes exitosamente
  📤 CATEGORIAS... ✓ Se cargaron 5 categorías exitosamente
  📤 PRODUCTOS... ✓ Se cargaron 6 productos exitosamente
  📤 VENTAS... ✓ Se cargaron 6 ventas exitosamente

✨ Estado final:
  • Clientes: 5
  • Productos: 6
  • Ventas: 6
  • Pedidos: 0

============================================================
✅ Se cargaron 4/4 archivos exitosamente
============================================================
```

- [ ] Script completa sin errores
- [ ] Resume correctamente los datos cargados

---

## 🔍 Verificación de la base de datos

### Archivo de BD existe

```bash
ls -la data/disuc.db
```

- [ ] Archivo `disuc.db` existe en `data/`
- [ ] Tiene tamaño > 0 bytes

### Inspeccionar BD (opcional)

```bash
# Si tienes sqlite3 instalado:
sqlite3 data/disuc.db ".tables"
```

Deberías ver:
```
clientes    categorias  productos   ventas
pedidos     lotes       dim_tiempo  mejores_modelos
```

- [ ] Todas las 8 tablas existen

---

## 🌐 Interfaz web completa

### Elementos visuales

- [ ] Header visible con "🏥 DISUC - Gestor de CSV"
- [ ] 8 tarjetas con inputs de archivo
- [ ] Botón "Cargar" en cada sección
- [ ] Botón "Actualizar Estado" visible
- [ ] Footer con información del proyecto

### Funcionalidad

- [ ] Puedo seleccionar archivos
- [ ] Aparece spinner durante la carga
- [ ] Mensajes de éxito/error son claros
- [ ] El estado se actualiza correctamente
- [ ] Responsive en móvil (si pruebas)

### Archivos estáticos

- [ ] Bootstrap CSS carga correctamente
- [ ] Estilos personalizados se aplican
- [ ] JavaScript funciona sin errores
- [ ] No hay errores en la consola del navegador

---

## 📁 Estructura de carpetas

Después de ejecutar, deberías tener:

```
DISUC_WEB/
├── app/
│   ├── __pycache__/          ✓ Se crea automáticamente
│   ├── routers/__pycache__/  ✓ Se crea automáticamente
│   ├── *.py                  ✓ Archivos Python
├── data/
│   ├── disuc.db              ✓ Se crea al iniciar
│   ├── ejemplo_*.csv         ✓ Archivos de ejemplo
├── templates/
│   └── index.html            ✓ Debe existir
├── static/
│   ├── script.js             ✓ Debe existir
│   ├── style.css             ✓ Debe existir
├── venv/                     ✓ Entorno virtual
└── [archivos de configuración]
```

- [ ] `__pycache__` se generó
- [ ] `disuc.db` se creó
- [ ] Todos los archivos estáticos existen

---

## 🔧 Troubleshooting

### El servidor no inicia

```bash
# Error: "Address already in use"
# Solución: Cambiar puerto
uvicorn app.main:app --reload --port 8001

# Error: "No module named 'fastapi'"
# Solución: Verificar entorno virtual activado
source venv/bin/activate
pip install -r requirements.txt
```

- [ ] Server inicia en puerto alternativo (si fue necesario)
- [ ] Módulos se instalaron correctamente

### La interfaz no carga

```bash
# Verificar que templates/index.html existe
ls templates/index.html

# Verificar que estáticos cargan
curl http://localhost:8000/static/script.js | head
```

- [ ] HTML existe
- [ ] Estáticos son accesibles

### Los archivos no se carga

```bash
# Verificar formato CSV
file data/ejemplo_clientes.csv

# Verificar que esté en UTF-8
file -bi data/ejemplo_clientes.csv
```

- [ ] CSVs están en formato correcto
- [ ] Encoding es UTF-8
- [ ] Columnas coinciden con formato esperado

---

## ✨ Indicadores de éxito

### ✅ Todo funciona si ves:

1. **Servidor inicia sin errores**
   - ✓ No hay excepciones
   - ✓ Puerto 8000 disponible

2. **Interfaz carga completa**
   - ✓ 8 secciones visibles
   - ✓ Estilos aplicados
   - ✓ Sin errores en consola

3. **Carga de archivos**
   - ✓ Puedo seleccionar CSV
   - ✓ Se procesa y muestra resultado
   - ✓ Sin excepciones

4. **Validación funciona**
   - ✓ Detecta errores de referencia
   - ✓ Carga registros válidos
   - ✓ Muestra detalles de errores

5. **BD se crea**
   - ✓ Archivo `disuc.db` existe
   - ✓ 8 tablas se crearon
   - ✓ Datos persisten

---

## 🎯 Resumen final

### Puntos críticos a verificar

- [ ] Python 3.8+ ✓
- [ ] Dependencias instaladas ✓
- [ ] Server inicia en puerto 8000 ✓
- [ ] Interfaz carga en http://localhost:8000 ✓
- [ ] Puedo seleccionar y cargar CSV ✓
- [ ] Datos se guardan en BD ✓
- [ ] Validación de referencias funciona ✓
- [ ] Carga automática al iniciar ✓

### Si todos ✓, entonces:
**✅ ¡El sistema está completamente operativo!**

---

## 📞 Si algo no funciona

1. Revisa `INSTALACION.md` - Guía paso a paso
2. Revisa `INICIO.md` - Guía rápida
3. Revisa `README.md` - Documentación completa
4. Ejecuta `python test_upload.py` - Diagnóstico automático
5. Verifica los archivos de ejemplo en `/data/`

---

**¡Bienvenido al DISUC CSV Manager!** 🚀
