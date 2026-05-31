from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import motor, Base
from dependencies import get_db
from models import Cliente, Coche, Servicio
from schemas import (
    ClienteCreate, ClienteResponse,
    CocheCreate, CocheResponse,
    ServicioCreate, ServicioResponse,
)

app = FastAPI(
    title="Taller de Coches — API con base de datos",
    description="API REST para gestionar clientes, coches y servicios de un taller mecánico.",
    version="2.0",
)


@app.on_event("startup")
async def crear_tablas():
    """Crea las tablas en SQLite al arrancar si no existen."""
    async with motor.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", tags=["General"])
def inicio():
    return {"mensaje": "API del Taller de Coches — visita /docs para ver los endpoints"}


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

@app.post("/clientes/", response_model=ClienteResponse, status_code=201, tags=["Clientes"])
async def crear_cliente(datos: ClienteCreate, db: AsyncSession = Depends(get_db)):
    """Registra un nuevo cliente en el taller."""
    existe = await db.execute(select(Cliente).where(Cliente.email == datos.email))
    if existe.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Ya existe un cliente con ese email")
    cliente = Cliente(**datos.dict())
    db.add(cliente)
    await db.flush()
    await db.refresh(cliente)
    return cliente


@app.get("/clientes/", response_model=list[ClienteResponse], tags=["Clientes"])
async def listar_clientes(db: AsyncSession = Depends(get_db)):
    """Devuelve todos los clientes con sus coches."""
    resultado = await db.execute(select(Cliente))
    return resultado.scalars().all()


@app.get("/clientes/buscar/", response_model=list[ClienteResponse], tags=["Clientes"])
async def buscar_clientes(
    nombre: str = Query(..., description="Texto a buscar en el nombre del cliente"),
    db: AsyncSession = Depends(get_db),
):
    """Busca clientes cuyo nombre contenga el texto indicado (sin distinguir mayúsculas)."""
    resultado = await db.execute(
        select(Cliente).where(Cliente.nombre.ilike(f"%{nombre}%"))
    )
    clientes = resultado.scalars().all()
    if not clientes:
        raise HTTPException(status_code=404, detail="No se encontraron clientes con ese nombre")
    return clientes


@app.get("/clientes/{cliente_id}", response_model=ClienteResponse, tags=["Clientes"])
async def obtener_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    """Devuelve el detalle de un cliente junto con todos sus coches y servicios."""
    resultado = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = resultado.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@app.put("/clientes/{cliente_id}", response_model=ClienteResponse, tags=["Clientes"])
async def actualizar_cliente(cliente_id: int, datos: ClienteCreate, db: AsyncSession = Depends(get_db)):
    """Actualiza los datos de un cliente existente."""
    resultado = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = resultado.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for campo, valor in datos.dict().items():
        setattr(cliente, campo, valor)
    await db.flush()
    await db.refresh(cliente)
    return cliente


@app.delete("/clientes/{cliente_id}", tags=["Clientes"])
async def eliminar_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    """Elimina un cliente y todos sus coches asociados (cascade)."""
    resultado = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = resultado.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    await db.delete(cliente)
    return {"mensaje": f"Cliente '{cliente.nombre}' eliminado correctamente"}


# ---------------------------------------------------------------------------
# Coches
# ---------------------------------------------------------------------------

@app.post("/coches/", response_model=CocheResponse, status_code=201, tags=["Coches"])
async def crear_coche(datos: CocheCreate, db: AsyncSession = Depends(get_db)):
    """Registra un coche nuevo. El cliente_id debe existir en la base de datos."""
    cliente = await db.execute(select(Cliente).where(Cliente.id == datos.cliente_id))
    if not cliente.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="El cliente indicado no existe")

    matricula = await db.execute(select(Coche).where(Coche.matricula == datos.matricula))
    if matricula.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Ya existe un coche con esa matrícula")

    coche = Coche(**datos.dict())
    db.add(coche)
    await db.flush()
    await db.refresh(coche)
    return coche


