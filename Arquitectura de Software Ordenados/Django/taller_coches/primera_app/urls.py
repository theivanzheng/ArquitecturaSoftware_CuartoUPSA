from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),

    path('saludo/<str:nombre>/', views.saludo, name='saludo'),
    path('usuario/<int:id>/', views.obtener_usuario, name='obtener_usuario'),

    path('tipo/string/<str:valor>/', views.string_view, name='string_view'),
    path('tipo/integer/<int:valor>/', views.integer_view, name='integer_view'),
    path('tipo/slug/<slug:valor>/', views.slug_view, name='slug_view'),
    path('tipo/uuid/<uuid:valor>/', views.uuid_view, name='uuid_view'),
    path('tipo/path/<path:valor>/', views.path_view, name='path_view'),

    path('validar/', views.validar_datos, name='validar_datos'),

    path('solo-get/', views.solo_get, name='solo_get'),
    path('solo-post/', views.solo_post, name='solo_post'),
    path('solo-put/', views.solo_put, name='solo_put'),
    path('solo-patch/', views.solo_patch, name='solo_patch'),
    path('solo-delete/', views.solo_delete, name='solo_delete'),
]
