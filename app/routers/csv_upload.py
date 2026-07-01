import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import CSVProcessor
from app.models import Cliente, Producto, Venta, Pedido

router = APIRouter(prefix="/api/upload", tags=["upload"])

os.makedirs('data', exist_ok=True)


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


@router.get("/status")
async def status(db: Session = Depends(get_db)):
    stats = {
        "clientes": db.query(Cliente).count(),
        "productos": db.query(Producto).count(),
        "ventas": db.query(Venta).count(),
        "pedidos": db.query(Pedido).count(),
    }
    return stats
