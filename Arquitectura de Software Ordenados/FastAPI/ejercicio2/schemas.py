from pydantic import BaseModel, Field


# --- Servicio ---

class ServicioBase(BaseModel):
    descripcion: str
    precio: float
    fecha: str


class ServicioCreate(ServicioBase):
    pass


class ServicioResponse(ServicioBase):
    id: int

    class Config:
        from_attributes = True


# --- Coche ---

class CocheBase(BaseModel):
    matricula: str
    marca: str
    modelo: str
    anio: int
    cliente_id: int


class CocheCreate(CocheBase):
    pass


class CocheResponse(CocheBase):
    id: int
    servicios: list[ServicioResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


# --- Cliente ---

class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    email: str


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
    coches: list[CocheResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
