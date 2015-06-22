from django.db import models

# Create your models here.

class Actividad(models.Model):
    titulo = models.TextField(blank=True)
    tipo = models.TextField(blank=True)
    precio = models.TextField(blank=True)
    fecha = models.DateField(blank=True)
    hora = models.TimeField(blank=True)
    larga_dur = models.TextField(blank=True)
    url = models.TextField(blank=True)
    fecha_usuario = models.DateField(blank=True)


class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    titulo_usuario = models.TextField(blank=True)
    actividades = models.ManyToManyField(Actividad, blank=True)

class FechaActualizada(models.Model):
    fecha = models.DateTimeField()
