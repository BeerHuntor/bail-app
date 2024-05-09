from django import forms

class LoginModalForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)