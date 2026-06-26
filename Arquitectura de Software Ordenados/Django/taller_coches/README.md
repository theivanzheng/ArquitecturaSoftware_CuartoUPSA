# Taller de coches

Proyecto Django para gestionar clientes, coches y servicios de un taller mecánico.

## Cómo arrancarlo

```bash
python3 manage.py migrate
python3 manage.py loaddata app_gestion_taller/fixtures/datos_ejemplo.json
python3 manage.py runserver
```

## Rutas principales

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/acerca-de/`
- `http://127.0.0.1:8000/contacto/`
- `http://127.0.0.1:8000/gestion/clientes/`
- `http://127.0.0.1:8000/gestion/clientes/1/`
- `http://127.0.0.1:8000/gestion/coches/1/servicios/`

## Formularios

Hay formularios para añadir clientes, coches, servicios y relaciones coche-servicio.

## Estructura

```text
taller_coches/
├── manage.py
├── taller_coches/
├── primera_app/
├── app_gestion_taller/
└── templates/
```
