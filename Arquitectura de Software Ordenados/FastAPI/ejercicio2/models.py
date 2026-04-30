from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from database import Base


# Tabla intermedia Coche ↔ Servicio (muchos a muchos)
coche_servicio = Table(
    "coche_servicio",
    Base.metadata,
    Column("coche_id", Integer, ForeignKey("coches.id"), primary_key=True),
    Column("servicio_id", Integer, ForeignKey("servicios.id"), primary_key=True),
    Column("observaciones", Text, default=""),
)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)

    coches = relationship("Coche", back_populates="cliente", cascade="all, delete-orphan")


class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    anio = Column(Integer)

    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="coches")
    servicios = relationship("Servicio", secondary=coche_servicio, back_populates="coches")


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    fecha = Column(String)

    coches = relationship("Coche", secondary=coche_servicio, back_populates="servicios")
