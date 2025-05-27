from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from client.models import Mission


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First name"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last name"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )



class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['title', 'description', 'category', 'level' ,'price']


