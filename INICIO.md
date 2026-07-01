# 🚀 Guía Rápida de Inicio

## Activar el entorno virtual

```bash
# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

## Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

Verás algo como esto:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
🔄 Inicializando base de datos...
📂 Cargando archivos CSV automáticamente...
  - categorias.csv no encontrado (se puede cargar luego)
  - clientes.csv no encontrado (se puede cargar luego)
  [etc...]
✅ Inicialización completada
```

## Abrir en el navegador

```
http://localhost:8000
```

Verás una interfaz bonita con 8 secciones para cargar CSV:
- 👥 Clientes
- 🏷️ Categorías
- 📦 Productos
- 📅 Dim Tiempo
- 🤖 Mejores Modelos
- 💰 Ventas
- 📋 Pedidos
- 📦 Lotes

## ¿Cómo cargar datos?

### Opción 1: Carga automática (al iniciar)

1. Copia tus archivos CSV a la carpeta `/data/`
2. Reinicia la aplicación
3. Los CSV se cargarán automáticamente

### Opción 2: Carga manual (en cualquier momento)

1. En la interfaz web, selecciona un archivo CSV
2. Haz clic en "Cargar"
3. El sistema procesará el archivo y mostrará el resultado

## 📝 Formato de los CSV

Consulta la sección de "Formato de CSV" en el `README.md` para ver ejemplos.

## ✨ Características principales

- ✅ Los CSVs se cargan **uno por uno**
- ✅ **Validación automática** de referencias (cliente_id, producto_id)
- ✅ **Interfaz web simple** y responsive
- ✅ **Base de datos local** (SQLite) en `/data/disuc.db`
- ✅ **Sin conexión a internet** necesaria
- ✅ Todo funciona en **localhost**

## 🔍 Ver el estado

Haz clic en "🔄 Actualizar Estado" para ver cuántos registros de cada tipo tienes cargados.

## 🛑 Detener la aplicación

Presiona `Ctrl+C` en la terminal donde corre el servidor.

## 📚 Más información

Lee el archivo `README.md` para documentación completa.
