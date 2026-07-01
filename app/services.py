import os
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import (
    Cliente, Categoria, Producto, Venta, Pedido, Lote, DimTiempo, MejorModelo
)


def _read_csv(file_path: str) -> list[dict]:
    with open(file_path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


class CSVProcessor:

    @staticmethod
    def cargar_clientes(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            ruc = row.get('Cliente_RUC', '').strip()
            if not ruc:
                continue
            if db.query(Cliente).filter_by(cliente_ruc=ruc).first():
                continue
            cliente = Cliente(
                cliente_ruc=ruc,
                razon_social=row.get('Razon_Social', '').strip(),
                nombre_comercial=row.get('Nombre_Comercial', '').strip(),
                direccion=row.get('Direccion', '').strip(),
                telefono=row.get('Telefono', '').strip(),
                email=row.get('Email', '').strip(),
            )
            db.add(cliente)
            count += 1
        db.commit()
        return count

    @staticmethod
    def cargar_categorias(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            cid = int(row.get('Categoria_ID', 0))
            if db.query(Categoria).filter_by(categoria_id=cid).first():
                continue
            categoria = Categoria(
                categoria_id=cid,
                nombre=row.get('Nombre', '').strip(),
            )
            db.add(categoria)
            count += 1
        db.commit()
        return count

    @staticmethod
    def cargar_productos(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            pid = int(row.get('Producto_ID', 0))
            if db.query(Producto).filter_by(producto_id=pid).first():
                continue
            producto = Producto(
                producto_id=pid,
                nombre=row.get('Nombre', '').strip(),
                precio_compra=float(row.get('Precio_Compra', 0) or 0),
                precio_unitario=float(row.get('Precio_Unitario', 0) or 0),
                stock_actual=int(row.get('Stock_Actual', 0) or 0),
                stock_minimo=int(row.get('Stock_Minimo', 0) or 0),
                requiere_receta=int(row.get('Requiere_Receta', 0) or 0),
                unidad_medida=row.get('Unidad_Medida', '').strip(),
                categoria_id=int(row.get('Categoria_ID', 0) or 0),
            )
            db.add(producto)
            count += 1
        db.commit()
        return count

    @staticmethod
    def cargar_dim_tiempo(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            fid = int(row.get('Fecha_ID', 0))
            if db.query(DimTiempo).filter_by(fecha_id=fid).first():
                continue
            dim = DimTiempo(
                fecha_id=fid,
                fecha=datetime.strptime(row.get('Fecha', ''), '%Y-%m-%d').date(),
                dia=int(row.get('Dia', 0)),
                mes=int(row.get('Mes', 0)),
                anio=int(row.get('Anio', 0)),
                trimestre=int(row.get('Trimestre', 0)),
            )
            db.add(dim)
            count += 1
        db.commit()
        return count

    @staticmethod
    def cargar_lotes(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            lid = int(row.get('Lote_ID', 0))
            if db.query(Lote).filter_by(lote_id=lid).first():
                continue
            fecha_venc = row.get('Fecha_Vencimiento', '').strip()
            lote = Lote(
                lote_id=lid,
                producto_id=int(row.get('Producto_ID', 0)),
                cantidad_inicial=int(row.get('Cantidad_Inicial', 0) or 0),
                cantidad_disponible=int(row.get('Cantidad_Disponible', 0) or 0),
                fecha_vencimiento=datetime.strptime(fecha_venc, '%Y-%m-%d').date() if fecha_venc else None,
                estado=row.get('Estado', '').strip(),
            )
            db.add(lote)
            count += 1
        db.commit()
        return count

    @staticmethod
    def cargar_ventas(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            vid = int(row.get('Venta_ID', 0))
            if db.query(Venta).filter_by(venta_id=vid).first():
                continue
            fecha_reg = row.get('Fecha_Registro', '').strip()
            fecha_env = row.get('Fecha_Envio', '').strip()
            venta = Venta(
                venta_id=vid,
                fecha_registro=datetime.strptime(fecha_reg, '%Y-%m-%d').date() if fecha_reg else None,
                fecha_envio=datetime.strptime(fecha_env, '%Y-%m-%d').date() if fecha_env else None,
                estado=row.get('Estado', '').strip(),
                monto_total=float(row.get('Monto_Total', 0) or 0),
                fecha_id=int(row.get('Fecha_ID', 0) or 0),
            )
            db.add(venta)
            count += 1
            if count % 2000 == 0:
                db.commit()
        db.commit()
        return count

    @staticmethod
    def cargar_pedidos(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            pid = int(row.get('Pedido_ID', 0))
            if db.query(Pedido).filter_by(pedido_id=pid).first():
                continue
            pedido = Pedido(
                pedido_id=pid,
                venta_id=int(row.get('Venta_ID', 0) or 0),
                cliente_ruc=row.get('Cliente_RUC', '').strip(),
                lote_id=int(row.get('Lote_ID', 0) or 0),
                cantidad_solicitada=int(row.get('Cantidad_Solicitada', 0) or 0),
                precio_unitario=float(row.get('Precio_Unitario', 0) or 0),
                subtotal=float(row.get('Subtotal', 0) or 0),
                igv=float(row.get('IGV', 0) or 0),
                total=float(row.get('Total', 0) or 0),
            )
            db.add(pedido)
            count += 1
            if count % 5000 == 0:
                db.commit()
        db.commit()
        return count

    @staticmethod
    def cargar_mejores_modelos(db: Session, file_path: str):
        rows = _read_csv(file_path)
        count = 0
        for row in rows:
            nombre = row.get('Producto', '').strip()
            if not nombre:
                continue
            if db.query(MejorModelo).filter_by(producto=nombre).first():
                continue
            modelo = MejorModelo(
                producto=nombre,
                arima=row.get('ARIMA', '').strip(),
                sarima=row.get('SARIMA', '').strip(),
                mae=float(row.get('MAE', 0) or 0),
                rmse=float(row.get('RMSE', 0) or 0),
                mape=float(row.get('MAPE', 0) or 0),
                aic=float(row.get('AIC', 0) or 0),
            )
            db.add(modelo)
            count += 1
        db.commit()
        return count
