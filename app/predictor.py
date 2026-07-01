import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from statsmodels.tsa.statespace.sarimax import SARIMAX
from app.models import Producto, Lote, Pedido, Venta, MejorModelo


class Predictor:
    @staticmethod
    def _parse_order(s: str):
        parts = s.strip().strip("()").split(",")
        return tuple(int(x.strip()) for x in parts)

    @staticmethod
    def _get_monthly_series(db: Session, producto_nombre: str) -> pd.Series:
        prod = db.query(Producto).filter_by(nombre=producto_nombre).first()
        if not prod:
            raise ValueError(f"Producto '{producto_nombre}' no encontrado")

        rows = (
            db.query(
                func.strftime('%Y-%m', Venta.fecha_registro).label('mes'),
                func.sum(Pedido.cantidad_solicitada).label('total')
            )
            .select_from(Pedido)
            .join(Lote, Pedido.lote_id == Lote.lote_id)
            .join(Producto, Lote.producto_id == Producto.producto_id)
            .join(Venta, Pedido.venta_id == Venta.venta_id)
            .filter(Producto.producto_id == prod.producto_id)
            .group_by(func.strftime('%Y-%m', Venta.fecha_registro))
            .order_by('mes')
            .all()
        )

        if not rows:
            raise ValueError(f"No hay datos de ventas para '{producto_nombre}'")

        df = pd.DataFrame(rows, columns=['mes', 'total'])
        df['mes'] = pd.to_datetime(df['mes'] + '-01')
        df = df.set_index('mes').sort_index()
        series = df['total'].asfreq('MS').fillna(0)

        if len(series) < 12:
            raise ValueError(
                f"Datos insuficientes para '{producto_nombre}': {len(series)} meses, se requieren al menos 12"
            )
        return series

    @staticmethod
    def predict(db: Session, producto_nombre: str, fecha_str: str) -> dict:
        prod = db.query(Producto).filter_by(nombre=producto_nombre).first()
        if not prod:
            raise ValueError(f"Producto '{producto_nombre}' no encontrado")

        params = db.query(MejorModelo).filter_by(producto=producto_nombre).first()
        if not params:
            raise ValueError(f"No hay parametros SARIMA para '{producto_nombre}'")

        series = Predictor._get_monthly_series(db, producto_nombre)

        try:
            order = Predictor._parse_order(params.arima)
            s_order = Predictor._parse_order(params.sarima)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Parametros SARIMA invalidos: {e}")

        if len(order) != 3 or len(s_order) != 4:
            raise ValueError("Orden ARIMA debe tener 3 valores y SARIMA 4")

        try:
            model = SARIMAX(
                series,
                order=order,
                seasonal_order=s_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            fitted = model.fit(disp=False, maxiter=200)
        except Exception as e:
            raise ValueError(f"Error al entrenar SARIMA: {e}")

        pred = fitted.forecast(steps=1)
        pronostico = float(round(max(0, pred.iloc[0]), 2))
        order_str = f"SARIMA{''.join(str(order).split())}{''.join(str(s_order).split())}"

        return {
            "producto": producto_nombre,
            "fecha": fecha_str,
            "pronostico": pronostico,
            "modelo": order_str,
            "mape": params.mape,
        }
