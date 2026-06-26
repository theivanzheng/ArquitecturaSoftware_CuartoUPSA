from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('coches/<int:coche_id>/servicios/', views.servicios_coche, name='servicios_coche'),

    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('coches/nuevo/', views.registrar_coche, name='registrar_coche'),
    path('servicios/nuevo/', views.registrar_servicio, name='registrar_servicio'),
    path('coche-servicio/nuevo/', views.registrar_coche_servicio, name='registrar_coche_servicio'),

    path('formulario/cliente/', views.nuevo_cliente_tradicional, name='nuevo_cliente_tradicional'),

    path('form/cliente/', views.nuevo_cliente, name='nuevo_cliente'),
    path('form/coche/', views.nuevo_coche, name='nuevo_coche'),
    path('form/servicio/', views.nuevo_servicio, name='nuevo_servicio'),
    path('form/coche-servicio/', views.nuevo_coche_servicio, name='nuevo_coche_servicio'),
]
