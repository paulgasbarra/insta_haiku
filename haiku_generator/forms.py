# haiku_generator/forms.py

from django import forms
from .models import Haiku

class HaikuForm(forms.ModelForm):
    class Meta:
        model = Haiku
        fields = ['text', 'image']
