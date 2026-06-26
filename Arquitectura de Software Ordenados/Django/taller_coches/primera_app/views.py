import json
import re
import uuid as uuid_lib

from django.http import HttpResponse, JsonResponse

def bienvenida(request):
    return HttpResponse("<h1>Bienvenido al Taller de Coches</h1><p>Tu taller de confianza.</p>")


def acerca_de(request):
    return HttpResponse("<h1>Acerca de nosotros</h1><p>Taller de coches con más de 20 años de experiencia.</p>")


def contacto(request):
    return HttpResponse("<h1>Contacto</h1><p>Llámanos al 600 000 000 o escríbenos a info@tallercoches.com</p>")
def saludo(request, nombre):
    return HttpResponse(f"<h1>Hola, {nombre}!</h1>")


def obtener_usuario(request, id):
    return HttpResponse(f"<p>Mostrando información del usuario con ID: {id}</p>")


def string_view(request, valor):
    return HttpResponse(f"String recibido: {valor}")


def integer_view(request, valor):
    return HttpResponse(f"Integer recibido: {valor}")


def slug_view(request, valor):
    return HttpResponse(f"Slug recibido: {valor}")


def uuid_view(request, valor):
    return HttpResponse(f"UUID recibido: {valor}")


def path_view(request, valor):
    return HttpResponse(f"Path recibido: {valor}")


def validar_datos(request):
    data = request.GET
    errores = {}

    string_valor = data.get('string')
    integer_valor = data.get('integer')
    slug_valor = data.get('slug')
    uuid_valor = data.get('uuid')
    path_valor = data.get('path')
    email_valor = data.get('email')

    if string_valor and not re.fullmatch(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', string_valor):
        errores['string'] = 'El valor debe contener solo letras y espacios'

    if integer_valor and not integer_valor.isdigit():
        errores['integer'] = 'El valor debe ser un número entero'

    if slug_valor and not re.fullmatch(r'^[a-zA-Z0-9_-]+$', slug_valor):
        errores['slug'] = 'El slug solo puede contener letras, números, guiones y guiones bajos'

    if uuid_valor:
        try:
            uuid_lib.UUID(uuid_valor, version=4)
        except ValueError:
            errores['uuid'] = 'UUID inválido'

    if path_valor and not re.fullmatch(r'^[\w\-/]+$', path_valor):
        errores['path'] = 'El path solo puede contener letras, números, guiones y barras'

    if email_valor and not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email_valor):
        errores['email'] = 'Correo electrónico inválido'

    if errores:
        return JsonResponse({'error': errores}, status=400)

    return JsonResponse({'mensaje': 'Todos los datos son válidos'})
def solo_get(request):
    if request.method == 'GET':
        return JsonResponse({'mensaje': 'Solicitud GET recibida correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def solo_post(request):
    if request.method == 'POST':
        return JsonResponse({'mensaje': 'Solicitud POST recibida correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def solo_put(request):
    if request.method == 'PUT':
        return JsonResponse({'mensaje': 'Solicitud PUT recibida correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def solo_patch(request):
    if request.method == 'PATCH':
        return JsonResponse({'mensaje': 'Solicitud PATCH recibida correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def solo_delete(request):
    if request.method == 'DELETE':
        return JsonResponse({'mensaje': 'Solicitud DELETE recibida correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
