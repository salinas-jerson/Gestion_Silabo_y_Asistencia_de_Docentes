from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#archivos
import csv
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from django.db import IntegrityError
from .models import Document,Docentes, CargaAcademica,Silabo
from .forms import crearTarea

# Create your views here.
 
def index(respuesta):
    title = 'Variable enviada'
    return render(respuesta,"index.html",{'cabecera': title}) #cabecera es una var
      
def AcerceDe(respuesta):
    return render(respuesta,"about.html") 

#----------------------- DIRECTOR DE ESCUELA --------------------------
@login_required
def misDocentes(respuesta):
    docentes= Docentes.objects.all()
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes}) 
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
    #records = Document.objects.all()       #elimina todo
    #records.delete()                       #el directorio
    if request.method == 'POST':   
        try:          
            file = request.FILES['file']     
            if str(file).split(sep='.')[1] =='csv':
                if Document.objects.filter(title='CargaAcademica').exists():
                    Document.objects.filter(title='CargaAcademica').delete()
                    #Document.objects.filter(title='CargaAcademica').update(uploadfile=file)
                    Document(title='CargaAcademica',uploadfile=file).save()
                    #------------------
                    #CsvToDB()
                    return render(request, 'DirEscuela/cargaAcademica.html', { 'uploaded_file_url': "actualizado"})
                else:
                    Document(title='CargaAcademica',uploadfile=file).save()
                    #------------------
                    #CsvToDB()
                    return render(request, 'DirEscuela/cargaAcademica.html', { 'uploaded_file_url': "XD"})
            
            else:
                return render(request, 'DirEscuela/cargaAcademica.html',{"error": "*seleccione un archivo con extención .CSV"})  
            
        
        except:
            return render(request, 'DirEscuela/cargaAcademica.html',{"error": "*seleccione un archivo"})    
    return render(request, 'DirEscuela/cargaAcademica.html')

@login_required
def CsvToDB(respuesta):
    miCSV = Document.objects.filter(title='CargaAcademica')
    if miCSV:
        records = CargaAcademica.objects.all()  #elimina todo
        records.delete()                        # el registro
        name=miCSV.first().uploadfile
        miCSV_arch = open(str(name),errors="ignore")        

        linea = miCSV_arch.readline()
        while (linea):
            elementos= linea.split(sep=';')
            #crea el objeto de cada linea
            CargaAcademica( id_docente = int(elementos[0]),
            TI_DO= elementos[1],
            DOCENTE= elementos[2],
            IDENT = int(elementos[3]),
            PR_DE= elementos[4],
            CARRERA=elementos[5],
            CURSO= elementos[6],
            CRED= int(elementos[7]),
            TIPO= elementos[8],
            GPO= elementos[9],
            HT= int(elementos[10]),
            HP= int(elementos[11]),
            DIA=elementos[12], 
            HR_INICIO= int(elementos[13]),
            HR_FIN= int(elementos[14]),
            AULA= elementos[15],
            LIMITE= int(elementos[16]),
            MATRICULADOS = int(elementos[17])).save()
                     
            linea = miCSV_arch.readline()
            #capturar error
            #print(elementos[3],">",elementos[14])

        miCSV_arch.close()
    return render(respuesta, 'DirEscuela/DirectorEscuela.html')

@login_required
def actualizarDocente(respuesta):
    records = Docentes.objects.all()  #elimina todo
    records.delete()                  # el registro
    id = 0
    # actualiza tabla docente con datos de la tabla carga academica
    for i in CargaAcademica.objects.all():
        if id != i.id_docente:
            id = i.id_docente
            if id != 0: #solo pasa cursos activados
                datos = i.DOCENTE.split(sep=' ') 
                #obtiene nombre del docente
                nom = ""
                for j in datos[:len(datos) -2]:
                    nom += j + " "
                Docentes(  id_docente = int(id),
                    Nombre = nom[:-1],
                    apellido = datos[len(datos)-2] +" "+ datos[len(datos)-1]
                ).save() # guarda cada docente de la carga academica
    docentes= Docentes.objects.all()
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes,"error":"Actualizado"}) 

def Eliminar(respuesta):
    if User.objects.filter(username='sali').exists():
        User.objects.filter(username='sali').delete()
    return render(respuesta,"DirEscuela/DirectorEscuela.html") 

#----------------------- DOCENTE --------------------------
@login_required
def misCursos(respuesta):
    cursos= "consulta cursos"
    Numero=[1,2]
    return render(respuesta,"Docente/MisCursos.html",{'cursos':cursos,'num':Numero})

