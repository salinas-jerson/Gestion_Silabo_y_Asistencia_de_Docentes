from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
#archivos
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from django.db import IntegrityError
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
@login_required
def misDocentes(respuesta):
    docentes= "consulta D.E. docentes"
    Numero=[1,2]
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes,'num':Numero}) 
@login_required
def dirEscuela(respuesta):
    Docente= "consultas del director de escuela" 
    return render(respuesta,"DirEscuela/DirectorEscuela.html",{'director':Docente}) 
def resgistDE(respuesta):
    if respuesta.method == "GET":
        return render(respuesta,"DirEscuela/resgistrarDE.html",{'form':UserCreationForm})
    else:
        if respuesta.POST["password1"] == respuesta.POST["password2"]:
            if respuesta.POST["password1"] == "":
                return render(respuesta, "DirEscuela/resgistrarDE.html", {"form": UserCreationForm, "error": "ingrese sus datos"})
            else:
                try:
                    user = User.objects.create_user(
                        respuesta.POST["username"], password=respuesta.POST["password1"])
                    user.save()
                    login(respuesta, user)
                    return redirect('direct')
                except IntegrityError:
                    return render(respuesta, "DirEscuela/resgistrarDE.html", {"form": UserCreationForm, "error": "El usuario ya existe."})

        return render(respuesta, "DirEscuela/resgistrarDE.html", {"form": UserCreationForm, "error": "La Contraseña no coencide."})

def iniciarSesionDE(respuesta):    
    if respuesta.method == 'GET':
        return render(respuesta, 'DirEscuela/loginDE.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            respuesta, username=respuesta.POST['username'], password=respuesta.POST['password'])
        if user is None:
            return render(respuesta, 'DirEscuela/loginDE.html', {"form": AuthenticationForm, "error": "nombre o contraseña incorrecta."})

        login(respuesta, user)
        return redirect('direct')

@login_required
def cerrarLoginDE(respuesta):
    logout(respuesta)
    return redirect("index")


@login_required
def cargaAcademica(request):
    if request.method == 'POST':    
        try:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file) 
            uploaded_file_url = fs.url(filename)            
            return render(request, 'DirEscuela/cargaAcademica.html', { 'uploaded_file_url': uploaded_file_url})
        
        except:
            return render(request, 'DirEscuela/cargaAcademica.html',{"error": "*seleccione un archivo"})    
    return render(request, 'DirEscuela/cargaAcademica.html')

#----------------------- DOCENTE --------------------------
@login_required
def misCursos(respuesta):
    cursos= "consulta cursos"
    Numero=[1,2]
    return render(respuesta,"Docente/MisCursos.html",{'cursos':cursos,'num':Numero}) 

@login_required
def docentes(respuesta):
    Docente= "consulta docente"
    return render(respuesta,"Docente/docentes.html",{'docente':Docente})

def resgistD(respuesta):
    if respuesta.method == "GET":
        return render(respuesta,"Docente/resgistrarD.html",{'form':UserCreationForm})
    else:
        if respuesta.POST["password1"] == respuesta.POST["password2"]:
            if respuesta.POST["password1"] == "":
                return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "ingrese sus datos"})
            else:
                try:
                    user = User.objects.create_user(
                        respuesta.POST["username"], password=respuesta.POST["password1"])
                    user.save()
                    login(respuesta, user)
                    return redirect('docentes')
                except IntegrityError:
                    return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "El usuario ya existe."})

        return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "La Contraseña no coencide."})

def iniciarSesionD(respuesta):    
    if respuesta.method == 'GET':
        return render(respuesta, 'Docente/loginD.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            respuesta, username=respuesta.POST['username'], password=respuesta.POST['password'])
        if user is None:
            return render(respuesta, 'Docente/loginD.html', {"form": AuthenticationForm, "error": "nombre o contraseña incorrecta."})

        login(respuesta, user)
        return redirect('docentes')

@login_required
def cerrarLoginD(respuesta):
    logout(respuesta)
    return redirect("index")