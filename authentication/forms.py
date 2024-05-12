from django import forms
from django.contrib.auth.models import User
from authentication.models import UserProfileInformation

class LoginModalForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder' : 'Enter your username',
                                   'class' : 'form-control'
                               }))
    password = forms.CharField(label="Password", required=True, 
                               widget=forms.PasswordInput(attrs={
                                   'placeholder' : 'Enter your password',
                                   'class' : 'form-control'
                               })) 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=25, required=True)

    class Meta():
        model = User
        fields = ('username',)

class RegsisterModalForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta():
        model = UserProfileInformation
        fields = ('profile_picture',)

