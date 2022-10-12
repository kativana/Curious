from pyexpat import model
from django import forms
from .models import Cueet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class CueetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Cueet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Cueet
        exclude = ("user",)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget = forms.PasswordInput())



class RegistrationForm(UserCreationForm):   
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields 

  
