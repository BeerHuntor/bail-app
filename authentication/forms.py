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

class UserRegisterModalForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control',
                                                'placeholder' : 'Enter a valid username'
                                                }),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control',
                                                    'placeholder' : 'Enter a valid password',
                                                }),
            'email' : forms.EmailInput(attrs={'class' : 'form-control',
                                              'placeholder' : 'Enter a valid email address',
                                              }),
        }