# 📡 Documentación de API

## Base URL

```
http://localhost:8000
```

## Endpoints de Carga de CSV

### 1. Cargar Clientes
```http
POST /api/upload/clientes
Content-Type: multipart/form-data

file: clientes.csv
```

**Respuesta exitosa (200):**
```json
{
  "mensaje": "✓ Se cargaron 5 clientes exitosamente"
}
```

---

### 2. Cargar Categorías
```http
POST /api/upload/categorias
Content-Type: multipart/form-data

file: categorias.csv
```

**Respuesta:**
```json
{
  "mensaje": "✓ Se cargaron 5 categorías exitosamente"
}
```

---

### 3. Cargar Productos
```http
POST /api/upload/productos
Content-Type: multipart/form-data

file: productos.csv
```

**Respuesta:**
```json
{
  "mensaje": "✓ Se cargaron 6 productos exitosamente"
}
```

---

### 4. Cargar Dim Tiempo
```http
POST /api/upload/dim_tiempo
Content-Type: multipart/form-data

file: dim_tiempo.csv
```

---

### 5. Cargar Mejores Modelos
```http
POST /api/upload/mejores_modelos
Content-Type: multipart/form-data

file: mejores_modelos.csv
```

---

### 6. Cargar Ventas (con validación)
```http
POST /api/upload/ventas
Content-Type: multipart/form-data

file: ventas.csv
```

**Respuesta con referencias válidas:**
```json
{
  "cargados": 6,
  "mensaje": "✓ Se cargaron 6 ventas exitosamente"
}
```

**Respuesta con errores de validación:**
```json
{
  "cargados": 4,
  "errores": [
    "Fila 3: Cliente 'Cliente Inexistente' no existe",
    "Fila 5: Producto 'Producto Fantasma' no existe"
  ]
}
```

---

### 7. Cargar Pedidos (con validación)
```http
POST /api/upload/pedidos
Content-Type: multipart/form-data

file: pedidos.csv
```

---

### 8. Cargar Lotes (con validación)
```http
POST /api/upload/lotes
Content-Type: multipart/form-data

file: lotes.csv
```

---

## Endpoint de Estado

### Obtener Estado de Datos
```http
GET /api/upload/status
```

**Respuesta:**
```json
{
  "clientes": 5,
  "productos": 6,
  "ventas": 6,
  "pedidos": 0
}
```

---

## Endpoint de Salud

### Health Check
```http
GET /api/health
```

**Respuesta:**
```json
{
  "status": "ok"
}
```

---

## Ejemplo con cURL

### Cargar archivos desde terminal

```bash
# Cargar clientes
curl -X POST \
  -F "file=@data/ejemplo_clientes.csv" \
  http://localhost:8000/api/upload/clientes

# Cargar categorías
curl -X POST \
  -F "file=@data/ejemplo_categorias.csv" \
  http://localhost:8000/api/upload/categorias

# Cargar productos
curl -X POST \
  -F "file=@data/ejemplo_productos.csv" \
  http://localhost:8000/api/upload/productos

# Cargar ventas (con validación)
curl -X POST \
  -F "file=@data/ejemplo_ventas.csv" \
  http://localhost:8000/api/upload/ventas

# Ver estado
curl http://localhost:8000/api/upload/status
```

---

## Ejemplo con Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Cargar clientes
with open("data/ejemplo_clientes.csv", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/upload/clientes",
        files={"file": f}
    )
    print(response.json())

# Obtener estado
response = requests.get(f"{BASE_URL}/api/upload/status")
print(response.json())
```

---

## Ejemplo con JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000";

// Cargar archivo
async function uploadFile(type, filePath) {
  const formData = new FormData();
  const file = await fetch(filePath).then(r => r.blob());
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/api/upload/${type}`, {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  console.log(data);
}

// Obtener estado
async function getStatus() {
  const response = await fetch(`${BASE_URL}/api/upload/status`);
  const data = await response.json();
  console.log(data);
}

// Usar
uploadFile("clientes", "data/ejemplo_clientes.csv");
getStatus();
```

---

## Códigos de Error

| Código | Descripción |
|--------|------------|
| 200    | ✓ Operación exitosa |
| 400    | ❌ Archivo no es CSV o formato inválido |
| 404    | ❌ Endpoint no encontrado |
| 422    | ❌ Datos no válidos |
| 500    | ❌ Error interno del servidor |

---

## Validación de Referencias

### Flujo de Validación para Ventas/Pedidos

1. Se lee el CSV
2. Para cada fila:
   - Se busca el cliente por nombre en la BD
   - Se busca el producto por nombre en la BD
   - Si NO existen → Se registra el error
   - Si existen → Se inserta el registro
3. Se retorna el total de insertados y los errores

### Ejemplo de Error

Si intentas cargar ventas sin que existan los clientes/productos:

```json
{
  "cargados": 0,
  "errores": [
    "Fila 2: Cliente 'Farmacia Central' no existe",
    "Fila 3: Producto 'Vitamina D 1000UI' no existe"
  ]
}
```

**Solución:** Carga primero los CSVs de clientes, categorías y productos.

---

## Estructura de Base de Datos

La BD se crea automáticamente en `/data/disuc.db` con las siguientes tablas:

| Tabla | Descripción |
|-------|------------|
| clientes | Información de clientes |
| categorias | Categorías de productos |
| productos | Catálogo de productos |
| ventas | Histórico de ventas |
| pedidos | Pedidos de clientes |
| lotes | Lotes de producción |
| dim_tiempo | Dimensión temporal |
| mejores_modelos | Parámetros SARIMA |

---

## Notas Importantes

- ✅ Todos los archivos DEBEN ser CSV
- ✅ Las columnas deben coincidir exactamente con el formato esperado
- ✅ Las fechas deben estar en formato `YYYY-MM-DD`
- ✅ Los nombres de cliente/producto deben ser exactos (case-sensitive)
- ✅ No hay límite de tamaño de archivo (pero procesa más lentamente si es muy grande)

---

## Ayuda

Si tienes problemas, consulta el archivo `README.md` o los archivos de ejemplo en `/data/ejemplo_*.csv`.
