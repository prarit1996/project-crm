from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your Username',
        'class':'w-full my-4 py-4 px-6 rounded-xl bg-gray-100',
        'autocomplete': 'off'
    }))
    password =  forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your Password',
        'class':'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'
    }))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={
        'placeholder':'Your Username',
        'class':'w-full mx-3 my-4 py-4 px-6 rounded-xl bg-gray-100',
        'autocomplete': 'off'
    }))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email',
        'class': 'w-full mx-3  my-4 py-4 px-6 rounded-xl bg-gray-100',
        'autocomplete': 'off'
    }))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={
        'placeholder':'Your Password',
        'class':'w-full mx-3 my-4 py-4 px-6 rounded-xl bg-gray-100'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Re-Type Password',
        'class':'w-full mx-3 my-4 py-4 px-6 rounded-xl bg-gray-100'
    }))