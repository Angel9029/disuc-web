from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"
    cliente_ruc = Column(String, primary_key=True)
    razon_social = Column(String)
    nombre_comercial = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)


class Categoria(Base):
    __tablename__ = "categorias"
    categoria_id = Column(Integer, primary_key=True)
    nombre = Column(String)

    productos = relationship("Producto", back_populates="categoria")


class Producto(Base):
    __tablename__ = "productos"
    producto_id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    precio_compra = Column(Float)
    precio_unitario = Column(Float)
    stock_actual = Column(Integer)
    stock_minimo = Column(Integer)
    requiere_receta = Column(Integer)
    unidad_medida = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.categoria_id"))

    categoria = relationship("Categoria", back_populates="productos")
    lotes = relationship("Lote", back_populates="producto")


class DimTiempo(Base):
    __tablename__ = "dim_tiempo"
    fecha_id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    dia = Column(Integer)
    mes = Column(Integer)
    anio = Column(Integer)
    trimestre = Column(Integer)

    ventas = relationship("Venta", back_populates="dim_tiempo")


class Lote(Base):
    __tablename__ = "lotes"
    lote_id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.producto_id"))
    cantidad_inicial = Column(Integer)
    cantidad_disponible = Column(Integer)
    fecha_vencimiento = Column(Date)
    estado = Column(String)

    producto = relationship("Producto", back_populates="lotes")
    pedidos = relationship("Pedido", back_populates="lote")


class Venta(Base):
    __tablename__ = "ventas"
    venta_id = Column(Integer, primary_key=True)
    fecha_registro = Column(Date, index=True)
    fecha_envio = Column(Date)
    estado = Column(String)
    monto_total = Column(Float)
    fecha_id = Column(Integer, ForeignKey("dim_tiempo.fecha_id"))

    dim_tiempo = relationship("DimTiempo", back_populates="ventas")
    pedidos = relationship("Pedido", back_populates="venta")


class Pedido(Base):
    __tablename__ = "pedidos"
    pedido_id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("ventas.venta_id"), index=True)
    cliente_ruc = Column(String, ForeignKey("clientes.cliente_ruc"), index=True)
    lote_id = Column(Integer, ForeignKey("lotes.lote_id"))
    cantidad_solicitada = Column(Integer)
    precio_unitario = Column(Float)
    subtotal = Column(Float)
    igv = Column(Float)
    total = Column(Float)

    venta = relationship("Venta", back_populates="pedidos")
    cliente = relationship("Cliente")
    lote = relationship("Lote", back_populates="pedidos")


class MejorModelo(Base):
    __tablename__ = "mejores_modelos"
    id = Column(Integer, primary_key=True)
    producto = Column(String, unique=True, index=True)
    arima = Column(String)
    sarima = Column(String)
    mae = Column(Float)
    rmse = Column(Float)
    mape = Column(Float)
    aic = Column(Float)
