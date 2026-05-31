from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite asíncrono con aiosqlite
# El archivo taller.db se crea automáticamente en la carpeta del proyecto
RUTA_BD = "sqlite+aiosqlite:///./taller.db"

# echo=False en producción para no saturar los logs
motor = create_async_engine(RUTA_BD, echo=True, future=True)

# expire_on_commit=False evita que los objetos queden inaccesibles
# después de hacer commit (importante con async)
SessionLocal = sessionmaker(
    bind=motor,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()
