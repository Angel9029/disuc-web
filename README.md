# 🏥 DISUC - Gestor de CSV para Business Intelligence

Aplicación web local para gestionar carga de archivos CSV en una base de datos SQLite. Diseñada para el proyecto académico de BI y ML de la empresa farmacéutica DISUC.

## ✨ Características

- ✅ Carga automática de CSV al iniciar (si existen en `/data/`)
- ✅ Interfaz web simple con Bootstrap 5
- ✅ Validación de referencias (producto_id, cliente_id en ventas y pedidos)
- ✅ Carga manual de CSV uno por uno mediante `/upload`
- ✅ Base de datos SQLite local (sin nubes)
- ✅ Backend FastAPI con SQLAlchemy
- ✅ Responsive y accesible

## 📋 Requisitos Previos

- Python 3.8+
- pip o poetry

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd DISUC_WEB
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Copiar archivos CSV a `/data/`

Los CSV se cargarán automáticamente al iniciar si existen en esta carpeta:
- `data/clientes.csv`
- `data/categorias.csv`
- `data/productos.csv`
- `data/dim_tiempo.csv`
- `data/mejores_modelos.csv`
- `data/ventas.csv` (valida referencias)
- `data/pedidos.csv` (valida referencias)
- `data/lotes.csv` (valida referencias)

## 🎯 Cómo Usar

### Iniciar la aplicación

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

### En el navegador

1. Abre http://localhost:8000
2. Verás la interfaz con 8 secciones de carga
3. Selecciona un CSV y haz clic en "Cargar"
4. El sistema validará y cargará los datos automáticamente
5. Haz clic en "Actualizar Estado" para ver el resumen

## 📁 Estructura del Proyecto

```
DISUC_WEB/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI + rutas principales
│   ├── database.py          # Configuración de SQLite
│   ├── models.py            # Modelos SQLAlchemy
│   ├── services.py          # Lógica de procesamiento de CSV
│   └── routers/
│       ├── __init__.py
│       └── csv_upload.py    # Endpoints de carga de CSV
│
├── data/
│   ├── disuc.db             # Base de datos SQLite (se crea automáticamente)
│   └── *.csv                # Archivos CSV para carga automática
│
├── templates/
│   └── index.html           # Interfaz web
│
├── static/
│   ├── script.js            # Lógica del cliente
│   └── style.css            # Estilos CSS
│
├── requirements.txt         # Dependencias Python
└── README.md               # Este archivo
```

## 🔌 API Endpoints

### Carga de archivos

```
POST /api/upload/clientes
POST /api/upload/categorias
POST /api/upload/productos
POST /api/upload/dim_tiempo
POST /api/upload/mejores_modelos
POST /api/upload/ventas         (valida referencias)
POST /api/upload/pedidos        (valida referencias)
POST /api/upload/lotes          (valida referencias)
```

### Estado de datos

```
GET /api/upload/status
```

Retorna:
```json
{
  "clientes": 10,
  "productos": 25,
  "ventas": 100,
  "pedidos": 50
}
```

## 📊 Validación de Datos

### Ventas, Pedidos y Lotes

El sistema valida automáticamente que:
- El cliente exista en la tabla de clientes
- El producto exista en la tabla de productos

Si hay errores, se muestran los detalles y se cargan solo los registros válidos.

## 🗄️ Base de Datos

La base de datos se crea automáticamente la primera vez que se inicia la aplicación.

### Tablas

- `clientes` - Información de clientes
- `categorias` - Categorías de productos
- `productos` - Productos disponibles
- `ventas` - Registro de ventas
- `pedidos` - Pedidos de clientes
- `lotes` - Lotes de producción
- `dim_tiempo` - Dimensión de tiempo
- `mejores_modelos` - Parámetros SARIMA para predicción

## 🛠️ Desarrollo

### Para modificar modelos

1. Edita `app/models.py`
2. La BD se recreará automáticamente (o borra `data/disuc.db` para forzar reset)

### Para agregar nuevos CSV types

1. Crea el método `cargar_nuevo_tipo()` en `app/services.py`
2. Añade el endpoint en `app/routers/csv_upload.py`
3. Agrega la interfaz en `templates/index.html`

## 📝 Formato de CSV

### clientes.csv
```csv
nombre,contacto,ciudad
Cliente A,contacto@a.com,Madrid
```

### productos.csv
```csv
nombre,categoria,precio,stock
Producto 1,Categoría 1,10.50,100
```

### ventas.csv
```csv
cliente,producto,cantidad,fecha,total
Cliente A,Producto 1,5,2024-01-15,52.50
```

## ⚠️ Notas Importantes

- Todos los datos se guardan en `/data/disuc.db`
- La aplicación funciona completamente en localhost
- No se requiere conexión a internet
- Los CSVs se cargan automáticamente al iniciar (si existen)
- Se pueden cargar CSVs nuevos en cualquier momento mediante la interfaz

## 🤝 Contribuir

Este es un proyecto académico para DISUC. Para cambios significativos, por favor contacta al equipo de desarrollo.

## 📄 Licencia

Académico - DISUC