@app.get("/coches/", response_model=list[CocheResponse], tags=["Coches"])
async def listar_coches(db: AsyncSession = Depends(get_db)):
    """Devuelve todos los coches registrados."""
    resultado = await db.execute(select(Coche))
    return resultado.scalars().all()


@app.get("/coches/marca/{marca}", response_model=list[CocheResponse], tags=["Coches"])
async def coches_por_marca(marca: str, db: AsyncSession = Depends(get_db)):
    """Filtra los coches por marca (sin distinguir mayúsculas)."""
    resultado = await db.execute(
        select(Coche).where(Coche.marca.ilike(f"%{marca}%"))
    )
    coches = resultado.scalars().all()
    if not coches:
        raise HTTPException(status_code=404, detail=f"No hay coches de la marca '{marca}'")
    return coches


@app.get("/coches/{coche_id}", response_model=CocheResponse, tags=["Coches"])
async def obtener_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = resultado.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche


@app.delete("/coches/{coche_id}", tags=["Coches"])
async def eliminar_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = resultado.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    await db.delete(coche)
    return {"mensaje": f"Coche {coche.matricula} eliminado correctamente"}


# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------

@app.post("/servicios/", response_model=ServicioResponse, status_code=201, tags=["Servicios"])
async def crear_servicio(datos: ServicioCreate, db: AsyncSession = Depends(get_db)):
    """Registra un nuevo tipo de servicio (revisión, cambio de aceite, etc.)."""
    servicio = Servicio(**datos.dict())
    db.add(servicio)
    await db.flush()
    await db.refresh(servicio)
    return servicio


@app.get("/servicios/", response_model=list[ServicioResponse], tags=["Servicios"])
async def listar_servicios(db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Servicio))
    return resultado.scalars().all()


@app.get("/servicios/{servicio_id}", response_model=ServicioResponse, tags=["Servicios"])
async def obtener_servicio(servicio_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Servicio).where(Servicio.id == servicio_id))
    servicio = resultado.scalar_one_or_none()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


# ---------------------------------------------------------------------------
# Relación Coche ↔ Servicio
# ---------------------------------------------------------------------------

@app.post("/coches/{coche_id}/servicios/{servicio_id}", response_model=CocheResponse, tags=["Relaciones"])
async def asignar_servicio(coche_id: int, servicio_id: int, db: AsyncSession = Depends(get_db)):
    """Asigna un servicio a un coche. Devuelve 409 si ya estaba asignado."""
    res_coche = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = res_coche.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    res_servicio = await db.execute(select(Servicio).where(Servicio.id == servicio_id))
    servicio = res_servicio.scalar_one_or_none()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if servicio in coche.servicios:
        raise HTTPException(status_code=409, detail="Ese servicio ya está asignado a este coche")

    coche.servicios.append(servicio)
    await db.flush()
    await db.refresh(coche)
    return coche


@app.get("/coches/{coche_id}/servicios/", response_model=list[ServicioResponse], tags=["Relaciones"])
async def servicios_de_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    """Lista todos los servicios realizados a un coche concreto."""
    resultado = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = resultado.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche.servicios


# ---------------------------------------------------------------------------
# Estadísticas (endpoint exclusivo, no en el código de referencia)
# ---------------------------------------------------------------------------

@app.get("/estadisticas/", tags=["General"])
async def estadisticas(db: AsyncSession = Depends(get_db)):
    """Resumen del estado actual del taller: totales de clientes, coches y servicios."""
    total_clientes = await db.execute(select(func.count(Cliente.id)))
    total_coches = await db.execute(select(func.count(Coche.id)))
    total_servicios = await db.execute(select(func.count(Servicio.id)))

    return {
        "clientes_registrados": total_clientes.scalar(),
        "coches_registrados": total_coches.scalar(),
        "servicios_disponibles": total_servicios.scalar(),
    }
