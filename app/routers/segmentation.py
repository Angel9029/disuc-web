from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.segmenter import KMeansSegmenter, DOWNLOAD_STORE

router = APIRouter(tags=["segmentation"])


@router.post("/segmentation/execute")
def execute_segmentation(db: Session = Depends(get_db)):
    try:
        result = KMeansSegmenter.segment(db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


@router.get("/segmentation/download/{token}")
def download_segmentation(token: str):
    excel_bytes = DOWNLOAD_STORE.get(token)
    if excel_bytes is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=Detalle_Lotes_Riesgo.xlsx"
        },
    )
