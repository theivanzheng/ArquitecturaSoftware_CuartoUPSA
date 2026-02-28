from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Coche(models.Model):
    matricula = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='coches')

    class Meta:
        verbose_name = 'Coche'
        verbose_name_plural = 'Coches'
        ordering = ['matricula']

    def __str__(self):
        return f"{self.matricula} — {self.marca} {self.modelo}"


class Servicio(models.Model):
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.descripcion} ({self.fecha})"


class CocheServicio(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, related_name='coche_servicios')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='coche_servicios')
    observaciones = models.TextField(blank=True, null=True, default='')

    class Meta:
        verbose_name = 'Servicio de coche'
        verbose_name_plural = 'Servicios de coches'
        unique_together = ('coche', 'servicio')

    def __str__(self):
        return f"{self.coche} — {self.servicio}"
