#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from xmlparser import getNoticias
import datetime
from models import Actividad, Usuario
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.loader import get_template
from django.template import Context
import urllib2
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def login(): #Formulario para registrarse o entrar en la pagina, aparece en todos los recursos de la misma
    salida = '<form action="" method="POST">'
    salida += 'Nombre de usuario<br><input type="text" name="Usuario"><br>'
    salida += 'Password<br><input type="password" name="Password">'
    salida += '<br><input type="submit" value="Entrar"> '
    salida += '</form>'
    return salida

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def pie():
    salida = 'Fernando Rioja Checa. All rights reserved'
    return salida

def nuevo_usuario(request): 
    log = '<form action="" method="POST">'
    log += 'Nombre de usuario<br><input type="text" name="Usuario"><br>'
    log += 'Password<br><input type="password" name="Password">'
    log += '<br><input type="submit" value="Registrarme">'
    log += '</form>'
    inicio = '<a href="/">Inicio</a>'
    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        lista = User.objects.all()
        for fila in lista:
            if fila.username == usuario:
                error = ""
                error += '<span>Error.</span><br>'
                error += 'El nombre de usuario ya esta usado. Pruebe otro.'
                plantilla = get_template('index.html')
                Contexto = Context({'loggin': log, 'inicio': inicio, 'error': error})
                renderizado = plantilla.render(Contexto)
                return HttpResponse(renderizado)

        user = User.objects.create_user(usuario, usuario + '@ejemplo.com', password)
        user.save()
        user = Usuario(nombre=usuario)
        user.save()
        return HttpResponseRedirect('/')
    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'inicio': inicio})
    renderizado = plantilla.render(Contexto)
    return HttpResponse(renderizado)
    

def pagina_principal(request):
    cuerpo = ""
    log = ""
    titulo = "Actividades mas proximas"
    error = ""
    personales = "<br>Paginas personales"
    cuerpo_user = ""
    rss = ""
    rss = '<a href="/root/rss"> RSS</a>'
    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username + '!'
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()
        
    hoy = datetime.datetime.today()
    fecha_final = datetime.date(2025, 6, 14)
    hora_actual = datetime.datetime.now()
    hora_final = datetime.time(23, 59, 00)
    actividades = Actividad.objects.filter(fecha__range=(hoy, fecha_final))
    actividades = actividades.filter(hora__range=(hora_actual, hora_final)).order_by('fecha', 'hora')[0:10]
    for actividad in actividades:
        cuerpo += '<ul><li><a href="/actividades/' + str(actividad.id) + '">' + actividad.titulo + '</a><ul><li>' + 'Fecha: ' + str(actividad.fecha) + ', Hora: ' + str(actividad.hora) + '</li></ul></li></ul>'
    
    Todos = Usuario.objects.all()
    for usuario in Todos:
        if len(usuario.actividades.values()) == 0:
            print "No tienes nada"
        else:
            titulo_personal = usuario.titulo_usuario
            if titulo_personal == "":
                titulo_personal = 'Pagina de ' + usuario.nombre
                
            cuerpo_user += '<ul><li><a href="' + usuario.nombre + '">' + titulo_personal
#Ahora vamos a guardar el usuario, cuando se registre en la página principal

    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            error += '<span>Error.</span> Datos no válidos<br>'
            plantilla = get_template('index.html')
            Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error,'personales': personales, 'cuerpo_user': cuerpo_user, 'pie': pie, 'rss': rss})
            renderizado = plantilla.render(Contexto)
            return HttpResponse(renderizado)

    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'personales': personales, 'cuerpo_user': cuerpo_user, 'pie': pie, 'rss': rss})
    renderizado = plantilla.render(Contexto)    
    return HttpResponse(renderizado)


