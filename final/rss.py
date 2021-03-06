# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from final.models import Usuario, Actividad
import datetime

class Usuarios_RSS(Feed):


    def get_object(self, request, recurso):
        print recurso
        return recurso

    def title(self, obj):
        return 'Estas son las actividades de ' + str(obj)

    def description(self, obj):
        return str(obj) + " ha añadido estas de momento"

    def link(self, obj):
        return "/"

    def item_title(self, item):
        return item.titulo

    def item_description(self):
        return "Disfrute con esta actividad"

    def item_link(self):
        return "/"

    def items(self, obj):
        print obj
        usuario = Usuario.objects.get(nombre=obj)
        actividades_selecc = usuario.actividades.all()
        return actividades_selecc


class RSS_Principal(Feed):


    def title(self, obj):
        return "Actividades Culturales en Madrid"
    
    def description(self, obj):
        return "Estas son las 10 más próximas"

    def link(self, obj):
        return "/"

    def item_title(self, item):
        return item.titulo

    def item_description(self):
        return "Más información en la página principal"

    def item_link(self):
        return "/"


    def items(self, obj):
        hoy = datetime.datetime.today()
        fecha_final = datetime.date(2025, 6, 14)
        hora_actual = datetime.datetime.now()
        hora_final = datetime.time(23, 59, 00)
        actividades = Actividad.objects.filter(fecha__range=(hoy, fecha_final))
        actividades = actividades.filter(hora__range=(hora_actual, hora_final)).order_by('fecha', 'hora')[0:10]
        return actividades

