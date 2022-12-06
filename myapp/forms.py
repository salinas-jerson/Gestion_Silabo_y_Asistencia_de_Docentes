from django import forms

class crearTarea(forms.Form):
    title = forms.CharField(label="Titulo:", max_length=200)
    descripcion = forms.CharField(label = "Descripcion.:", widget=forms.Textarea)

class login(forms.Form):
    usuario = forms.CharField(label="Usuario:", max_length=50)
    contrasena = forms.CharField(label = "Contraseña:", max_length=50)