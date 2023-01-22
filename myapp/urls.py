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
    path('silabos/',views.registro_Silabo,name="regis_silabo"),
    path('silabos/eliminarSilabo/<i>',views.eliminarSilabo,name='eliminarSilabo'),
    path('silabos/guardarSilabo/<i>',views.guardarSilabo,name="guardarSilabo"),
    path('asistencia/',views.asistencia,name="asistencia"),
    path('asistencia/registroTema/<cur>',views.registroTema,name="regis_Tema"),
    path('asistencia/registroAsistencia/<cur>',views.registroAsistencia,name="registroAsistencia"),
    path('asistencia_alumnos/',views.asistencia_alumnos,name="asistencia_Al"),
    path('carga_academica/',views.carga_academica,name="carga_academica"),
    path('docentes/',views.docentes,name="docentes"),
    path('regist_D/',views.resgistD,name="regist_D"),
    path('iniciaSessionD/',views.iniciarSesionD,name="iniciaSessionD"),
    path('cerrarSessionD/',views.cerrarLoginD,name="cerrarSessionD"),
    
    #------------ URL DIRECTOR DE ESCUELA ----------------------------
    path('mis_docentes/',views.misDocentes,name="mis_docentes"),
    path('direct/',views.dirEscuela,name="direct"),
    path('mis_datos/',views.misDatos,name="mis_datos"),
    path('iniciaSessionDE/',views.iniciarSesionDE,name="iniciaSessionDE"),
    path('cerrarSessionDE/',views.cerrarLoginDE,name="cerrarSessionDE"),
    path('carga_academcica/',views.cargaAcademica,name="carga_academcica"),
    path('carga_DB/',views.CsvToDB,name="carga_DB"),
    path('update_docente/',views.actualizarDocente,name="update_docente"), 
    path('Eliminar_docente/',views.Eliminar_user_docentes,name="Eliminar_docente"), 
    path('crear_user_docentes/',views.crear_user_docentes,name="crear_user_docentes"), 
    path('mis_docentes/ver_silabos/<int:id>/',views.verSilabos,name="ver_silabos"),
    path('mis_docentes/ver_silabos/reporte-asistencia/',views.verAsistencia,name="reporte-asistencia"),

]#
urlpatterns+=[
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
