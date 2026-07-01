# ✨ Características Principales del Sistema

## 🎯 Lo que puedes hacer

### 1. 📤 Cargar CSVs de forma simple

```
┌─────────────────────────────────────────┐
│  DISUC - Gestor de CSV                  │
├─────────────────────────────────────────┤
│                                         │
│  👥 Clientes     [Seleccionar] [Cargar] │
│  🏷️ Categorías    [Seleccionar] [Cargar] │
│  📦 Productos    [Seleccionar] [Cargar] │
│  📅 Dim Tiempo   [Seleccionar] [Cargar] │
│  🤖 Mejores Modelos [Seleccionar] [Cargar] │
│  💰 Ventas       [Seleccionar] [Cargar] │
│  📋 Pedidos      [Seleccionar] [Cargar] │
│  📦 Lotes        [Seleccionar] [Cargar] │
│                                         │
│         [🔄 Actualizar Estado]         │
│                                         │
└─────────────────────────────────────────┘
```

### 2. ✅ Validación automática de referencias

```
FLUJO DE VALIDACIÓN:

┌────────────────┐
│  Cargar Ventas │
└────────┬───────┘
         │
         ▼
┌──────────────────────────────────┐
│ ¿El cliente existe?              │
│ ┌ SI  ▶ Continuar               │
│ └ NO  ▶ Marcar error             │
└──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ ¿El producto existe?             │
│ ┌ SI  ▶ Insertar registro        │
│ └ NO  ▶ Marcar error             │
└──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│ Mostrar resultado:               │
│ ✓ X registros cargados          │
│ ⚠️ Y errores encontrados         │
└──────────────────────────────────┘
```

### 3. 🔄 Carga automática al iniciar

```
SECUENCIA DE INICIO:

1. Crear base de datos → ✓
   ├─ 8 tablas SQL
   └─ Índices

2. Buscar CSVs en /data/
   ├─ categorias.csv     → ✓ (0 dependencias)
   ├─ clientes.csv       → ✓ (0 dependencias)
   ├─ productos.csv      → ✓ (necesita categorias)
   ├─ dim_tiempo.csv     → ✓ (0 dependencias)
   ├─ mejores_modelos.csv → ✓ (0 dependencias)
   ├─ ventas.csv         → ✓ (necesita clientes + productos)
   ├─ pedidos.csv        → ✓ (necesita clientes + productos)
   └─ lotes.csv          → ✓ (necesita productos)

3. Mostrar resumen → ✓
   Aplicación lista → ✓
```

---

## 🎮 Interfaz de Usuario

### Características del Frontend

| Característica | Descripción |
|---|---|
| **Responsive** | Funciona en móvil, tablet y desktop |
| **Drag & Drop** | Arrastra archivos o usa el selector |
| **Feedback Visual** | Spinner durante carga, alertas de resultado |
| **Bootstrap 5** | Diseño moderno y accesible |
| **JavaScript Vanilla** | Sin dependencias pesadas |
| **HTTPS Local** | Funciona en http://localhost:8000 |

### Estados de Carga

```
Inicial          Cargando         Éxito           Error
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ [Seleccionar] │ ⏳ Loading │ │ ✓ Cargado │ │ ❌ Error  │
│ [Cargar]      │ ...       │ │ 5 registros   │ │ Detalles │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## 🗄️ Base de Datos

### 8 Tablas Relacionadas

```
DIAGRAMA DE RELACIONES:

┌──────────────────┐
│   categorias     │
│ ├─ id (PK)       │
│ ├─ nombre        │
│ └─ descripcion   │
└────────┬─────────┘
         │ (1:N)
         │
         ▼
┌──────────────────┐         ┌──────────────────┐
│   productos      │◄────────│   lotes          │
│ ├─ id (PK)       │  (1:N)  │ ├─ id (PK)       │
│ ├─ nombre        │         │ ├─ producto_id   │
│ ├─ categoria_id  │         │ ├─ numero_lote   │
│ ├─ precio        │         │ └─ ...           │
│ └─ stock         │         └──────────────────┘
└──┬──────────────┬┘
   │ (1:N)       │ (1:N)
   │             │
   ▼             ▼
┌──────────────────┐    ┌──────────────────┐
│   ventas         │    │   pedidos        │
│ ├─ id (PK)       │    │ ├─ id (PK)       │
│ ├─ cliente_id    │    │ ├─ cliente_id    │
│ ├─ producto_id   │    │ ├─ producto_id   │
│ ├─ cantidad      │    │ ├─ cantidad      │
│ ├─ fecha         │    │ ├─ fecha_pedido  │
│ └─ total         │    │ ├─ fecha_entrega │
└────────┬─────────┘    │ └─ estado        │
         │              └──────────────────┘
         │ (N:1)
         │
         ▼
┌──────────────────┐
│   clientes       │
│ ├─ id (PK)       │
│ ├─ nombre        │
│ ├─ contacto      │
│ └─ ciudad        │
└──────────────────┘

Tabla adicional:
┌──────────────────┐
│   dim_tiempo     │
│ ├─ id (PK)       │
│ ├─ fecha         │
│ ├─ año, mes, ...  │
└──────────────────┘

┌──────────────────┐
│   mejores_modelos│
│ ├─ id (PK)       │
│ ├─ producto      │
│ ├─ sarima        │
│ ├─ mape, rmse... │
└──────────────────┘
```

---

## 🌐 API REST

### Estructura de Endpoints

```
POST /api/upload/{tipo}
├─ /clientes            (sin validación)
├─ /categorias          (sin validación)
├─ /productos           (sin validación)
├─ /dim_tiempo          (sin validación)
├─ /mejores_modelos     (sin validación)
├─ /ventas              (✓ con validación)
├─ /pedidos             (✓ con validación)
└─ /lotes               (✓ con validación)

