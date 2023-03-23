from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from .models import *
from django.contrib.auth.models import User

# user form for the django user model
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': TextInput(attrs={
                'id': "username",
                'class': "form-control",
                'placeholder': 'Enter your username',
                }),
            'username.label_tag': TextInput(attrs={
                'class': "small mb-1",
                'value': 'Username',
                }),
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Enter your first name',
                }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Enter your last name',
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Enter your email address'
                }),
            'password': PasswordInput(attrs={
                'class': "form-control",
                'placeholder': 'Enter your password'
                })
        }
        

# user form for the django user model --extended fields
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('image', 'phone_number', 'dob')


# updateuser form for the django user model
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# updateuser form for the django user model --extended fields
class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = UserAccount
        fields = ['image', 'phone_number', 'dob']