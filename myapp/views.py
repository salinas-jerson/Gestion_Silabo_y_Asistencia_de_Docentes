from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#archivos
from django.template.loader import render_to_string
#from weasyprint import HTML
#from weasyprint.fonts import FontConfiguration

from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from django.db import IntegrityError
from .models import Document,Docentes, CargaAcademica,Silabo,Asistencia_In,Avance_Docente

# Create your views here.
 
def index(respuesta):
    title = 'Variable enviada'
    return render(respuesta,"index.html",{'cabecera': title}) #cabecera es una var
      
def AcerceDe(respuesta):
    return render(respuesta,"about.html") 

#----------------------- DIRECTOR DE ESCUELA --------------------------
#variables globales
nombre_director_escuela = ""
@login_required # lista, consulta de docentes
def misDocentes(respuesta):
    docentes= Docentes.objects.all()
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes}) 

@login_required # home director de escuela
def dirEscuela(respuesta):
    #"consultas del director de escuela" 
    return render(respuesta,"DirEscuela/DirectorEscuela.html",{"nombre_director_escuela": nombre_director_escuela}) 

def iniciarSesionDE(respuesta):    # 
    if respuesta.method == 'GET':
        global nombre_director_escuela
        return render(respuesta, 'DirEscuela/loginDE.html', {"form": 
        AuthenticationForm})
    else:
        user = authenticate(
            respuesta, username=respuesta.POST['username'], password=respuesta.POST['password'])
        if user is None:
            return render(respuesta, 'DirEscuela/loginDE.html', {"form": AuthenticationForm, "error": "nombre o contraseña incorrecta."})

        login(respuesta, user)
        global nombre_director_escuela  #var global DE
        datosDE = User.objects.filter(username=respuesta.POST['username'])
        nombre_director_escuela = datosDE[0]
        
        return render(respuesta, 'DirEscuela/DirectorEscuela.html', {"nombre_director_escuela": nombre_director_escuela})

@login_required  # cierra sesion
def cerrarLoginDE(respuesta):
    logout(respuesta)
    return redirect("index")

@login_required # recibe el archivo csv (carga academica)
def cargaAcademica(request):
    if request.method == 'POST':   
        try:          
            file = request.FILES['file']     
            if str(file).split(sep='.')[1].lower() =='csv':
                if Document.objects.filter(title='CargaAcademica').exists():
                    Document.objects.filter(title='CargaAcademica').delete()
                    #Document.objects.filter(title='CargaAcademica').update(uploadfile=file)
                    Document(title='CargaAcademica',uploadfile=file).save()
                    return render(request, 'DirEscuela/cargaAcademica.html', { 'uploaded_file_url': "actualizado"})
                else:
                    Document(title='CargaAcademica',uploadfile=file).save()
                    return render(request, 'DirEscuela/cargaAcademica.html', { 'uploaded_file_url': "XD"})            
            else:
                return render(request, 'DirEscuela/cargaAcademica.html',{"error": "*seleccione un archivo con extención .CSV"})
        except:
            return render(request, 'DirEscuela/cargaAcademica.html',{"error": "*seleccione un archivo"})    
    return render(request, 'DirEscuela/cargaAcademica.html')

@login_required # actualiza la base de datos con el archivo cargado
def CsvToDB(respuesta):
    miCSV = Document.objects.filter(title='CargaAcademica')
    if miCSV:
        records = CargaAcademica.objects.all()  #elimina todo
        records.delete()                        # el registro
        name=miCSV.first().uploadfile
        miCSV_arch = open("myapp/"+str(name),errors="ignore")        

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
        miCSV_arch.close()
    return render(respuesta, 'DirEscuela/DirectorEscuela.html')

@login_required #actualiza la tabla de docentes
def actualizarDocente(respuesta):
    records = Docentes.objects.all()  #elimina todo
    records.delete()                  # el registro
    id = 0
    # actualiza tabla docente con datos de la tabla carga academica
    for i in CargaAcademica.objects.all():
        if id != i.id_docente:
            id = i.id_docente
            if id != 0: #solo pasa cursos activados .:. con docentes 
                datos = i.DOCENTE.split(sep=' ') 
                num_apelli = 2
                if len(datos) > 4 and datos[-2:][0] == "LA": #en caso sea casado
                    num_apelli = 4
                #obtiene nombre del docente
                nom = ""      
                ape = ""          
                for j in datos[:len(datos) - num_apelli]:
                    nom += j + " "
                for k in datos[-num_apelli:]:
                    ape += k +" "
                Docentes(  id_docente = int(id),
                    Nombre = nom[:-1].lower(),
                    apellido = ape[:-1].upper()
                ).save() # guarda cada docente de la carga academica
    docentes= Docentes.objects.all()
    messages.info (respuesta,"Usted, actualizó la tabla docente")
    return render(respuesta,"DirEscuela/MisDocentes.html",{'docentes':docentes,"error":"Actualizado"}) 

