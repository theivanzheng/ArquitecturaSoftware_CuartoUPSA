from django.http import HttpResponse


def bienvenida(request):
    return HttpResponse("<h1>Bienvenido al Taller de Coches</h1><p>Tu taller de confianza.</p>")


def acerca_de(request):
    return HttpResponse("<h1>Acerca de nosotros</h1><p>Taller de coches con más de 20 años de experiencia.</p>")


def contacto(request):
    return HttpResponse("<h1>Contacto</h1><p>Llámanos al 600 000 000 o escríbenos a info@tallercoches.com</p>")