def actividad_concreta(request, recurso):
    actividad = Actividad.objects.get(id=recurso)
    cuerpo = ""
    log = ""
    error = ""
    inicio = '<a href="/">INICIO</a>'
    titulo = actividad.titulo
    cuerpo += '<ul><li>Tipo de evento: ' + actividad.tipo + '<br></li>'
    cuerpo += '<li>Precio: ' + actividad.precio + '</li>'
    cuerpo += '<li>Fecha: ' + str(actividad.fecha) + ', Hora: ' + str(actividad.hora) + '</li>'
    cuerpo += u'<li>Evento de larga duración: ' + actividad.larga_dur + '</li>'
    
    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username + '!'
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()

    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_activate:
            auth.login(request, user)
            return HttpResponseRedirect("/actividades/" + str(recurso))
        else:
            error += '<span>Error.</span> Datos incorrectos<br>'
            plantilla = get_template('index.html')
            Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'pie': pie()}) 
            renderizado = plantilla.render(Contexto)
            return HttpResponse(renderizado)

    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'inicio': inicio, 'pie': pie()})
    renderizado = plantilla.render(Contexto)
    return HttpResponse(renderizado)

def lista_actividades(request):
    titulo = "Estas son las actividades propuestas"
    cuerpo = ""
    log = ""
    error = ""
    refrescar = ""
    inicio = '<a href="/">Inicio</a>'
    busqueda = ""
    busqueda += '<label><strong>Busqueda</strong></label> <br/>'
    busqueda += '<form action="" method="POST">'
    busqueda += '<select name="buscar"><option value="" selected="selected">- selecciona -</option>'
    busqueda += '<option value="fecha">Por fecha</option>'
    busqueda += u'<option value="titulo">Por título</option>'
    busqueda += '<option value="precio">Por precio</option></select>'
    busqueda += '<br><input type="submit" value="Buscar">'
    busqueda += '</form>'
    actividades = Actividad.objects.all()
    if request.user.is_authenticated():
        refrescar += '<label><strong>Actualizar Actividades</strong></label>'
        refrescar += '<form action="" method="POST" >'
        refrescar += '<input type="submit" name="update" value="Actualizar">'
        refrescar += '</form>'
        log += 'Hola ' + request.user.username
        log += '<br><a href="/logout">Salir</a>'
        cuerpo += str(actividades.count()) + ' Actividades<br>'
        for fila in actividades:
            cuerpo += '<form action="" method="POST" >'
            cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
            cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
            cuerpo += '</li></ul>'
        cuerpo += u'<center><input type="submit" value="Añadir"></center></form>'
    else:
        log += login()
        for fila in actividades:
            cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'

    if request.method == 'POST':
        cuerpo = ""
        datos = request.body
        name = datos.split('=')[0]

        if name == 'seleccion': #1
            if datos.find('&') == -1:
                numero = datos.split('=')[1]
                hoy = datetime.datetime.now() + datetime.timedelta(hours=2)
                actividad = Actividad.objects.get(id=numero)
                actividad.fecha_usuario = hoy
                actividad.save()
                usuario = Usuario.objects.get(nombre=request.user.username)
                usuario.actividades.add(actividad)
                cuerpo += str(actividades.count()) + ' Actividades<br>'
                for fila in actividades:
                    cuerpo += '<form action="" method="POST" >'
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                    cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                    cuerpo += '</li></ul>'
                cuerpo += '<center><input type="submit" value="Elegir"></center></form>'        

            else: #Mas de una
                datos = datos.split('&')
                contador = 0
                while (contador < len(datos)):
                    datos[contador] = datos[contador].split('=')[1]
                    contador = contador + 1
                contador = 0
                while (contador < len(datos)):
                    hoy = datetime.datetime.now() + datetime.timedelta(hours=2)
                    actividad = Actividad.objects.get(id=datos[contador])
                    actividad.fecha_usuario = hoy
                    actividad.save()
                    usuario = Usuario.objects.get(nombre=request.user.username)
                    usuario.actividades.add(actividad)
                    contador = contador + 1

                cuerpo += str(actividades.count()) + ' Actividades<br>'
                for fila in actividades:
                    cuerpo += '<form action="" method="POST" >'
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                    cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                    cuerpo += '</li></ul>'
                cuerpo += u'<center><input type="submit" value="Añadir"></center></form>'

        elif name == 'buscar':
            if request.POST['buscar'] == 'fecha':
                actividades = actividades.order_by('fecha')
                if request.user.is_authenticated():
                    cuerpo += str(actividades.count()) + ' Actividades<br>'
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '<ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul>'
                        cuerpo += '</li></ul>'
                    cuerpo += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">'
                        cuerpo += fila.titulo + '</a><ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul></li></ul>' 
                
            elif request.POST['buscar'] == 'precio':
                actividades = actividades.order_by('precio')
                if request.user.is_authenticated():
                    cuerpo += str(actividades.count()) + ' Actividades<br>'
                    cuerpo += fila.titulo + '</a><ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul></li></ul>'
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '<ul><li>' + 'Precio: ' + fila.precio + '</li></ul>'
                        cuerpo += '</li></ul>'
                    cuerpo += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">'
                        cuerpo += fila.titulo + '</a><ul><li>' + 'Precio: ' + fila.precio + '</li></ul></li></ul>'

            elif request.POST['buscar'] == 'titulo':
                actividades = actividades.order_by('titulo')
                if request.user.is_authenticated():
                    cuerpo += str(actividades.count()) + ' Actividades<br>'
                    cuerpo += fila.titulo + '<a><ul><li>' + 'Fecha: ' + str(fila.fecha) + '</li></ul></li></ul>'
                    for fila in actividades:
                        cuerpo += '<form action="" method="POST" >'
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a>'
                        cuerpo += '<input type="checkbox" name="seleccion" value="' + str(fila.id) + '">'
                        cuerpo += '</li></ul>'
                    cuerpo += u'<center><input type="submit" value="Añadir"></center></form>'
                else:
                    for fila in actividades:
                        cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">'
                        cuerpo += fila.titulo + '</a></li></ul>'
            elif request.POST['buscar'] == "":
                for fila in actividades:
                    cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'

        else:
            for fila in actividades:
                cuerpo += '<ul><li><a href="/actividades/' + str(fila.id) + '">' + fila.titulo + '</a></li></ul>'
            usuario = request.POST['Usuario']
            contrasena = request.POST['Password']
            user = auth.authenticate(username=usuario, password=contrasena)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/todas")
            else:
                error += '<span>Error.</span> Datos incorrectos<br>'
                plantilla = get_template('index.html')
                Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'refrescar': refrescar, 'error': error, 'pie': pie()})
                renderizado = plantilla.render(Contexto)
                return HttpResponse(renderizado)

        plantilla = get_template('index.html')
        Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'refrescar': refrescar, 'pie': pie()})
        renderizado = plantilla.render(Contexto)
        return HttpResponse(renderizado)

    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'busqueda': busqueda, 'inicio': inicio, 'refrescar': refrescar, 'pie': pie()})
    renderizado = plantilla.render(Contexto)
    return HttpResponse(renderizado)


