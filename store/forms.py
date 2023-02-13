from django import forms
from django.forms import ModelForm
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# creating a form

class productform(ModelForm):
     class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'digital']


class CreateUserForm(UserCreationForm):
	class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']