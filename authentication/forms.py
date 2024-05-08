from django import forms

class login_modal_form(forms.Form):
    username = forms.CharField(label="username", max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)