@login_required #modifica sus datos 
def misDatos(respuesta):
    if respuesta.method == 'GET':
        DirEsc = User.objects.filter(is_superuser=1)
        return render(respuesta,"DirEscuela/misDatosDE.html",{'director_escuela':DirEsc}) 
    else:
        return render(respuesta,"DirEscuela/misDatosDE.html") 

@login_required
def Eliminar_user_docentes(respuesta): #elimina todos los usuarios de los docentes
    docentes= Docentes.objects.all()
    for i in docentes:
        if User.objects.filter(username=i.Nombre).exists():
            User.objects.filter(username=i.Nombre).delete()
    return render(respuesta,"DirEscuela/DirectorEscuela.html") 

@login_required
def crear_user_docentes(respuesta): # crea usuarios para todos los docentes
    docentes= Docentes.objects.all()
    for i in docentes:
        User(  
            email= i.Nombre+"@gmail.com",
            first_name=i.Nombre,
            last_name=i.apellido,            
            username=i.Nombre,             
            password=make_password("123")).save()
    return render(respuesta,"DirEscuela/DirectorEscuela.html") 

def regla3Simple(total,parte):
    if total != 0:
        return 100*parte/total
    else:
        return 0

def reporteAsistencia(id_curso,id_docente):
    return Asistencia_In.objects.filter(id_Docente = id_docente, codigo_curso = id_curso)

def reporteTemas(id_curso,id_docente):
    return Avance_Docente.objects.filter(id_Docente_Avance = id_docente, codigo_curso = id_curso)



def totalAsistencia(id_docente,id_curso,asistencia,total_asistencia, total_destiempo, total_puntual, total_tarde):
    objeto = CargaAcademica.objects.filter( id_docente = id_docente, PR_DE = id_curso)
    hora = str(objeto.first().HR_INICIO)+":00:00" # hora de inicio del curso
    horaFin = str(objeto.first().HR_FIN)+":00:00" # hora de inicio del curso
    horaFin = datetime.strptime(horaFin, "%H:%M:%S")
    hora = datetime.strptime(hora, "%H:%M:%S")
    minutosClase = str(horaFin - hora).split(':')
    minutosClase = int(minutosClase[0])*60 + int(minutosClase[1])

    total_asistencia += len(asistencia)
    for j in asistencia:
        #c.
        diferencia =  datetime.strptime(str(j.HoraEntrada).split('.')[0], "%H:%M:%S") - hora
        diferencia = str(diferencia).split(':')
        if len(diferencia[0].split(',')) >= 2: # muy a destiempo , resulta en días
            total_destiempo+=1
        else:
            minutos = int(diferencia[0])*60 + int(diferencia[1])
                        
            if  0 <= minutos <= 15: #puntual
                total_puntual+=1
            else:
                if minutos < minutosClase :
                    total_tarde+=1
                else:
                    total_destiempo+=1
                
    return total_asistencia,total_destiempo, total_puntual,total_tarde



@login_required
def verDetalleActividades(respuesta):
    if respuesta.method == 'POST':   
        id_docente = respuesta.POST["id_docente"] 
        silabos = Silabo.objects.filter(id_Docente=id_docente)        
        cursos1 = CargaAcademica.objects.filter(id_docente=id_docente)
        cursos = []
        nom = ""
        for i in cursos1:                
            if i.PR_DE != nom: #restringir por codigo de curso PR_DE
                nom = i.PR_DE
                cursos.append(i)
                docente = i.DOCENTE    

        if respuesta.POST["btn"] == "silabo": 
            return render(respuesta,"DirEscuela/verSilabos.html",{"silabos":silabos,"cursos":cursos,"docente":docente})
        else: # btn = reporte
            temas_totales = []
            for i in cursos:
                temas = reporteTemas(i.PR_DE, id_docente)
                temas_totales.append(([i.PR_DE,i.CURSO,"  : Hora "+str(i.HR_INICIO)+":00"],temas))
            
            total_asistencia = 0
            total_destiempo = 0
            total_puntual = 0
            total_tarde = 0
            asistencia_totales = []
            for i in cursos:
                asistencia = reporteAsistencia(i.PR_DE,id_docente)
                asistencia_totales.append(([i.PR_DE,i.CURSO,"  : Hora "+str(i.HR_INICIO)+":00"],asistencia))
                total_asistencia, total_destiempo, total_puntual, total_tarde =  totalAsistencia(id_docente, i.PR_DE, asistencia,total_asistencia, total_destiempo, total_puntual, total_tarde)
            
            
            return render(respuesta,"DirEscuela/reporte.html",{"total_asistencia" :total_asistencia,
            "total_destiempo":regla3Simple(total_asistencia,total_destiempo),"total_puntual":regla3Simple(total_asistencia,total_puntual), "total_tarde" :regla3Simple(total_asistencia,total_tarde),"temas_totales":temas_totales,"asistencia_totales":asistencia_totales,"docente":docente})
 
