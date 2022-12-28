from django.db import models

# Create your models here.
# estas clases son tablas
# las modificaciones aquí, se deben migrar
class Docentes(models.Model):
    id_docente = models.PositiveIntegerField()
    Nombre = models.CharField(max_length=40,default="defauld value")
    apellido = models.CharField(max_length=40,default="default value")
    cargo=models.CharField(max_length=20,default="default value")
    
    def __str__(self):
        return self.apellido + " "+ self.Nombre
#tabla silabo---------    
class Silabo(models.Model):
    docente=models.ForeignKey(Docentes,on_delete=models.CASCADE,null=False,blank=False,max_length=20)
    silabo=models.FileField(upload_to='uploads/')
    
    def __str__(self):
        return self.silabo
#--------------------------
class Document(models.Model):
    title=models.CharField(max_length=20)
    uploadfile=models.FileField(upload_to='myapp/files/')
    dataTimeOfUpload=models.DateTimeField(auto_now=True)
#----------------------------------------------


# Tabla carga académica
class CargaAcademica(models.Model):
    id_docente = models.PositiveIntegerField()
    TI_DO= models.CharField(max_length=10,default="defauld value")
    DOCENTE= models.CharField(max_length=80,default="defauld value")
    IDENT = models.PositiveIntegerField()
    PR_DE= models.CharField(max_length=10,default="defauld value")
    CARRERA=models.CharField(max_length=50,default="defauld value")
    CURSO=models.CharField(max_length=80,default="defauld value")
    CRED=models.PositiveIntegerField()
    TIPO=models.CharField(max_length=2,default="defauld value")
    GPO=models.CharField(max_length=2,default="defauld value")
    HT=models.PositiveIntegerField()
    HP=models.PositiveIntegerField()
    DIA=models.CharField(max_length=10,default="defauld value")
    HR_INICIO=models.PositiveIntegerField()
    HR_FIN=models.PositiveIntegerField()
    AULA=models.CharField(max_length=10,default="defauld value")
    LIMITE=models.PositiveIntegerField()
    MATRICULADOS =models.PositiveIntegerField()




    
#