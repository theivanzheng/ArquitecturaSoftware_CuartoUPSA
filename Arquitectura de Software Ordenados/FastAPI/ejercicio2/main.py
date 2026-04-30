from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import engine, Base
from dependencies import get_db
from models import Cliente, Coche, Servicio, coche_servicio
from schemas import (
    ClienteCreate, ClienteResponse,
    CocheCreate, CocheResponse,
    ServicioCreate, ServicioResponse,
)

app = FastAPI(title="Taller de Coches — API con base de datos")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API del Taller de Coches con persistencia"}


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------

@app.post("/clientes/", response_model=ClienteResponse, status_code=201)
async def crear_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_db)):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    result = await db.execute(
        select(Cliente).options(selectinload(Cliente.coches)).where(Cliente.id == db_cliente.id)
    )
    return result.scalar_one()


@app.get("/clientes/", response_model=list[ClienteResponse])
async def listar_clientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Cliente).options(selectinload(Cliente.coches))
    )
    return result.scalars().all()


@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Cliente)
        .options(selectinload(Cliente.coches).selectinload(Coche.servicios))
        .where(Cliente.id == cliente_id)
    )
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@app.put("/clientes/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(cliente_id: int, datos: ClienteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for campo, valor in datos.dict().items():
        setattr(cliente, campo, valor)
    await db.commit()
    await db.refresh(cliente)
    return cliente


@app.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    await db.delete(cliente)
    await db.commit()
    return {"mensaje": f"Cliente {cliente_id} eliminado"}


# ---------------------------------------------------------------------------
# Coches
# ---------------------------------------------------------------------------

@app.post("/coches/", response_model=CocheResponse, status_code=201)
async def crear_coche(coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == coche.cliente_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db_coche = Coche(**coche.dict())
    db.add(db_coche)
    await db.commit()
    await db.refresh(db_coche)
    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios)).where(Coche.id == db_coche.id)
    )
    return result.scalar_one()


@app.get("/coches/", response_model=list[CocheResponse])
async def listar_coches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios))
    )
    return result.scalars().all()


@app.get("/coches/{coche_id}", response_model=CocheResponse)
async def obtener_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios)).where(Coche.id == coche_id)
    )
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche


@app.delete("/coches/{coche_id}")
async def eliminar_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    await db.delete(coche)
    await db.commit()
    return {"mensaje": f"Coche {coche_id} eliminado"}


# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------

@app.post("/servicios/", response_model=ServicioResponse, status_code=201)
async def crear_servicio(servicio: ServicioCreate, db: AsyncSession = Depends(get_db)):
    db_servicio = Servicio(**servicio.dict())
    db.add(db_servicio)
    await db.commit()
    await db.refresh(db_servicio)
    return db_servicio


@app.get("/servicios/", response_model=list[ServicioResponse])
async def listar_servicios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servicio))
    return result.scalars().all()


@app.get("/servicios/{servicio_id}", response_model=ServicioResponse)
async def obtener_servicio(servicio_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servicio).where(Servicio.id == servicio_id))
    servicio = result.scalar_one_or_none()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


# ---------------------------------------------------------------------------
# Relación Coche ↔ Servicio
# ---------------------------------------------------------------------------

@app.post("/coches/{coche_id}/servicios/{servicio_id}", response_model=CocheResponse)
async def asignar_servicio_a_coche(
    coche_id: int,
    servicio_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios)).where(Coche.id == coche_id)
    )
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    result = await db.execute(select(Servicio).where(Servicio.id == servicio_id))
    servicio = result.scalar_one_or_none()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if servicio in coche.servicios:
        raise HTTPException(status_code=409, detail="Este servicio ya está asignado a ese coche")

    coche.servicios.append(servicio)
    await db.commit()

    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios)).where(Coche.id == coche_id)
    )
    return result.scalar_one()


@app.get("/coches/{coche_id}/servicios/", response_model=list[ServicioResponse])
async def listar_servicios_de_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.servicios)).where(Coche.id == coche_id)
    )
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche.servicios
