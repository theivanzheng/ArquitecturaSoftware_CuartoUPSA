from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


# ---------------------------------------------------------------------------
# Coches
# ---------------------------------------------------------------------------

@app.get("/coches/")
def listar_coches() -> dict:
    return {"coches": coches}


@app.get("/coches/{coche_id}")
def obtener_coche(coche_id: int) -> dict:
    if coche_id not in coches:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return {"coche": coches[coche_id]}


@app.post("/coches/", status_code=201)
def crear_coche(coche: Coche) -> dict:
    global contador_coches
    if coche.cliente_id not in clientes:
        raise HTTPException(status_code=404, detail="El cliente especificado no existe")
    coches[contador_coches] = coche
    resultado = {"mensaje": "Coche registrado", "id": contador_coches, "coche": coche}
    contador_coches += 1
    return resultado


@app.put("/coches/{coche_id}")
def actualizar_coche(coche_id: int, coche: Coche) -> dict:
    if coche_id not in coches:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    coches[coche_id] = coche
    return {"mensaje": f"Coche {coche_id} actualizado", "coche": coche}


@app.delete("/coches/{coche_id}")
def eliminar_coche(coche_id: int) -> dict:
    if coche_id not in coches:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    del coches[coche_id]
    return {"mensaje": f"Coche {coche_id} eliminado"}


# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------

@app.get("/servicios/")
def listar_servicios() -> dict:
    return {"servicios": servicios}


@app.get("/servicios/{servicio_id}")
def obtener_servicio(servicio_id: int) -> dict:
    if servicio_id not in servicios:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"servicio": servicios[servicio_id]}


@app.post("/servicios/", status_code=201)
def crear_servicio(servicio: Servicio) -> dict:
    global contador_servicios
    servicios[contador_servicios] = servicio
    resultado = {"mensaje": "Servicio registrado", "id": contador_servicios, "servicio": servicio}
    contador_servicios += 1
    return resultado


@app.put("/servicios/{servicio_id}")
def actualizar_servicio(servicio_id: int, servicio: Servicio) -> dict:
    if servicio_id not in servicios:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    servicios[servicio_id] = servicio
    return {"mensaje": f"Servicio {servicio_id} actualizado", "servicio": servicio}


@app.delete("/servicios/{servicio_id}")
def eliminar_servicio(servicio_id: int) -> dict:
    if servicio_id not in servicios:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    del servicios[servicio_id]
    return {"mensaje": f"Servicio {servicio_id} eliminado"}
