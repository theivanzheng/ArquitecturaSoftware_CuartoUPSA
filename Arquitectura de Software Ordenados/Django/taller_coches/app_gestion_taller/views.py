from django.http import JsonResponse
from .models import Cliente, Coche, Servicio, CocheServicio


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
