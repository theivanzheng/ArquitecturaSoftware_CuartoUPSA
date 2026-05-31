import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Cliente, Coche, Servicio, CocheServicio
from .forms import ClienteFormTradicional, ClienteForm, CocheForm, ServicioForm, CocheServicioForm


# --- Vistas GET (renderizan plantillas HTML) ---

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/lista_clientes.html', {'clientes': clientes})


def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    coches = cliente.coches.all()
    return render(request, 'app_gestion_taller/detalle_cliente.html', {
        'cliente': cliente,
        'coches': coches,
    })


def servicios_coche(request, coche_id):
    coche = get_object_or_404(Coche, pk=coche_id)
    servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
    return render(request, 'app_gestion_taller/servicios_coche.html', {
        'coche': coche,
        'servicios': servicios,
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


# --- P6: Formulario tradicional (sin modelo) ---

def nuevo_cliente_tradicional(request):
    if request.method == 'POST':
        form = ClienteFormTradicional(request.POST)
        if form.is_valid():
            Cliente.objects.create(
                nombre=form.cleaned_data['nombre'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
            )
            return redirect('lista_clientes')
    else:
        form = ClienteFormTradicional()
    return render(request, 'app_gestion_taller/form_tradicional.html', {
        'form': form,
        'titulo': 'Nuevo cliente (formulario tradicional)',
        'accion': 'Registrar cliente',
    })


# --- P6: ModelForms ---

def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'app_gestion_taller/form_modelo.html', {
        'form': form,
        'titulo': 'Nuevo cliente',
        'accion': 'Registrar cliente',
    })


def nuevo_coche(request):
    if request.method == 'POST':
        form = CocheForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = CocheForm()
    return render(request, 'app_gestion_taller/form_modelo.html', {
        'form': form,
        'titulo': 'Nuevo coche',
        'accion': 'Registrar coche',
    })


def nuevo_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ServicioForm()
    return render(request, 'app_gestion_taller/form_modelo.html', {
        'form': form,
        'titulo': 'Nuevo servicio',
        'accion': 'Registrar servicio',
    })


def nuevo_coche_servicio(request):
    if request.method == 'POST':
        form = CocheServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = CocheServicioForm()
    return render(request, 'app_gestion_taller/form_modelo.html', {
        'form': form,
        'titulo': 'Asignar servicio a coche',
        'accion': 'Asignar servicio',
    })
