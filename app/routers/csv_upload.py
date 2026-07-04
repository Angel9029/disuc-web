import os
import zipfile
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import CSVProcessor
from app.models import Cliente, Producto, Venta, Pedido, Lote, Categoria, DimTiempo, MejorModelo

router = APIRouter(prefix="/api/upload", tags=["upload"])

os.makedirs('data', exist_ok=True)

REQUIRED_TABLES = ['clientes', 'productos', 'lotes', 'pedidos', 'ventas', 'dim_tiempo']

TRUNCATE_MAP = {
    'clientes': Cliente,
    'categorias': Categoria,
    'productos': Producto,
    'lotes': Lote,
    'ventas': Venta,
    'pedidos': Pedido,
    'dim_tiempo': DimTiempo,
    'mejores_modelos': MejorModelo,
}


def _truncate(db: Session, endpoint: str):
    model = TRUNCATE_MAP.get(endpoint)
    if model:
        db.query(model).delete()
        db.commit()


def _save_temp(file: UploadFile) -> str:
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos CSV")
    fd, path = tempfile.mkstemp(suffix='.csv', dir='data')
    os.close(fd)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


def _upload_endpoint(endpoint: str, loader):
    async def handler(file: UploadFile = File(...), db: Session = Depends(get_db)):
        file_path = _save_temp(file)
        try:
            _truncate(db, endpoint)
            count = loader(db, file_path)
            return {"mensaje": f"Se cargaron {count} registros exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.unlink(file_path)
    handler.__name__ = f"upload_{endpoint}"
    return handler


for ep, loader in [
    ('clientes', CSVProcessor.cargar_clientes),
    ('categorias', CSVProcessor.cargar_categorias),
    ('productos', CSVProcessor.cargar_productos),
    ('ventas', CSVProcessor.cargar_ventas),
    ('pedidos', CSVProcessor.cargar_pedidos),
    ('lotes', CSVProcessor.cargar_lotes),
    ('dim_tiempo', CSVProcessor.cargar_dim_tiempo),
    ('mejores_modelos', CSVProcessor.cargar_mejores_modelos),
]:
    router.add_api_route(
        f"/{ep}",
        _upload_endpoint(ep, loader),
        methods=["POST"],
    )


CSV_NAMES = {
    'clientes', 'categorias', 'productos', 'dim_tiempo',
    'lotes', 'ventas', 'pedidos', 'mejores_modelos'
}

LOADER_MAP = {
    'clientes': CSVProcessor.cargar_clientes,
    'categorias': CSVProcessor.cargar_categorias,
    'productos': CSVProcessor.cargar_productos,
    'dim_tiempo': CSVProcessor.cargar_dim_tiempo,
    'lotes': CSVProcessor.cargar_lotes,
    'ventas': CSVProcessor.cargar_ventas,
    'pedidos': CSVProcessor.cargar_pedidos,
    'mejores_modelos': CSVProcessor.cargar_mejores_modelos,
}


def _detect_endpoint(filename: str) -> str | None:
    name = os.path.splitext(os.path.basename(filename))[0].lower()
    if name in CSV_NAMES:
        return name
    if name == 'mejoresmodelos':
        return 'mejores_modelos'
    if name == 'dimtiempo':
        return 'dim_tiempo'
    return None


@router.post("/zip")
async def upload_zip(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos ZIP")
    tmpdir = tempfile.mkdtemp(dir='data')
    endpoints_encontrados = []
    try:
        zip_path = os.path.join(tmpdir, file.filename)
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmpdir)
        results = {}
        for fname in os.listdir(tmpdir):
            if not fname.endswith('.csv'):
                continue
            endpoint = _detect_endpoint(fname)
            if not endpoint:
                continue
            endpoints_encontrados.append(endpoint)
        for endpoint in endpoints_encontrados:
            _truncate(db, endpoint)
        for endpoint in endpoints_encontrados:
            fname = None
            for fn in os.listdir(tmpdir):
                if _detect_endpoint(fn) == endpoint:
                    fname = fn
                    break
            if not fname:
                continue
            fpath = os.path.join(tmpdir, fname)
            try:
                loader = LOADER_MAP[endpoint]
                count = loader(db, fpath)
                results[endpoint] = count
            except Exception as e:
                results[endpoint] = f"Error: {e}"
        if not results:
            raise HTTPException(status_code=400, detail="No se encontraron archivos CSV validos en el ZIP")
        return {"mensaje": "Carga completada", "resultados": results}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@router.get("/status")
async def status(db: Session = Depends(get_db)):
    stats = {
        "clientes": db.query(Cliente).count(),
        "productos": db.query(Producto).count(),
        "lotes": db.query(Lote).count(),
        "ventas": db.query(Venta).count(),
        "pedidos": db.query(Pedido).count(),
        "dim_tiempo": db.query(DimTiempo).count(),
    }
    cargados = {k for k, v in stats.items() if v > 0}
    faltantes = [t for t in REQUIRED_TABLES if t not in cargados]
    return {"completo": len(faltantes) == 0, "faltantes": faltantes, **stats}
