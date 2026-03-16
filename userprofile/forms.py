from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'datepicker',
                'placeholder': 'DD/MM/YYYY'
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['birthdate', 'gender', 'bio', 'avatar']