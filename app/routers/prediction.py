from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Producto
from app.predictor import Predictor

router = APIRouter(tags=["prediction"])


class PronosticoRequest(BaseModel):
    producto: str
    fecha: str


@router.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    resultados = (
        db.query(Producto)
        .order_by(Producto.nombre)
        .with_entities(Producto.producto_id, Producto.nombre)
        .all()
    )
    return [{"id": r.producto_id, "nombre": r.nombre} for r in resultados]


@router.get("/productos/search")
def buscar_productos(q: str = "", db: Session = Depends(get_db)):
    resultados = (
        db.query(Producto)
        .filter(Producto.nombre.ilike(f"%{q}%"))
        .order_by(Producto.nombre)
        .with_entities(Producto.producto_id, Producto.nombre)
        .limit(20)
        .all()
    )
    return [{"id": r.producto_id, "nombre": r.nombre} for r in resultados]


@router.post("/pronosticar")
def pronosticar(body: PronosticoRequest, db: Session = Depends(get_db)):
    try:
        resultado = Predictor.predict(db, body.producto, body.fecha)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
