#!/usr/bin/python

#
# Simple XML parser for JokesXML
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the jokes in a JokesXML file

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from datetime import datetime
from models import Actividad, Usuario
import string
import urllib, urllib2
#from bs4 import BeautifulSoup

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""
        self.atributo = ""
        self.titulo = ""
        self.tipo = ""
        self.gratis = ""
        self.precio = ""
        self.fecha = ""
        self.hora = ""
        self.larga_dur = ""
        self.url = ""
        self.repetido = 0

    def startElement (self, name, attrs):
        if name == 'atributo':
            self.atributo = normalize_whitespace(attrs.get('nombre'))
        if self.atributo == 'TITULO':
            self.inContent = 1
        elif self.atributo == 'GRATUITO':
            self.inContent = 1
        elif self.atributo == 'PRECIO':
            self.inContent = 1
        elif self.atributo == 'EVENTO-LARGA-DURACION':
            self.inContent = 1
        elif self.atributo == 'FECHA-EVENTO':
            self.inContent = 1
        elif self.atributo == 'FECHA-FIN-EVENTO':
            self.inContent = 1
        elif self.atributo == 'HORA-EVENTO':
            self.inContent = 1
        elif self.atributo == 'CONTENT-URL':
            self.inContent = 1
        elif self.atributo == 'TIPO':
            self.inContent = 1
      
    def endElement (self, name):

        todas = Actividad.objects.all()

        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        
        if self.atributo == 'TITULO':
            for fila in todas:
                if fila.titulo == self.theContent:
                    self.repetido = 1
            if self.repetido == 0:
                self.titulo = self.theContent

        elif self.atributo == 'GRATUITO' and self.repetido == 0:
            if self.theContent == '1':
                self.precio = 'Gratis'
            else:
                if self.precio == "":
                    self.precio = '-----'

        elif self.atributo == 'PRECIO' and self.repetido == 0:
            self.precio = self.theContent

        elif self.atributo == 'EVENTO-LARGA-DURACION' and self.repetido == 0:
            if self.theContent == '1':
                self.larga_dur = 'Si'
            else:
                self.larga_dur = 'No'

        elif self.atributo == 'FECHA-EVENTO' and self.repetido == 0:
            self.fecha = self.theContent.split(' ')[0].replace('-', ' ')
            self.fecha = datetime.strptime(self.fecha, '%Y %m %d')

        elif self.atributo == 'HORA-EVENTO' and self.repetido == 0:
            self.hora = self.theContent

        elif self.atributo == 'CONTENT-URL' and self.repetido == 0:
            self.url = self.theContent
            #urlDescriptor = urllib2.urlopen(self.url)
            #html = urlDescriptor.read()
            #urlDescriptor.close()
            #soup = BeautifulSoup(html)
            #tag = soup.find("a", {"class":"punteado"})
            #if tag == None:
             #   self.url = 'No disponible'
            #else:
             #   self.url = tag.attrs['href']

        elif self.atributo == 'TIPO':
            if self.theContent.find('/') == -1:
                self.inContent = 0
            else:   
                if self.repetido == 0:
                    self.tipo = self.theContent.split('/')[3]
                    actividad = Actividad(titulo=self.titulo, tipo=self.tipo, precio=self.precio, fecha = self.fecha, hora = self.hora, larga_dur=self.larga_dur, url = self.url, fecha_usuario="2000-01-01")
                    actividad.save()
                    self.titulo = ""
                    self.tipo = ""
                    self.gratis = ""
                    self.precio = ""
                    self.fecha = ""
                    self.hora = ""
                    self.larga_dur = ""
                    self.url = ""
                else:
                    self.repetido = 0

        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
    
# Load parser and driver

def getNoticias():

    theParser = make_parser()
    theHandler = CounterHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!

    xmlFile = urllib.urlopen('http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD')
    theParser.parse(xmlFile)
    return ('Actualizacion completada')

print "Parse complete"


