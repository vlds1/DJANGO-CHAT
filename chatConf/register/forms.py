from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        labels = {'email': 'Email'}
        help_texts = {'username': None}
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'auth_input'}),
            'username': forms.TextInput(attrs={'class': 'auth_input'}),
            'password': forms.PasswordInput(attrs={'class': 'auth_input'}),
        }



class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        help_texts = {'username': None}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'auth_input'}),
            'password': forms.PasswordInput(attrs={'class': 'auth_input'})
        }
