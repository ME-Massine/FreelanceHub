from django import forms
from client import models

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['content']