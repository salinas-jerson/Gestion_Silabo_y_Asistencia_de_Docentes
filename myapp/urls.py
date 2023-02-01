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
    path('silabos/ParteSilabo/<i>',views.ParteSilabo,name="ParteSilabo"),

    path('asistencia/',views.asistencia,name="asistencia"),
    path('asistencia/control_de_asistenciaAL/<i>',views.ControlAsistenciaAL,name='control_de_asistenciaAL'),
    path('asistencia/control_de_asistenciaAL/<i>/control_alumno',views.control_alumno,name='control_alumno'),
    #path('control_alumno/',views.control_alumno,name='control_alumno'),
    path('asistencia/registroTema/<cur>',views.registroTema,name="regis_Tema"),
    path('asistencia/registroAsistencia/<cur>',views.registroAsistencia,name="registroAsistencia"),
    path('asistencia_alumnos/',views.asistencia_alumnos,name="asistencia_Al"),
    path('asistencia_alumnos/guardarAlumnos/<i>',views.guardar_Alumnos,name="guardar_alumnos"),
    path('asistencia_alumnos/borrarAlumnos/<i>',views.borrar_Alumnos,name="borrar_alumnos"),
    path('carga_academica/',views.carga_academica,name="carga_academica"),
    path('docentes/',views.docentes,name="docentes"),
    path('regist_D/',views.resgistD,name="regist_D"),
    path('iniciaSessionD/',views.iniciarSesionD,name="iniciaSessionD"),
    path('cerrarSessionD/',views.cerrarLoginD,name="cerrarSessionD"),
    
    
    #------------ URL DIRECTOR DE ESCUELA ----------------------------
    path('mis_docentes/',views.misDocentes,name="mis_docentes"),
    path('direct/',views.dirEscuela,name="direct"),
    path('programar-tarea/',views.programarTarea,name="programar-tarea"),
    path('iniciaSessionDE/',views.iniciarSesionDE,name="iniciaSessionDE"),
    path('cerrarSessionDE/',views.cerrarLoginDE,name="cerrarSessionDE"),
    path('carga_academcica/',views.cargaAcademica,name="carga_academcica"),
    path('carga_DB/',views.CsvToDB,name="carga_DB"),
    path('update_docente/',views.actualizarDocente,name="update_docente"), 
    path('Eliminar_docente/',views.Eliminar_user_docentes,name="Eliminar_docente"), 
    path('crear_user_docentes/',views.crear_user_docentes,name="crear_user_docentes"), 
    path('mis_docentes/ver-actividades/',views.verDetalleActividades,name="ver-actividades"),
    path('mis_docentes/ver-actividades/consulta/',views.verAsistencia_Tema,name="consulta"),
    #path('mis_docentes/ver-actividades/export/', views.export_pdf, name="export-pdf" ),

]#
urlpatterns+=[
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