@login_required
def verAsistencia_Tema(respuesta):
    if respuesta.method == 'POST':
        id_docente = respuesta.POST["id_docente"]
        curso =   respuesta.POST["curso"]
        id_curso =   respuesta.POST["id_curso"] #PR_DE de la carga
        docente =   respuesta.POST["docente"]
        if respuesta.POST["btn"] == "asistencia": # despues de los 15 minutos se consira tarde para el docente
            hora = CargaAcademica.objects.filter( id_docente = id_docente, PR_DE = id_curso)
            hora = hora.first().HR_INICIO
            return render(respuesta,"DirEscuela/asistencia.html",{"id_curso":id_curso,"curso":curso,"docente":docente, "hora":hora,"asistencia":reporteAsistencia(id_curso,id_docente)})
        else: # btn = temas 
            return render(respuesta,"DirEscuela/temasAvance.html",{"id_curso":id_curso, "curso":curso,"docente":docente,"temas":reporteTemas(id_curso,id_docente)})


"""def resgistDE(respuesta):
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

        return render(respuesta, "DirEscuela/resgistrarDE.html", {"form": UserCreationForm, "error": "La Contraseña no coencide."})"""

#----------------------- DOCENTE --------------------------
@login_required
def misCursos(respuesta):
    cursos= "consulta cursos"
    Numero=[1,2]
    return render(respuesta,"Docente/MisCursos.html",{'cursos':cursos,'num':Numero})

#variable global
nombre_de_docente=""
apellido_de_docente=""
Id_de_docente=""
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
            if es_docente(respuesta.POST["first_name"].lower(),respuesta.POST["last_name"].upper()):
                if respuesta.POST["password1"] == "":
                    return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "ingrese sus datos"})
                else:
                    try:
                        user = User.objects.create_user(
                            email=respuesta.POST["email"],last_name=respuesta.POST["last_name"].upper(),first_name=respuesta.POST["first_name"].lower(),username=respuesta.POST["username"].lower(), password=respuesta.POST["password1"])
                        if buscar_D_login(respuesta.POST["first_name"].lower(),respuesta.POST["last_name"].upper())==False:
                            user.save()
                            login(respuesta, user)
                            messages.info("se registró correctamente")
                            return redirect('iniciaSessionD')
                    except IntegrityError:
                        return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "El usuario ya existe."})
            return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "Usted aun no esta registrado como Docente."})
        return render(respuesta, "Docente/resgistrarD.html", {"form": UserCreationForm, "error": "La Contraseña no coincide."})


#-----------------
#buscamos el id mediante username y buscamos el first_name y last_name
def buscar_id(name,lastname):
        for i in Docentes.objects.all():
            if i.Nombre.lower()==name.lower() and i.apellido.lower()==lastname.lower():
                return i.id_docente

def iniciarSesionD(respuesta):    
    def busqueda_username(username1):
        for fila in User.objects.all():
            if fila.username==username1.lower():
                return fila.first_name, fila.last_name
        return 0
    #------------
#-----------------
    if respuesta.method == 'GET':
        return render(respuesta, 'Docente/loginD.html', {"form": AuthenticationForm})
    else:
        #recuperamos el nombre y apellido de la persona que ingresó 
        if busqueda_username(respuesta.POST['username'].lower()) != 0:
            nombre_docente,apellido_docente=busqueda_username(respuesta.POST['username'].lower())
            
        else:
            
            mensaje = "No existe usuario"
            nombre_docente = "0"
            apellido_docente ="0"
        global nombre_de_docente
        global apellido_de_docente
        nombre_de_docente=nombre_docente
        apellido_de_docente=apellido_docente
        global Id_de_docente
        Id_de_docente=buscar_id(nombre_de_docente,apellido_de_docente)
        #------------------------------------------------
        user = authenticate(
            respuesta, username=respuesta.POST['username'], password=respuesta.POST['password'])
        if user is None: 
            return render(respuesta, 'Docente/loginD.html', {"form": AuthenticationForm, "error": "nombre o contraseña incorrecta."})

        login(respuesta, user)
        return render(respuesta, 'Docente/docentes.html')
        #return redirect('docentes')