def pagina_personal(request, recurso):
    cuerpo = ""
    usuario = Usuario.objects.get(nombre=recurso)
    titulo = usuario.titulo_usuario
    log = ""
    error = ""
    inicio = ""
    pagina_principal = '<a href="/">INICIO</a>'
    rss = ""
    rss += '<a href="/' + recurso + '/rss">RSS DEL USUARIO</a>'
    cambio_titulo = ""
    cambio_estilo = ""

    if titulo == "":
        titulo = u'Página de ' + usuario.nombre
    try:
        actividades_selecc = usuario.actividades.all()
        actividades_selecc = actividades_selecc.values()
        aux = 0
        while (aux < len(actividades_selecc)):
            num = actividades_selecc[aux]['id']
            titulo_actividad = actividades_selecc[aux]['titulo']
            fecha = actividades_selecc[aux]['fecha']
            hora = actividades_selecc[aux]['hora']
            cuerpo += '<ul><li><a href="/actividades/' + str(num) + '">' + titulo_actividad
            cuerpo += '</a><ul><li>' + 'Fecha: ' + str(fecha) + ', Hora: ' + str(hora) + '</li></ul></li></ul>'
            aux = aux + 1
    except ObjectDoesNotExist:
        return HttpResponse('No')

    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username + '!'
        log += '<br><a href="/logout">Salir</a>'

    else:
        log += login()
        if request.method == 'POST':
            usuario = request.POST['Usuario']
            password = request.POST['Password']
            user = auth.authenticate(username=usuario, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/" + recurso)
            else:
                error += '<span>Error.</span> Datos incorrectos<br>'
                plantilla = get_template('index.html')
                Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'inicio': inicio, 'pie': pie()})
                renderizado = plantilla.render(Contexto)
                return HttpResponse(renderizado)

    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'inicio': inicio, 'actualizar': cambio_titulo, 'busqueda': cambio_estilo, 'pie': pie(), 'rss': rss})
    renderizado = plantilla.render(Contexto)
    return HttpResponse(renderizado)

