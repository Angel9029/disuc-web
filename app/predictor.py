import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy import func

from statsmodels.tsa.statespace.sarimax import SARIMAX

from app.models import (
    Producto,
    Lote,
    Pedido,
    Venta,
    MejorModelo
)

class Predictor:
    @staticmethod
    def _parse_order(s: str):
        partes = s.strip().strip("()").split(",")
        return tuple(int(x.strip()) for x in partes)

    @staticmethod
    def _get_monthly_series(db: Session, producto_nombre: str):

        prod = (
            db.query(Producto)
            .filter_by(nombre=producto_nombre)
            .first()
        )

        if not prod:
            raise ValueError(
                f"No existe el producto '{producto_nombre}'"
            )

        rows = (
            db.query(
                func.strftime(
                    "%Y-%m",
                    Venta.fecha_registro
                ).label("mes"),
                func.sum(
                    Pedido.cantidad_solicitada
                ).label("total")
            )

            .select_from(Pedido)
            .join(
                Lote,
                Pedido.lote_id == Lote.lote_id
            )
            .join(
                Producto,
                Lote.producto_id == Producto.producto_id
            )
            .join(
                Venta,
                Pedido.venta_id == Venta.venta_id
            )
            .filter(
                Producto.producto_id == prod.producto_id
            )
            .group_by(
                func.strftime(
                    "%Y-%m",
                    Venta.fecha_registro
                )
            )
            .order_by("mes")
            .all()
        )

        if len(rows) == 0:
            raise ValueError(
                "No existen datos históricos."
            )

        df = pd.DataFrame(
            rows,
            columns=[
                "Fecha_Mes",
                "Cantidad_Solicitada"
            ]
        )

        df["Fecha_Mes"] = pd.to_datetime(
            df["Fecha_Mes"] + "-01"
        )

        # EXACTAMENTE IGUAL QUE COLAB

        fechas = pd.date_range(
            start="2020-01-01",
            end="2025-12-01",
            freq="MS"

        )

        serie = (
            df
            .set_index("Fecha_Mes")
            .reindex(fechas)

        )

        serie["Cantidad_Solicitada"] = (
            serie["Cantidad_Solicitada"]
            .interpolate()
        )
        return serie["Cantidad_Solicitada"]

    @staticmethod
    def predict(
        db: Session,
        producto_nombre: str,
        fecha_str: str
    ):
        
        parametros = (
            db.query(MejorModelo)
            .filter_by(
                producto=producto_nombre
            )
            .first()
        )

        if parametros is None:
            raise ValueError(
                "No existen parámetros SARIMA."
            )

        order = Predictor._parse_order(
            parametros.arima
        )

        seasonal = Predictor._parse_order(
            parametros.sarima
        )

        serie = Predictor._get_monthly_series(
            db,
            producto_nombre
        )

        modelo = SARIMAX(
            serie,
            order=order,
            seasonal_order=seasonal,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fit = modelo.fit(
            disp=False
        )

        # ---------------------------
        # CALCULAR LOS MESES
        # ---------------------------

        fecha_objetivo = pd.to_datetime(
            fecha_str
        )

        ultima = serie.index.max()
        meses = (
            (fecha_objetivo.year - ultima.year) * 12 + (fecha_objetivo.month - ultima.month)
        )

        if meses <= 0:
            raise ValueError(
                "La fecha debe ser posterior al histórico."
            )

        forecast = fit.forecast(
            steps=meses
        )

        pronostico = round(

            float(
                forecast.iloc[-1]
            ),
            2
        )

        return {
            "producto": producto_nombre,
            "fecha": fecha_str,
            "pronostico": pronostico,
            "modelo": f"SARIMA{order}{seasonal}",
            "mape": parametros.mape
        }