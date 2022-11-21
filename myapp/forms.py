from django import forms

class crearTarea(forms.Form):
    title = forms.CharField(label="Titulo:", max_length=200)
    descripcion = forms.CharField(label = "Descripcion.:", widget=forms.Textarea)