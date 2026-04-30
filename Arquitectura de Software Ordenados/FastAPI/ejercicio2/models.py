from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


# Tabla intermedia para la relación muchos a muchos entre Coche y Servicio.
# Incluye el campo 'observaciones' para notas específicas de cada intervención.
asociacion_coche_servicio = Table(
    "coche_servicio",
    Base.metadata,
    Column("coche_id", Integer, ForeignKey("coches.id", ondelete="CASCADE"), primary_key=True),
    Column("servicio_id", Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True),
    Column("observaciones", Text, default=""),
)


class Cliente(Base):
    """Persona propietaria de uno o más coches en el taller."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)

    coches = relationship(
        "Coche",
        back_populates="cliente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Cliente id={self.id} nombre={self.nombre!r}>"


class Coche(Base):
    """Vehículo registrado en el taller, vinculado a un cliente."""

    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(10), unique=True, nullable=False, index=True)
    marca = Column(String(50), nullable=False, index=True)
    modelo = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)

    cliente = relationship("Cliente", back_populates="coches")
    servicios = relationship(
        "Servicio",
        secondary=asociacion_coche_servicio,
        back_populates="coches",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Coche {self.matricula} — {self.marca} {self.modelo}>"


class Servicio(Base):
    """Trabajo realizado en el taller: revisión, cambio de aceite, etc."""

    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    fecha = Column(String(10), nullable=False)  # formato ISO: YYYY-MM-DD

    coches = relationship(
        "Coche",
        secondary=asociacion_coche_servicio,
        back_populates="servicios",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Servicio id={self.id} descripcion={self.descripcion!r}>"
