from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('about/',views.AcerceDe),
    path('hello/<str:username>',views.helloWorld)   #se llama y espera otro nombre
]