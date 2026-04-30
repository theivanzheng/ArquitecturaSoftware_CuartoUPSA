"""
Script auxiliar para crear las tablas manualmente.
Normalmente no hace falta ejecutarlo: el servidor las crea al arrancar.
Útil para inicializar la BD antes de lanzar tests o migraciones.
"""
import asyncio
from database import motor, Base
import models  # noqa: necesario para que Base registre los modelos


async def inicializar():
    async with motor.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    asyncio.run(inicializar())
