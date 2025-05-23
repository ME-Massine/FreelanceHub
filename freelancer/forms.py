from django import forms
from freelancer.models import Freelancer
from client import models



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['location', 'bio', 'portfolio_url']