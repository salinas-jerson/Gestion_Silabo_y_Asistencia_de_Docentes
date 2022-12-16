from django.db import models

# Create your models here.
# estas clases son tablas
# las modificaciones aquí, se deben migrar
class Docentes(models.Model):
    username = models.TextField()
    password = models.TextField()

class Project(models.Model):
    #atributos 
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Task(models.Model):
    #atributos 
    name = models.CharField(max_length=200)
    descripcion = models.TextField()
    #si la dependencia es eliminada -> esta se elimina en cascada
    OdersTablas = models.ForeignKey(Project, on_delete = models.CASCADE)

    #done = models.BooleanField(default=False)
    def __str__(self):
        return self.name + " - " + self.OdersTablas.name