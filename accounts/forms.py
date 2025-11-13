from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# This form will handle user registration (signup)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

# This handles login — we can use Django’s built-in one, but we include it for clarity
class CustomUserLoginForm(AuthenticationForm):
    pass