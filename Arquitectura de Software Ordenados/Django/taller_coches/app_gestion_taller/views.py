import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Cliente, Coche, Servicio, CocheServicio


# --- Vistas GET ---

def lista_clientes(request):
    clientes = list(Cliente.objects.values('id', 'nombre', 'telefono', 'email'))
    return JsonResponse({'clientes': clientes})


def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    coches = list(cliente.coches.values('id', 'matricula', 'marca', 'modelo', 'anio'))
    return JsonResponse({
        'cliente': {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'email': cliente.email,
        },
        'coches': coches,
        'tiene_coches': len(coches) > 0,
    })


def servicios_coche(request, coche_id):
    try:
        coche = Coche.objects.get(pk=coche_id)
    except Coche.DoesNotExist:
        return JsonResponse({'error': 'Coche no encontrado'}, status=404)

    servicios = list(
        CocheServicio.objects
        .filter(coche=coche)
        .values('servicio__descripcion', 'servicio__precio', 'servicio__fecha', 'observaciones')
    )
    return JsonResponse({
        'coche': str(coche),
        'servicios': servicios,
        'tiene_servicios': len(servicios) > 0,
    })


# --- Vistas POST ---

@csrf_exempt
def registrar_cliente(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            telefono=data['telefono'],
            email=data['email'],
        )
        return JsonResponse({'mensaje': 'Cliente registrado con éxito', 'cliente_id': cliente.id}, status=201)
    except KeyError:
        return JsonResponse({'error': 'Datos incompletos. Se requieren: nombre, telefono, email'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def registrar_coche(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        cliente = Cliente.objects.get(pk=data['cliente_id'])
        coche = Coche.objects.create(
            matricula=data['matricula'],
            marca=data['marca'],
            modelo=data['modelo'],
            anio=data['anio'],
            cliente=cliente,
        )
        return JsonResponse({'mensaje': 'Coche registrado con éxito', 'coche_id': coche.id}, status=201)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Datos incompletos. Se requieren: matricula, marca, modelo, anio, cliente_id'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def registrar_servicio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        servicio = Servicio.objects.create(
            descripcion=data['descripcion'],
            precio=data['precio'],
            fecha=data['fecha'],
        )
        return JsonResponse({'mensaje': 'Servicio registrado con éxito', 'servicio_id': servicio.id}, status=201)
    except KeyError:
        return JsonResponse({'error': 'Datos incompletos. Se requieren: descripcion, precio, fecha'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def registrar_coche_servicio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        coche = Coche.objects.get(pk=data['coche_id'])
        servicio = Servicio.objects.get(pk=data['servicio_id'])
        cs, creado = CocheServicio.objects.get_or_create(
            coche=coche,
            servicio=servicio,
            defaults={'observaciones': data.get('observaciones', '')},
        )
        if not creado:
            return JsonResponse({'error': 'Ese servicio ya está registrado para ese coche'}, status=409)
        return JsonResponse({'mensaje': 'Servicio asignado al coche con éxito', 'id': cs.id}, status=201)
    except (Coche.DoesNotExist, Servicio.DoesNotExist) as e:
        return JsonResponse({'error': 'Coche o servicio no encontrado'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Datos incompletos. Se requieren: coche_id, servicio_id'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