@login_required
def cerrarLoginD(respuesta):
    logout(respuesta)
    return redirect("index")


@login_required

def registro_Silabo(respuesta):
    def buscar_id_Silabo(curso):
        for item in Silabo.objects.all():
            if item.docente.Nombre.lower()==nombre_de_docente.lower() and item.docente.apellido.lower()==apellido_de_docente.lower() and item.curso.lower()==curso.lower():
                return item.id
       
            
    def buscar_id_Doncente():
        for item in Docentes.objects.all():
            if item.Nombre.lower()==nombre_de_docente.lower() and item.apellido.lower()==apellido_de_docente.lower():
                return item.id_docente
    def buscar_curso():
        cursos=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente==Id_de_docente:
                cursos.append(item.CURSO.replace(" "," ")) # porque es necesario reemplazar el espacio?
        cursos_unicos=list(set(cursos))
        return cursos_unicos

    materias=buscar_curso()
    registros_objetos=[]
    subidos=[]
    if respuesta.method=="GET":
        #consultamos el numero de silabos
        for item in materias:
            ss=buscar_id_Silabo(item)
            if ss:
                File=Silabo.objects.get(id=ss)#--------------
                registros_objetos.append(File)
                subidos.append(File.curso)  
                 
        return render(respuesta,"Docente/silabos.html",{'cursos':materias,'BD':registros_objetos})

def guardarSilabo(request,i):
    def buscar_id_Silabo(curso):
        for item in Silabo.objects.all():
            if item.docente.Nombre.lower()==nombre_de_docente.lower() and item.docente.apellido.lower()==apellido_de_docente.lower() and item.curso.lower()==curso.lower():
                return item.id
    def buscar_id_Doncente():
        for item in Docentes.objects.all():
            if item.Nombre.lower()==nombre_de_docente.lower() and item.apellido.lower()==apellido_de_docente.lower():
                return item.id_docente
    def buscar_curso():
        cursos=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente==Id_de_docente:
                cursos.append(item.CURSO.replace(" ",""))
        cursos_unicos=list(set(cursos))
        return cursos_unicos
    materias=buscar_curso()
    registros_objetos=[]
    if request.method=='POST':            
        uploadedFile=request.FILES["archivo"]
        objeto_de_docente=Docentes.objects.get(id_docente=buscar_id_Doncente())
        document=Silabo(docente=objeto_de_docente,silabo=uploadedFile,curso=i,id_Docente=objeto_de_docente.id_docente)
        document.save()    
        messages.info(request,"Silabo"+ i +" Guardado!")
        for item in materias:
            ss=buscar_id_Silabo(item)
            if ss:
                File=Silabo.objects.get(id=ss)#--------------
                registros_objetos.append(File)
        return redirect('regis_silabo')
        #return render(request,"Docente/silabos.html",{'cursos':materias,'BD':registros_objetos})                       
def eliminarSilabo(request,i):
    silabo=Silabo.objects.get(curso=i)
    silabo.delete()
    messages.info(request,i+" ELIMINADO")
    return redirect('regis_silabo')



def asistencia_alumnos(request):
    return render(request,"Docente/asistenciaAlumnos.html")
def carga_academica(request):
    #separamos solo carga del docente del resto
    def buscar_Carga():
        #buscamos la carga del docente y almacenamos
        Docente_carga=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente== Id_de_docente:
                Docente_carga.append(item)
        return Docente_carga
    #utilizamos el arreglo del docente
    def consultas():
        carga_docente=buscar_Carga()
        cursos=[]
        for item in carga_docente:
            cursos.append(item.CURSO)
        cursos_unicos=list(set(cursos))
        
        #diccionario anidado
        dic={}  
        for cur in cursos_unicos:
            dic[cur]={}
            for g in carga_docente:
                if cur==g.CURSO:
                    dic[cur][g.PR_DE]={}
                    for d in carga_docente:
                        if g.PR_DE==d.PR_DE:
                            dic[cur][g.PR_DE][d.DIA]={}
                            dic[cur][g.PR_DE][d.DIA]=d.AULA+" "+str(d.HR_INICIO)+":00"+" - "+str(d.HR_FIN)+":00"
                            
        return dic
    if request.method=='GET':
        diccionario=consultas()
        return render(request,"Docente/cargaAcademica.html",{'dic':diccionario})

