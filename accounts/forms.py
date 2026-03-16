from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from userprofile.models import Profile


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

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
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        required=False
    )

    role = forms.ChoiceField(
    choices=Profile.ROLE_CHOICES,
    required=True
    )

    bio = forms.CharField(
    required=False,
    max_length=350,   # 350 characters approx ~70 words
    widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': 'Tell us about yourself…',
        'maxlength': 350
    })
)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'gender',
            'role',
            'bio',
            'avatar',
            'password1',
            'password2',
        )

class UserLoginForm(AuthenticationForm):
    pass
