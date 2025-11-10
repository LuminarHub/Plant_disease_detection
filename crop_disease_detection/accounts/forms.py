from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    is_farmer = forms.BooleanField(required=False, initial=True, label="Farmer")

    class Meta:
        model = CustUser
        fields = ['username', 'email', 'password1', 'password2', 'is_farmer']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
