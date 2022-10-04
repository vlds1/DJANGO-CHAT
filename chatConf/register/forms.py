from django.contrib.auth.models import User
from django import forms
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')