def registroTema(request,cur):
    def buscar_IdDoncente():
        for item in Docentes.objects.all():
            if item.Nombre.lower()==nombre_de_docente.lower() and item.apellido.lower()==apellido_de_docente.lower():
                return item.id_docente
    #reunimos la informacion necesaria
    #docente,Tema,FechaAvance,id_Docente,Avance_curso
    avance_docente=Docentes.objects.get(id_docente=buscar_IdDoncente())
    cod_curso=CargaAcademica.objects.filter(id_docente=avance_docente.id_docente)
    cod=""
    for c in cod_curso:
        if c.CURSO==cur:
            cod=c.PR_DE
    contenido=request.POST['TemaAvance']
    registro_avance=Avance_Docente(docente=avance_docente,Tema=contenido,id_Docente_Avance=avance_docente.id_docente,Avance_curso=cur,codigo_curso=cod)
    registro_avance.save()
    messages.success(request,"Su Avance del dia "+cur+" Fue Registrada!")
    return redirect('asistencia')
    


from datetime import datetime
def asistencia(request):
    def buscar_curso():
        cursos=[]
        grupos=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente==Id_de_docente:
                cursos.append(item.CURSO) # porque es necesario reemplazar el espacio?
                grupos.append(item.PR_DE)
        cursos_unicos=list(set(cursos))
        grupos_unicos=list(set(grupos))
        return cursos_unicos,grupos_unicos
    def buscar_Carga():
        #buscamos la carga del docente y almacenamos
        Docente_carga=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente== Id_de_docente:
                Docente_carga.append(item)
        return Docente_carga
    #utilizamos el arreglo del docente
    def consultas():
        carga_docente=buscar_Carga()
        cursos=[]
        for item in carga_docente:
            cursos.append(item.CURSO)
        cursos_unicos=list(set(cursos))
        
        #diccionario anidado
        dic={}  
        for cur in cursos_unicos:
            dic[cur]={}
            for g in carga_docente:
                if cur==g.CURSO:
                    dic[cur][g.PR_DE]={}
                    
        return dic
    #importamos datetime from datetime
    #entonces capturamos la fecha y hora
    materia,grupos=buscar_curso()
    m=consultas() #diccionario de grupos
    time_now=datetime.now()
    Fecha=time_now.date()
    Hora=time_now.time()
    if request.method=='GET':
        return render(request,"Docente/asistencia.html",{'cursos':materia,'Fecha_actual':Fecha,'Hora_actual':Hora,'grupos':m})

@login_required
def registroAsistencia(request,cur):
    def buscar_IdDoncente():
        for item in Docentes.objects.all():
            if item.Nombre.lower()==nombre_de_docente.lower() and item.apellido.lower()==apellido_de_docente.lower():
                return item.id_docente
    def buscar_curso():
        cursos=[]
        for item in CargaAcademica.objects.all():
            if item.id_docente==Id_de_docente:
                cursos.append(item.CURSO.replace(" "," ")) # porque es necesario reemplazar el espacio?
        cursos_unicos=list(set(cursos))
        return cursos_unicos

    #importamos datetime from datetime
    #entonces capturamos la fecha y hora
    materia=buscar_curso()
    time_now=datetime.now()
    Fecha=time_now.date()
    Hora=time_now.time()
    if request.method=='GET':
        return render(request,"Docente/asistencia.html",{'cursos':materia,'Fecha_actual':Fecha,'Hora_actual':Hora})
    else:
        if request.method=='POST':
            try:
                if request.POST["mi_asistencia"]:
                    try:
                        #aqui se registraria la asistencia en una tabla en la BD
                        asistencia_docente=Docentes.objects.get(id_docente=buscar_IdDoncente())
                        cod_curso=CargaAcademica.objects.filter(id_docente=asistencia_docente.id_docente)
                        '''cod=""
                        for c in cod_curso:
                            if c.CURSO==cur:
                                cod=c.PR_DE'''
                        cod=request.POST["grupos"]
                        print(cod)
                        registro_asistencia=Asistencia_In(docente=asistencia_docente,HoraEntrada=Hora,FechaIn=Fecha,id_Docente=asistencia_docente.id_docente,Asistencia_curso=cur,codigo_curso=cod)
                        registro_asistencia.save()
                        messages.success(request,"Su Asistencia de "+cur+" Fue Registrada!")
                        return redirect('asistencia')      
                    except:
                        messages.warning(request,"usted ya registró su asistencia en "+cur)
                        return redirect('asistencia')
            except:
                messages.warning(request,"no seleccionó la casilla ")
        return redirect('asistencia')