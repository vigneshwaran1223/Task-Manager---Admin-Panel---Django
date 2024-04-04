from django.contrib.auth.models import User
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email' ,'password1', 'password2']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# Create a task

class CreateTaskForm(forms.ModelForm):
    class Meta:

        model = Task
        fields = ['title','content',]
        exclude = ['user',]

