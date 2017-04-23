from django import forms

from .models import OfertaTrabajo


class OfertasForm(forms.ModelForm):
    class Meta:
        model = OfertaTrabajo
        fields = ('title', 'descripcion',)