from django.contrib import admin
from .models import Docentes, CargaAcademica

# Register your models here. es decir las tablas, para editar desde la administracion
#admin.site.register(Project)
#admin.site.register(Task)
admin.site.register(Docentes)
admin.site.register(CargaAcademica)