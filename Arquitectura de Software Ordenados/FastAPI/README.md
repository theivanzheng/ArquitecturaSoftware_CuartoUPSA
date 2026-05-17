# FastAPI — Taller de Coches

Dos ejercicios progresivos con FastAPI adaptados a la gestión de un taller de coches.

---

## Ejercicio 1 — API básica en memoria

CRUD completo para Clientes, Coches y Servicios sin base de datos. Los datos viven en la memoria del servidor y se pierden al reiniciarlo.

### Arrancar

```bash
cd ejercicio1
pip install -r requirements.txt
uvicorn main:app --reload
```

### Endpoints

| Método | URL | Qué hace |
|--------|-----|----------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/clientes/` | Lista todos los clientes |
| GET | `/clientes/{id}` | Detalle de un cliente |
| POST | `/clientes/` | Crea un cliente |
| PUT | `/clientes/{id}` | Actualiza un cliente |
| DELETE | `/clientes/{id}` | Elimina un cliente |
| GET | `/coches/` | Lista todos los coches |
| POST | `/coches/` | Registra un coche (valida que el cliente exista) |
| PUT | `/coches/{id}` | Actualiza un coche |
| DELETE | `/coches/{id}` | Elimina un coche |
| GET | `/servicios/` | Lista todos los servicios |
| POST | `/servicios/` | Registra un servicio |
| PUT | `/servicios/{id}` | Actualiza un servicio |
| DELETE | `/servicios/{id}` | Elimina un servicio |

### Ejemplo rápido

```bash
# Crear un cliente
curl -X POST http://127.0.0.1:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Iván Zheng", "telefono": "612345678", "email": "ivan@taller.com"}'

# Registrar su Porsche
curl -X POST http://127.0.0.1:8000/coches/ \
  -H "Content-Type: application/json" \
  -d '{"matricula": "4821PMV", "marca": "Porsche", "modelo": "Cayenne Turbo S", "anio": 2023, "cliente_id": 1}'
```

---

## Ejercicio 2 — API con base de datos SQLite y relaciones

Misma API pero con persistencia real usando SQLAlchemy async + SQLite. Incluye la relación muchos a muchos entre Coches y Servicios.

### Arrancar

```bash
cd ejercicio2
pip install -r requirements.txt
python3 seed.py          # carga los datos de ejemplo
uvicorn main:app --reload
```

Las tablas se crean automáticamente al arrancar. El script `seed.py` carga 10 clientes con sus coches de alta gama, 6 servicios y 10 asignaciones. Se puede ejecutar varias veces sin duplicados.

### Endpoints adicionales respecto al Ejercicio 1

| Método | URL | Qué hace |
|--------|-----|----------|
| POST | `/coches/{id}/servicios/{id}` | Asigna un servicio a un coche |
| GET | `/coches/{id}/servicios/` | Lista los servicios de un coche |

### Documentación automática

FastAPI genera documentación interactiva en:

- `http://127.0.0.1:8000/docs` — Swagger UI (puedes probar los endpoints desde el navegador)
- `http://127.0.0.1:8000/redoc` — ReDoc

### Estructura de archivos

```
ejercicio2/
├── main.py          ← endpoints y arranque de la app
├── models.py        ← tablas SQLAlchemy (Cliente, Coche, Servicio)
├── schemas.py       ← validación Pydantic (request/response)
├── database.py      ← conexión a SQLite
├── dependencies.py  ← inyección de sesión de BD
├── init_db.py       ← script para crear tablas manualmente
└── requirements.txt
```
