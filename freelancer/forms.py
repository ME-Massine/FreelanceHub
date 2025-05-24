from django import forms
from django.forms import CheckboxSelectMultiple, SelectMultiple
from multiselectfield import MultiSelectFormField

from freelancer.models import Freelancer
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
        fields = ['bio', 'portfolio_url', 'location', 'languages']