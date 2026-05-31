# Arquitectura del Software — Prácticas Django

**Alumno:** Ivan Zheng  
**Asignatura:** Arquitectura del Software — 4º curso  
**Repositorio:** `arquitectura-software`

---

## Estructura del repositorio

```
arquitectura-software/
├── Django/
│   └── taller_coches/       ← Proyecto Django (P1–P6, incremental)
└── FastAPI/                  ← Prácticas FastAPI (próximamente)
```

## Ramas

| Rama | Contenido |
|------|-----------|
| `main` | Código estable. Merge final del 31 de mayo. |
| `develop` | Integración de todas las prácticas. |
| `feature/practica1-primera-app` | P1: proyecto + primera app |
| `feature/practica2-url-parametros` | P2: parámetros en URL |
| `feature/practica3-modelos-bd` | P3: modelos y base de datos |
| `feature/practica4-endpoints-post` | P4: endpoints POST |
| `feature/practica5-plantillas` | P5: plantillas HTML |
| `feature/practica6-formularios` | P6: formularios |

---

## Puesta en marcha

```bash
cd Django/taller_coches
python3 manage.py migrate
python3 manage.py runserver
```

El servidor arranca en `http://127.0.0.1:8000/`

Para crear datos de prueba desde el panel de administración:

```bash
python3 manage.py createsuperuser
# Acceder en: http://127.0.0.1:8000/admin/
```

---

## Guía de corrección por práctica

### Práctica 1 — Configuración del proyecto y primera app
**Commit:** 12 de febrero · Rama: `feature/practica1-primera-app`

Proyecto Django `taller_coches` con la app `primera_app` registrada en `INSTALLED_APPS`.  
Cada URL devuelve una respuesta `HttpResponse` simple.

| URL | Respuesta esperada |
|-----|--------------------|
| `http://127.0.0.1:8000/` | Bienvenida al taller |
| `http://127.0.0.1:8000/acerca-de/` | Texto sobre el taller |
| `http://127.0.0.1:8000/contacto/` | Teléfono y email de contacto |

Archivos clave:
- `primera_app/views.py` — tres vistas básicas
- `primera_app/urls.py` — tres rutas
- `taller_coches/urls.py` — include de primera_app
- `taller_coches/settings.py` — app registrada, idioma `es-es`, zona `Europe/Madrid`

---

### Práctica 2 — URLs con parámetros
**Commit:** 19 de febrero · Rama: `feature/practica2-url-parametros`

Parámetros en URL con los cinco convertidores de Django (`str`, `int`, `slug`, `uuid`, `path`).  
Validación de datos GET con expresiones regulares. Restricción de métodos HTTP.

| URL | Método | Respuesta esperada |
|-----|--------|--------------------|
| `/saludo/Ivan/` | GET | `Hola, Ivan!` |
| `/usuario/5/` | GET | `usuario con ID: 5` |
| `/tipo/integer/42/` | GET | `Integer recibido: 42` |
| `/tipo/slug/hola-mundo/` | GET | `Slug recibido: hola-mundo` |
| `/validar/?string=Hola&integer=42&email=a@b.com` | GET | `{"mensaje": "Todos los datos son válidos"}` |
| `/validar/?integer=abc` | GET | `{"error": {"integer": "..."}}` (400) |
| `/solo-get/` | GET | `{"mensaje": "Solicitud GET recibida correctamente"}` |
| `/solo-post/` | GET | `{"error": "Método no permitido"}` (405) |

Archivos clave:
- `primera_app/views.py` — vistas con parámetros, validación y métodos
- `primera_app/urls.py` — rutas con convertidores de tipo

---

### Práctica 3 — Modelos y base de datos
**Commit:** 26 de febrero · Rama: `feature/practica3-modelos-bd`

App `app_gestion_taller` con cuatro modelos y sus relaciones.

**Modelos:**
- `Cliente` — nombre, teléfono, email (único)
- `Coche` — matrícula (única), marca, modelo, año · FK → Cliente
- `Servicio` — descripción, precio, fecha
- `CocheServicio` — FK → Coche + FK → Servicio · campo observaciones · unique\_together

Archivos clave:
- `app_gestion_taller/models.py` — cuatro modelos con Meta, `__str__` y ordering
- `app_gestion_taller/migrations/0001_initial.py` — migración generada
- `app_gestion_taller/admin.py` — registro en el panel admin con `list_display`
- `taller_coches/settings.py` — app añadida a `INSTALLED_APPS`

Para verificar en el admin: `http://127.0.0.1:8000/admin/` (requiere superusuario).

---

### Práctica 4 — Endpoints POST
**Commit:** 12 de marzo · Rama: `feature/practica4-endpoints-post`

Endpoints que reciben JSON por POST y crean registros en la base de datos.

