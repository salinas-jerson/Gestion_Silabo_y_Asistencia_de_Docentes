from django.contrib import admin
from .models import Project,Docentes,Task

# Register your models here. es decir las tablas, para editar desde la administracion
admin.site.register(Project)
admin.site.register(Task)