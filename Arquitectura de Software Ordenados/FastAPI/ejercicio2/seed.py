"""
Carga datos de ejemplo en la base de datos.
Ejecutar con: python3 seed.py
El servidor no tiene que estar corriendo.
"""
import asyncio
from sqlalchemy import insert, text
from database import motor, Base
import models  # noqa


CLIENTES = [
    {"nombre": "Iván Zheng",               "telefono": "612345678", "email": "ivan@tallercoches.com"},
    {"nombre": "Javier Pozo González",      "telefono": "633112244", "email": "javier.pozo@gmail.com"},
    {"nombre": "Pablo Martín Gil",          "telefono": "655778899", "email": "pablo.martin@hotmail.com"},
    {"nombre": "Alfredo Sánchez Fuentes",   "telefono": "677001122", "email": "alfredo.sf@outlook.com"},
    {"nombre": "Julio San Juan Santander",  "telefono": "699334556", "email": "julio.sanjuan@gmail.com"},
    {"nombre": "Ricardo Trujillo Antiveros","telefono": "611990334", "email": "r.trujillo@icloud.com"},
    {"nombre": "Manuel Fas",                "telefono": "644223445", "email": "manuelfas@gmail.com"},
    {"nombre": "Celia Muñoz Gil",           "telefono": "622334455", "email": "celia.munoz@gmail.com"},
    {"nombre": "Eva Martín Rodríguez",      "telefono": "655667788", "email": "eva.martin@hotmail.com"},
    {"nombre": "Anna Herrero García",       "telefono": "688990011", "email": "anna.herrero@gmail.com"},
]

COCHES = [
    {"matricula": "4821PMV", "marca": "Porsche",     "modelo": "Cayenne Turbo S",       "anio": 2023, "cliente_id": 1},
    {"matricula": "7732BCD", "marca": "BMW",         "modelo": "M3 Competition",         "anio": 2022, "cliente_id": 2},
    {"matricula": "3345GHJ", "marca": "Audi",        "modelo": "R8 V10 Performance",     "anio": 2021, "cliente_id": 3},
    {"matricula": "5567KLM", "marca": "Mercedes",    "modelo": "AMG GT 63 S",            "anio": 2022, "cliente_id": 4},
    {"matricula": "1123NOP", "marca": "Lamborghini", "modelo": "Urus S",                 "anio": 2023, "cliente_id": 5},
    {"matricula": "8890QRS", "marca": "Ferrari",     "modelo": "Roma",                   "anio": 2022, "cliente_id": 6},
    {"matricula": "2234TUV", "marca": "Maserati",    "modelo": "Ghibli Trofeo",          "anio": 2021, "cliente_id": 7},
    {"matricula": "6678WXY", "marca": "Porsche",     "modelo": "911 Carrera 4S",         "anio": 2023, "cliente_id": 8},
    {"matricula": "9901ZAB", "marca": "Bentley",     "modelo": "Continental GT Speed",   "anio": 2022, "cliente_id": 9},
    {"matricula": "4456CDE", "marca": "Lexus",       "modelo": "LC 500",                 "anio": 2023, "cliente_id": 10},
]

SERVICIOS = [
    {"descripcion": "Revisión general",       "precio": 85.00,  "fecha": "2026-02-10"},
    {"descripcion": "Cambio de aceite",       "precio": 45.00,  "fecha": "2026-02-15"},
    {"descripcion": "Cambio de frenos",       "precio": 120.00, "fecha": "2026-03-01"},
    {"descripcion": "Cambio de neumáticos",   "precio": 200.00, "fecha": "2026-03-10"},
    {"descripcion": "Diagnóstico electrónico","precio": 60.00,  "fecha": "2026-04-05"},
    {"descripcion": "Reparación de embrague", "precio": 350.00, "fecha": "2026-04-20"},
]

# (coche_id, servicio_id, observaciones)
ASIGNACIONES = [
    (1, 1, "Todo en orden, próxima revisión en un año"),
    (1, 2, "Aceite 5W40 sintético Porsche original"),
    (2, 3, "Pastillas delanteras y traseras sustituidas"),
    (3, 1, ""),
    (4, 4, "Neumáticos Pirelli P Zero 265/35 R20"),
    (5, 2, "Aceite Lamborghini 0W40, filtro original"),
    (6, 5, "Fallo en sensor de O2, pendiente de presupuesto"),
    (7, 6, "Embrague muy desgastado, reparación urgente"),
    (8, 3, "Solo pastillas delanteras, traseras en buen estado"),
    (9, 1, "Revisión previa a pasar la ITV"),
]


async def seed():
    async with motor.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Vaciar tablas para evitar duplicados si se ejecuta varias veces
        await conn.execute(text("DELETE FROM coche_servicio"))
        await conn.execute(text("DELETE FROM coches"))
        await conn.execute(text("DELETE FROM servicios"))
        await conn.execute(text("DELETE FROM clientes"))

        await conn.execute(insert(models.Cliente), CLIENTES)
        await conn.execute(insert(models.Servicio), SERVICIOS)
        await conn.execute(insert(models.Coche), COCHES)
        await conn.execute(insert(models.asociacion_coche_servicio), [
            {"coche_id": c, "servicio_id": s, "observaciones": o}
            for c, s, o in ASIGNACIONES
        ])

    print("✓ 10 clientes, 10 coches, 6 servicios y 10 asignaciones cargados correctamente.")


if __name__ == "__main__":
    asyncio.run(seed())
