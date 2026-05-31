# Taller de Coches — App de gestión

Una aplicación web para gestionar clientes, coches y servicios de un taller mecánico. Desarrollada con Django de forma incremental a lo largo del curso.

---

## Cómo arrancar la aplicación

Desde la carpeta `Django/taller_coches/`:

```bash
python3 manage.py migrate
python3 manage.py loaddata app_gestion_taller/fixtures/datos_ejemplo.json
python3 manage.py runserver
```

Abre el navegador en `http://127.0.0.1:8000/` y ya está con datos de ejemplo cargados.

---

## Qué puedes hacer

### Página de inicio y presentación

Tres páginas sencillas para ver que el enrutamiento funciona:

- `http://127.0.0.1:8000/` — portada del taller
- `http://127.0.0.1:8000/acerca-de/` — quiénes somos
- `http://127.0.0.1:8000/contacto/` — datos de contacto

---

### URLs con parámetros

Puedes pasar datos directamente en la URL:

```
http://127.0.0.1:8000/saludo/Carlos/
→ Hola, Carlos!

http://127.0.0.1:8000/usuario/7/
→ Mostrando información del usuario con ID: 7
```

También hay un endpoint que valida los datos que le pases:

```
http://127.0.0.1:8000/validar/?string=Carlos&integer=42&email=carlos@taller.com
→ {"mensaje": "Todos los datos son válidos"}

http://127.0.0.1:8000/validar/?email=esto-no-es-un-email
→ {"error": {"email": "Correo electrónico inválido"}}
```

---

### Ver clientes y coches

Para que haya algo que ver, primero hay que meter datos. La forma más cómoda es desde el panel de administración:

```bash
python3 manage.py createsuperuser
```

Entra en `http://127.0.0.1:8000/admin/` con el usuario que acabas de crear y añade, en este orden:

1. Un **cliente** — por ejemplo: *Iván Zheng, 612 345 678, ivan@tallercoches.com*
2. Un **coche** asignado a ese cliente — por ejemplo: *Mercedes C220, matrícula 4821 PMV, año 2019*
3. Un **servicio** — por ejemplo: *Revisión general, 85.00 €, fecha de hoy*
4. Un **CocheServicio** que enlace el Mercedes con la revisión

Puedes meter tantos clientes como quieras para que la lista se vea bien. Algunos ejemplos:

| Nombre | Teléfono | Email |
|--------|----------|-------|
| Iván Zheng | 612 345 678 | ivan@tallercoches.com |
| Javier Pozo González | 633 112 244 | javier.pozo@gmail.com |
| Pablo Martín Gil | 655 778 899 | pablo.martin@hotmail.com |
| Alfredo Sánchez Fuentes | 677 001 122 | alfredo.sf@outlook.com |
| Julio San Juan Santander | 699 334 556 | julio.sanjuan@gmail.com |
| Ricardo Trujillo Antiveros | 611 990 334 | r.trujillo@icloud.com |
| Manuel Fas | 644 223 445 | manuelfas@gmail.com |

Una vez hecho eso, estas páginas ya muestran datos reales:

```
http://127.0.0.1:8000/taller/clientes/
→ Tabla con todos los clientes del taller

http://127.0.0.1:8000/taller/clientes/1/
→ Ficha de Iván Zheng con su Mercedes C220

http://127.0.0.1:8000/taller/coches/1/servicios/
→ La revisión general del Mercedes C220
```

---

### Registrar datos desde código (API JSON)

Si prefieres añadir datos sin usar el admin, puedes hacerlo con peticiones POST. Abre una terminal con el servidor corriendo y ejecuta:

```bash
# Añadir a Ricardo Trujillo Antiveros
curl -X POST http://127.0.0.1:8000/taller/clientes/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ricardo Trujillo Antiveros", "telefono": "611990334", "email": "r.trujillo@icloud.com"}'

# Añadir su coche (usa el cliente_id que te devuelve el paso anterior)
curl -X POST http://127.0.0.1:8000/taller/coches/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"matricula": "7732 BCD", "marca": "BMW", "modelo": "Serie 3", "anio": 2021, "cliente_id": 1}'

# Añadir un servicio
curl -X POST http://127.0.0.1:8000/taller/servicios/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"descripcion": "Cambio de frenos", "precio": "120.00", "fecha": "2026-05-31"}'

# Asignar ese servicio al coche de Ricardo
curl -X POST http://127.0.0.1:8000/taller/coche-servicio/nuevo/ \
  -H "Content-Type: application/json" \
  -d '{"coche_id": 1, "servicio_id": 1, "observaciones": "Pastillas delantera y trasera"}'
```

---

### Formularios web

Para crear datos desde el navegador, sin tocar la terminal:

| Qué quieres hacer | URL |
|--------------------|-----|
| Añadir un cliente (formulario básico) | `http://127.0.0.1:8000/taller/formulario/cliente/` |
| Añadir un cliente (formulario completo) | `http://127.0.0.1:8000/taller/form/cliente/` |
| Añadir un coche | `http://127.0.0.1:8000/taller/form/coche/` |
| Añadir un servicio | `http://127.0.0.1:8000/taller/form/servicio/` |
| Asignar servicio a un coche | `http://127.0.0.1:8000/taller/form/coche-servicio/` |

Si rellenas mal algún campo (por ejemplo, un email sin @), el formulario te avisa sin borrar lo que habías escrito.

---

## Estructura del proyecto

```
taller_coches/
├── manage.py
├── taller_coches/          ← configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── primera_app/            ← vistas básicas y ejercicios de URL
│   ├── views.py
│   └── urls.py
├── app_gestion_taller/     ← lógica principal del taller
│   ├── models.py           ← Cliente, Coche, Servicio, CocheServicio
│   ├── views.py            ← vistas HTML y endpoints JSON
│   ├── forms.py            ← formularios
│   └── urls.py
└── templates/
    ├── base.html           ← plantilla base (todas las páginas la usan)
    └── app_gestion_taller/
        ├── lista_clientes.html
        ├── detalle_cliente.html
        ├── servicios_coche.html
        ├── form_tradicional.html
        └── form_modelo.html
```
