from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from .models import Project,Task
from .forms import crearTarea

# Create your views here.
 
def index(respuesta):
    title = 'Variable enviada'
    return render(respuesta,"index.html",{'cabecera': title}) #cabecera es una var

def project(respuesta):
    projec = Project.objects.all()
    return render(respuesta,"projects.html",{'proyecto':projec}) 

def tareas(respuesta):
    tarea = Task.objects.all()
    return render(respuesta,"tareas.html",{'tareas':tarea}) 

def crear_new_tarea(respuesta):
    if respuesta.method == 'GET':
        #mostrar interface
        return render(respuesta,"crear_tarea.html", {'form':crearTarea()})
    else:
        #guardar datos / cada atributo
        #print(respuesta.POST['title']) # lo que viene del formulario en title y descripcion
        Task.objects.create(
        name=respuesta.POST['title'],
        descripcion=respuesta.POST['descripcion'],
        OdersTablas_id=1
        )
        #las variables son los mismops de la tabla (si es forinkey -> con ..._...)
        return redirect('tarea')
        

def AcerceDe(respuesta):
    return render(respuesta,"about.html") 

#----------------------- DIRECTOR DE ESCUELA --------------------------
def misDocentes(respuesta):
    docentes= "consulta D.E. docentes"
    Numero=[1,2]
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes,'num':Numero}) 

def dirEscuela(respuesta):
    Docente= "consultas del director de escuela" 
    return render(respuesta,"DirEscuela/DirectorEscuela.html",{'director':Docente}) 

#----------------------- DOCENTE --------------------------
def misCursos(respuesta):
    cursos= "consulta cursos"
    Numero=[1,2]
    return render(respuesta,"Docente/MisCursos.html",{'cursos':cursos,'num':Numero}) 

def docentes(respuesta):
    Docente= "consulta docente"
    return render(respuesta,"Docente/docentes.html",{'docente':Docente})