from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.AcerceDe,name="about"),
    #path('hello/<str:username>',views.helloWorld,name="hello"),   #se llama y espera nombre de parametro
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
    path('carga_academcica/',views.cargaAcademica,name="carga_academcica"),
    path('carga_DB/',views.CsvToDB,name="carga_DB"),
    path('update_docente/',views.actualizarDocente,name="update_docente"),
]
urlpatterns+=[
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )