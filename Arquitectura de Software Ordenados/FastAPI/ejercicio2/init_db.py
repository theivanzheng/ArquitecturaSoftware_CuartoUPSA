import asyncio
from database import engine, Base
import models  # noqa: importar modelos para que Base los registre


async def crear_tablas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    asyncio.run(crear_tablas())
