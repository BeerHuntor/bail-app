from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter a valid password',
            'required' : True,
            'pattern' : '(?=.*[a-z])(?=.*[A-Z]).{8,}', # Basic pattern for password validation
            'title' : 'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters!',
            'type' : 'password'
            }) 
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm Password',
            'required' : True,
            'type' : 'password'
            })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter a valid username',
                'required' : True,
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter a valid email address',
                'required' : True,
                'type' : 'email'
                }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        does_exist = User.objects.filter(email=email)
        if len(does_exist) != 0:
            raise ValidationError("Email Already in use, please use another email. ")
        else:
            return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user