def ayuda(request):
    cuerpo = ""
    log = ""
    titulo = u"Ayuda"
    pagina_principal = '<a href="/">INICIO</a>'
    error = ""
    if request.user.is_authenticated():
        log += 'Hola ' + request.user.username + '!'
        log += '<br><a href="/logout">Salir</a>'
    else:
        log += login()

    cuerpo += u'<span>Interfaz pública:</span>'
    cuerpo += '<br><ul style="list-style-type: square">'
    cuerpo += u'<li>Página principal: ofrece las 10 actividades mas cercanas, acceso a las paginas personales, y una serie de enlaces a sitios de interes de la aplicacion.</li>'
    cuerpo += u'<li>Pagina personal de usuario: muestra las actividades seleccionadas por el usuario.</li>'
    cuerpo += '<li>Todas: ofrece todas las actividades disponibles. Permite ordenarlas por precio, fecha y titulo.</li>'
    cuerpo += u'<li>Cada actividad ofrece un pequeño resumen de sus principales caracteristicas, como cuando es, cuando empieza... </li></ul>'
    cuerpo += u'<li> Canal RSS de las 10 actividades mas proximas en el tiempo</li></ul>'
    cuerpo += '<span>Interfaz privada: </span>'
    cuerpo += u'Adicionalmente permite:'
    cuerpo += '<ul style="list-style-type: square">'
    cuerpo += u'<li>Seleccionar actividades en la pagina ACTIVIDADES para su página personal.</li>'
    cuerpo += u'<li>Permite ver un canal RSS con las noticias seleccionadas por el usuario.</li></ul>'


    if request.method == 'POST':
        usuario = request.POST['Usuario']
        password = request.POST['Password']
        user = auth.authenticate(username=usuario, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/ayuda")
        else:
            error += '<span>Error.</span> Datos incorrectos<br>'
            plantilla = get_template('index.html')
            Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'error': error, 'pie': pie()})
            renderizado = plantilla.render(Contexto)
            return HttpResponse(renderizado)

    plantilla = get_template('index.html')
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'titulo': titulo, 'pagina_principal': pagina_principal, 'pie': pie()})
    renderizado = plantilla.render(Contexto)
    return HttpResponse(renderizado)

def CSS(request, recurso):
    log = ""
    cuerpo = ""
    pie = ""
    plantilla_css = get_template(recurso)
    Contexto = Context({'loggin': log, 'contenido': cuerpo, 'pie': pie})
    css = plantilla_css.render(Contexto)
    return HttpResponse(css, content_type='text/css')