#variable global
nombre_de_docente=""
apellido_de_docente=""
@login_required
def docentes(respuesta):
    if respuesta.method=="GET":
        Docente= nombre_de_docente
        return render(respuesta,"Docente/docentes.html",{'nombre':Docente})
    else:
        return render(respuesta,"Docente/docentes.html",{'nombre':Docente,'error':"Problemas a iniciar secion"})
        
        
                
#modulo para validar si es un docente
def es_docente(elemento_nombre,elemento_apellido):
    lista_Nombre=[] 
    for item in Docentes.objects.all():
        if elemento_nombre==item.Nombre and elemento_apellido==item.apellido:
            lista_Nombre.append(item.Nombre)
            return True
    return False
def buscar_D_login(Name,lastN):
    for item in User.objects.all():
        if item.first_name==Name and item.last_name==lastN:
            return True
    return False
def resgistD(respuesta):
    if respuesta.method == "GET":
        return render(respuesta,"Docente/resgistrarD.html",{'form':UserCreationForm})
    else:
        if respuesta.POST["password1"] == respuesta.POST["password2"]:
            if es_docente(respuesta.POST["first_name"],respuesta.POST["last_name"]):
                if respuesta.POST["password1"] == "":
                    return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "ingrese sus datos"})
                else:
                    try:
                        user = User.objects.create_user(
                            email=respuesta.POST["email"],last_name=respuesta.POST["last_name"],first_name=respuesta.POST["first_name"],username=respuesta.POST["username"], password=respuesta.POST["password1"])
<<<<<<< HEAD
                        user.save()
                        login(respuesta, user)
                        messages.info(respuesta,"se registró correctamente")
                        return redirect('iniciaSessionD')
=======
                        if buscar_D_login(respuesta.POST["first_name"],respuesta.POST["last_name"])==False:
                            user.save()
                            login(respuesta, user)
                            messages.info("se registró correctamente")
                            return redirect('iniciaSessionD')
>>>>>>> 7371132ddb3004e33c547fb4cc77a2c7ba3ef82c
                    except IntegrityError:
                        return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "El usuario ya existe."})
            return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "Usted aun no esta registrado como Docente."})
        return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "La Contraseña no coincide."})


#-----------------
#buscamos el id mediante username y buscamos el first_name y last_name


def iniciarSesionD(respuesta):    
    def busqueda_username(username1):
        mensaje="no se encontró al usuario"
        for fila in User.objects.all():
            if fila.username==username1:
                return fila.first_name,fila.last_name
        return mensaje

#-----------------
    if respuesta.method == 'GET':
        
        return render(respuesta, 'Docente/loginD.html', {"form": AuthenticationForm})
    else:
        #recuperamos el nombre y apellido de la persona que ingresó 
        nombre_docente,apellido_docente=busqueda_username(respuesta.POST['username'])
        global nombre_de_docente
        global apellido_de_docente
        nombre_de_docente=nombre_docente
        apellido_de_docente=apellido_docente
        #------------------------------------------------
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

@login_required
def registro_Silabo(respuesta):
    def buscar_id_Silabo():
        for item in Silabo.objects.all():
            if item.docente.Nombre==nombre_de_docente and item.docente.apellido==apellido_de_docente:
                return item.id
            
    def buscar_id_Doncente():
        for item in Docentes.objects.all():
            if item.Nombre==nombre_de_docente and item.apellido==apellido_de_docente:
                return item.id

    if respuesta.method=="GET":
        try:
            File=Silabo.objects.get(id=buscar_id_Silabo())#--------------
            return render(respuesta,"Docente/silabos.html",{'file':File.silabo})
        except:
            return render(respuesta,"Docente/silabos.html",{'error':"aun no registró un silabo"})
    else:
        #si se ejecuta el metodo POST subimos el archivo
        if respuesta.method=='POST':
            try:
                uploadedFile=respuesta.FILES["archivo"]
                #sacamos el id del docente
                objeto_de_docente=Docentes.objects.get(id=buscar_id_Doncente())
                document=Silabo(docente=objeto_de_docente,silabo=uploadedFile)
                if buscar_id_Silabo():
                    messages.info(respuesta,"usted ya cargó un silabo")
                    return render(respuesta,"Docente/silabos.html",{'file':File.silabo})
                else:
                    document.save()
                    messages.info(respuesta,"Guardado")
                    return render(respuesta,"Docente/silabos.html",{'file':File.silabo})
                    #File=Silabo.objects.get(id=buscar_id_Silabo())#--------------
                
            except:
                return render(respuesta,"Docente/silabos.html",{'error':"campo vacio"})
        return redirect('silabos')


def asistencia(request):
    return render(request,"Docente/asistencia.html")
def asistencia_alumnos(request):
    return render(request,"Docente/asistenciaAlumnos.html")
def carga_academica(request):
    return render(request,"Docente/cargaAcademica.html")