GET /api/upload/status
└─ Retorna: {clientes, productos, ventas, pedidos}

GET /api/health
└─ Retorna: {status: "ok"}
```

---

## 📊 Flujo de Datos

### De CSV a Base de Datos

```
┌─────────────┐
│ Archivo CSV │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ 1. Validar formato   │
│    - Es un CSV?      │
│    - Tiene columnas? │
└──────┬───────────────┘
       │ OK
       ▼
┌──────────────────────┐
│ 2. Leer registros    │
│    - Parsear filas   │
│    - Mapear campos   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 3. Validar datos     │
│    - Tipos corretos? │
│    - Referencias OK? │
└──────┬───────────────┘
       │
       ├─ SI ▶ Continuar
       └─ NO ▶ Registrar error
       │
       ▼
┌──────────────────────┐
│ 4. Insertar en BD    │
│    - Transacción     │
│    - Confirmar       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 5. Retornar resultado│
│    - Conteo          │
│    - Errores         │
└──────────────────────┘
```

---

## 🔐 Seguridad

### Características de seguridad implementadas

```
✅ Entrada
  ├─ Validación de tipo de archivo (solo CSV)
  ├─ Validación de formato de datos
  └─ Sanitización de entrada

✅ Procesamiento
  ├─ Transacciones atómicas (todo o nada)
  ├─ Validación de referencias
  └─ Manejo de errores

✅ Almacenamiento
  ├─ Base de datos local (sin nube)
  ├─ Encriptación opcional (SQLite)
  └─ Respaldo en archivos

✅ Red
  ├─ Localhost solo (127.0.0.1)
  ├─ Sin conexión externa
  └─ HTTP local (sin HTTPS necesario)
```

---

## ⚙️ Arquitectura

### Capas de la aplicación

```
┌─────────────────────────────────┐
│      Capa de Presentación        │
│  (Frontend - HTML/CSS/JS)        │
│  http://localhost:8000           │
└────────────┬────────────────────┘
             │ Fetch API
             ▼
┌─────────────────────────────────┐
│      Capa de API REST            │
│  (FastAPI - Endpoints)           │
│  POST /api/upload/{tipo}         │
│  GET /api/upload/status          │
└────────────┬────────────────────┘
             │ SQLAlchemy ORM
             ▼
┌─────────────────────────────────┐
│      Capa de Lógica              │
│  (Services - Procesamiento)      │
│  CSVProcessor                    │
│  - cargar_clientes()             │
│  - cargar_productos()            │
│  - cargar_ventas()               │
│  - etc...                        │
└────────────┬────────────────────┘
             │ SQL Queries
             ▼
┌─────────────────────────────────┐
│      Capa de Persistencia        │
│  (SQLite - Base de Datos)        │
│  /data/disuc.db                  │
│  - 8 tablas                      │
│  - Índices                       │
│  - Relaciones                    │
└─────────────────────────────────┘
```

---

## 📈 Rendimiento

### Características de optimización

| Aspecto | Implementación |
|--------|---|
| **Índices** | En claves primarias y foráneas |
| **Validación** | Antes de insertar (evita errores) |
| **Transacciones** | Atómicas (consistencia garantizada) |
| **Caché** | Frontend cachea estado local |
| **Carga** | Automática en background al iniciar |

---

## 🎓 Integración con el proyecto DISUC

### Cómo se integra con SARIMA

```
┌─────────────────────────────────────────┐
│   DISUC CSV Manager (Este proyecto)     │
│   - Cargar datos históricos             │
│   - Validar integridad                  │
│   - Almacenar en SQLite                 │
└──────────────┬──────────────────────────┘
               │ Datos limpios
               ▼
┌─────────────────────────────────────────┐
│   Módulo SARIMA (Próximo)               │
│   - Leer histórico de productos         │
│   - Obtener parámetros de mejores_modelos│
│   - Entrenar modelo SARIMA              │
│   - Generar pronósticos                 │
└─────────────────────────────────────────┘
```

---

## 🚀 Caso de Uso Típico

### Paso a paso

```
1. Usuario ejecuta: uvicorn app.main:app --reload
   ↓
2. Sistema crea BD y carga CSVs automáticamente
   ↓
3. Usuario abre: http://localhost:8000
   ↓
4. Ve la interfaz con 8 secciones
   ↓
5. Selecciona un CSV y hace clic en "Cargar"
   ↓
6. Sistema valida y carga los datos
   ↓
7. Usuario ve resumen: "✓ Se cargaron 150 registros"
   ↓
8. Repite con otros CSVs según sea necesario
   ↓
9. Todos los datos están en /data/disuc.db
   ↓
10. Listos para usar en análisis SARIMA
```

---

## 📝 Formatos soportados

### Extensiones
- ✅ `.csv` - Comma-Separated Values
- ✅ Encoding UTF-8
- ✅ Headers en primera fila

### Delimitadores
- ✅ Comas (,)
- ✅ Soporta texto con comillas

### Tipos de datos
- ✅ Strings (texto)
- ✅ Números (enteros y decimales)
- ✅ Fechas (YYYY-MM-DD)

---

## 🎯 Resumen Visual

```
              ┌──────────────┐
              │   Usuario    │
              └───────┬──────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    [Web UI]    [API REST]    [Terminal]
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │   FastAPI        │
            │  (Backend)       │
            └────────┬─────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    [Services]  [Models]  [Database]
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
            ┌──────────────────┐
            │  SQLite BD       │
            │  /data/disuc.db  │
            │  (8 tablas)      │
            └──────────────────┘
```

---

**¡El sistema está listo para usar!** 🎉
