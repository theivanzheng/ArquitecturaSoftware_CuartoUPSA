# Arquitectura del Software — Prácticas

Repositorio de prácticas de la asignatura **Arquitectura del Software** (4º curso).

## Estructura

```
arquitectura-software/
├── Django/          # Prácticas con Django (P1–P6)
│   └── taller_coches/   # Proyecto Django: gestión de taller de coches
└── FastAPI/         # Prácticas con FastAPI
```

## Django — Taller de Coches

Aplicación de gestión de un taller de coches desarrollada de forma incremental a lo largo de las prácticas.

### Modelos
- **Cliente** — nombre, teléfono, email
- **Coche** — matrícula, marca, modelo, año, FK a Cliente
- **Servicio** — descripción, precio, fecha
- **CocheServicio** — relación M:M entre Coche y Servicio

### Prácticas
| Práctica | Contenido |
|----------|-----------|
| P1 | Configuración del proyecto, primera app, vistas básicas |
| P2 | URLs con parámetros, validación, métodos HTTP |
| P3 | Modelos y base de datos (ORM Django) |
| P4 | Endpoints REST (GET/POST) con JsonResponse |
| P5 | Plantillas HTML con herencia (base.html) |
| P6 | Formularios tradicionales y ModelForms |

### Puesta en marcha

```bash
cd Django/taller_coches
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install django==5.1.6
python manage.py migrate
python manage.py runserver
```