```bash
# Registrar un cliente
curl -X POST http://127.0.0.1:8000/taller/clientes/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ana García", "telefono": "600000000", "email": "ana@test.com"}'

# Registrar un coche (usar el cliente_id devuelto arriba)
curl -X POST http://127.0.0.1:8000/taller/coches/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"matricula": "1234ABC", "marca": "Seat", "modelo": "Ibiza", "anio": 2020, "cliente_id": 1}'

# Registrar un servicio
curl -X POST http://127.0.0.1:8000/taller/servicios/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"descripcion": "Cambio de aceite", "precio": "45.00", "fecha": "2026-03-12"}'

# Asignar servicio a coche
curl -X POST http://127.0.0.1:8000/taller/coche-servicio/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"coche_id": 1, "servicio_id": 1, "observaciones": "Aceite 5W40"}'
```

Comportamiento ante errores:
- Datos incompletos → 400
- Recurso no encontrado → 404
- Método no POST → 405
- Servicio ya asignado a ese coche → 409

Archivos clave:
- `app_gestion_taller/views.py` — funciones `registrar_*` con `@csrf_exempt`
- `app_gestion_taller/urls.py` — rutas POST bajo `/taller/`

---

### Práctica 5 — Plantillas HTML
**Commit:** 12 de marzo · Rama: `feature/practica5-plantillas`

Las vistas GET pasan de devolver JSON a renderizar plantillas HTML.  
Todas las plantillas heredan de `base.html` (herencia de plantillas).

> **Nota:** crear datos primero desde el admin o via POST (P4) para ver contenido.

| URL | Plantilla | Qué muestra |
|-----|-----------|-------------|
| `/taller/clientes/` | `lista_clientes.html` | Tabla con todos los clientes |
| `/taller/clientes/1/` | `detalle_cliente.html` | Datos del cliente + tabla de sus coches |
| `/taller/coches/1/servicios/` | `servicios_coche.html` | Servicios realizados a ese coche |

Si no hay datos, cada plantilla muestra un aviso informativo en lugar de tabla vacía.

Archivos clave:
- `templates/base.html` — layout con header, nav, estilos y bloque `contenido`
- `templates/app_gestion_taller/*.html` — tres plantillas que extienden base.html
- `taller_coches/settings.py` — `DIRS: [BASE_DIR / 'templates']`

---

### Práctica 6 — Formularios
**Commit:** 19 de marzo · Rama: `feature/practica6-formularios`

Dos tipos de formularios implementados y diferenciados claramente.

**Formulario tradicional (`forms.Form`):**
- URL: `http://127.0.0.1:8000/taller/formulario/cliente/`
- Validación manual: teléfono solo dígitos, email no duplicado
- Mensaje de error inline bajo cada campo

**ModelForms (`forms.ModelForm`):**
- `http://127.0.0.1:8000/taller/form/cliente/`
- `http://127.0.0.1:8000/taller/form/coche/`
- `http://127.0.0.1:8000/taller/form/servicio/`
- `http://127.0.0.1:8000/taller/form/coche-servicio/`

Todos los formularios:
- Heredan de `base.html`
- Usan `{% csrf_token %}`
- Muestran errores de validación en rojo
- Redirigen a `/taller/clientes/` tras guardar correctamente

Archivos clave:
- `app_gestion_taller/forms.py` — `ClienteFormTradicional` + cuatro ModelForms
- `templates/app_gestion_taller/form_tradicional.html`
- `templates/app_gestion_taller/form_modelo.html`

---

## Resumen de URLs

```
/                                   ← P1: bienvenida
/acerca-de/                         ← P1
/contacto/                          ← P1
/saludo/<str:nombre>/               ← P2
/usuario/<int:id>/                  ← P2
/tipo/string/<str:valor>/           ← P2
/tipo/integer/<int:valor>/          ← P2
/tipo/slug/<slug:valor>/            ← P2
/tipo/uuid/<uuid:valor>/            ← P2
/tipo/path/<path:valor>/            ← P2
/validar/                           ← P2: validación GET
/solo-get/ /solo-post/ ...          ← P2: restricción de métodos

/taller/clientes/                   ← P3/P5: lista (HTML)
/taller/clientes/<id>/              ← P3/P5: detalle (HTML)
/taller/coches/<id>/servicios/      ← P3/P5: servicios (HTML)
/taller/clientes/nuevo/             ← P4: POST JSON
/taller/coches/nuevo/               ← P4: POST JSON
/taller/servicios/nuevo/            ← P4: POST JSON
/taller/coche-servicio/nuevo/       ← P4: POST JSON

/taller/formulario/cliente/         ← P6: forms.Form tradicional
/taller/form/cliente/               ← P6: ModelForm
/taller/form/coche/                 ← P6: ModelForm
/taller/form/servicio/              ← P6: ModelForm
/taller/form/coche-servicio/        ← P6: ModelForm

/admin/                             ← Panel de administración Django
```
