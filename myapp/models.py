from django.db import models

# Create your models here.
# estas clases son tablas
# las modificaciones aquí, se deben migrar
class Docentes(models.Model):
    Nombre = models.CharField(max_length=40,default="defauld value")
    apellido = models.CharField(max_length=40,default="default value")
    cargo=models.CharField(max_length=20,default="default value")
#tabla silabo---------    
class Silabo(models.Model):
    docente=models.ForeignKey(Docentes,on_delete=models.CASCADE,null=False,blank=False,max_length=20)
    silabo=models.FileField(upload_to='uploads/')
    
    def __str__(self):
        return self.silabo
#--------------------------
class Document(models.Model):
    title=models.CharField(max_length=20)
    uploadfile=models.FileField(upload_to='uploaded Files')
    dataTimeOfUpload=models.DateTimeField(auto_now=True)
#----------------------------------------------




    
#