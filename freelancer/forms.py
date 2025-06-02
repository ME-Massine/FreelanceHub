from django import forms
from multiselectfield import MultiSelectFormField

from freelancer.models import Freelancer, Service
from client import models


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['content']


class ProfileForm(forms.ModelForm):
    languages = MultiSelectFormField(
        choices=Freelancer.LANGUAGE_CHOICES,
        flat_choices=[choice[0] for choice in Freelancer.LANGUAGE_CHOICES],
        required=False)

    class Meta:
        model = Freelancer
        fields = ['pfp', 'bio', 'portfolio_url', 'location', 'languages']
        widgets = {
            'pfp': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image_url', 'price']
