from django.db import models

# Create your models here.
#estas clases son tablas
class Uasers(models.Model):
    title = models.TextField()

class Proyect(models.Model):
    #atributos 
    name = models.CharField(max_length=200)
    #dependencias
    #si la dependencia es eliminada -> esta se elimina en cascada
    OdersTablas = models.ForeignKey(Uasers, on_delete = models.CASCADE)