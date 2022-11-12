from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def helloWorld(respuesta,username):
    return HttpResponse("<h1> Hello World bienvenido %s </h1>" %username)
 
def index(respuesta):
    return HttpResponse("<h1> iNDEX PAGE </h1>")

def AcerceDe(respuesta):
    return HttpResponse("<h1> Acerca de la gestion de silabo </h1>")