from django.contrib import admin
from django.urls import path, include

#from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("myapp.urls")) #las rutas de la aplicacion
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MADIA_ROOT)