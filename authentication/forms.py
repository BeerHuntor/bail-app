from django import forms

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
