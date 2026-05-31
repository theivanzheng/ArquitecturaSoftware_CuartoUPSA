from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Abre una sesión de base de datos y la cierra al terminar la petición."""
    sesion = SessionLocal()
    try:
        yield sesion
        await sesion.commit()
    except Exception:
        await sesion.rollback()
        raise
    finally:
        await sesion.close()
