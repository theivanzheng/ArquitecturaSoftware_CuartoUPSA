from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Taller de Coches — API básica")

# ---------------------------------------------------------------------------
# Modelos Pydantic
# ---------------------------------------------------------------------------

class Cliente(BaseModel):
    nombre: str
    telefono: str
    email: str


class Coche(BaseModel):
    matricula: str
    marca: str
    modelo: str
    anio: int
    cliente_id: int


class Servicio(BaseModel):
    descripcion: str
    precio: float
    fecha: str


# ---------------------------------------------------------------------------
# Almacenamiento en memoria
# ---------------------------------------------------------------------------

clientes: dict[int, Cliente] = {}
coches: dict[int, Coche] = {}
servicios: dict[int, Servicio] = {}

contador_clientes = 1
contador_coches = 1
contador_servicios = 1


# ---------------------------------------------------------------------------
# Raíz
# ---------------------------------------------------------------------------

@app.get("/")
def read_root() -> dict[str, str]:
    return {"mensaje": "Bienvenido a la API del Taller de Coches"}


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

@app.get("/clientes/")
def listar_clientes() -> dict:
    return {"clientes": clientes}


@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int) -> dict:
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"cliente": clientes[cliente_id]}


@app.post("/clientes/", status_code=201)
def crear_cliente(cliente: Cliente) -> dict:
    global contador_clientes
    clientes[contador_clientes] = cliente
    resultado = {"mensaje": "Cliente creado", "id": contador_clientes, "cliente": cliente}
    contador_clientes += 1
    return resultado


@app.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente: Cliente) -> dict:
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    clientes[cliente_id] = cliente
    return {"mensaje": f"Cliente {cliente_id} actualizado", "cliente": cliente}


@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int) -> dict:
    if cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    del clientes[cliente_id]
    return {"mensaje": f"Cliente {cliente_id} eliminado"}
