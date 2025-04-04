from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Emailová adresa")
    phone_number = forms.CharField(required=True, label="Telefonní číslo")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class CustomUserForm(UserChangeForm):
    password = None  # nechceme zobrazovat pole pro heslo

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'membership_paid', 'phone_number']