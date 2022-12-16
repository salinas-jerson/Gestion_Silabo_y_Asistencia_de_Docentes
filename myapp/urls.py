from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.AcerceDe,name="about"),
    #path('hello/<str:username>',views.helloWorld,name="hello"),   #se llama y espera nombre de parametro
    path('tarea/',views.tareas,name="tarea"),
    path('project/',views.project,name="project"),
    path('crea_tarea/',views.crear_new_tarea,name="crea_tarea"), 
    #------------ URL DOCENTES ----------------------------
    path('mis_cursos/',views.misCursos,name="mis_cursos"),
    path('docentes/',views.docentes,name="docentes"),
    path('regist_D/',views.resgistD,name="regist_D"),
    path('iniciaSessionD/',views.iniciarSesionD,name="iniciaSessionD"),
    path('cerrarSessionD/',views.cerrarLoginD,name="cerrarSessionD"),
    
    #------------ URL DIRECTOR DE ESCUELA ----------------------------
    path('mis_docentes/',views.misDocentes,name="mis_docentes"),
    path('direct/',views.dirEscuela,name="direct"),
    path('regist_DE/',views.resgistDE,name="regist_DE"),
    path('iniciaSessionDE/',views.iniciarSesionDE,name="iniciaSessionDE"),
    path('cerrarSessionDE/',views.cerrarLoginDE,name="cerrarSessionDE"),
]