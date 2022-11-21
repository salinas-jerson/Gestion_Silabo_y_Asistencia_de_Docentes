from django.contrib import admin
from .models import Project,Uasers,Task

# Register your models here. es decir las tablas
admin.site.register(Project)
admin.site.register(Task)