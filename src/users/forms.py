from django import forms


# Create a login form to use in the login view
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
