import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import init_db, SessionLocal
from app.services import CSVProcessor
from app.routers import csv_upload, prediction

os.makedirs('data', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

CSV_LOADERS = [
    ('data/clientes.csv', 'clientes', CSVProcessor.cargar_clientes),
    ('data/categorias.csv', 'categorias', CSVProcessor.cargar_categorias),
    ('data/productos.csv', 'productos', CSVProcessor.cargar_productos),
    ('data/dim_tiempo.csv', 'dim_tiempo', CSVProcessor.cargar_dim_tiempo),
    ('data/lotes.csv', 'lotes', CSVProcessor.cargar_lotes),
    ('data/ventas.csv', 'ventas', CSVProcessor.cargar_ventas),
    ('data/pedidos.csv', 'pedidos', CSVProcessor.cargar_pedidos),
    ('data/mejores_modelos.csv', 'mejores_modelos', CSVProcessor.cargar_mejores_modelos),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando base de datos...")
    init_db()

    db = SessionLocal()
    print("Cargando archivos CSV...")
    for file_path, nombre, loader in CSV_LOADERS:
        if os.path.exists(file_path):
            try:
                count = loader(db, file_path)
                print(f"  {nombre}: {count} registros cargados")
            except Exception as e:
                print(f"  Error en {nombre}: {e}")
        else:
            print(f"  {nombre}: archivo no encontrado ({file_path})")
    db.close()
    print("Inicializacion completada\n")
    yield

app = FastAPI(title="Sistema Predictivo de Demanda DISUC", version="2.0.0", lifespan=lifespan)
app.include_router(csv_upload.router)
app.include_router(prediction.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("templates/index.html")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
