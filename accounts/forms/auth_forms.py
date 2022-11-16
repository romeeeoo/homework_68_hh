from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField


class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput
    )
    is_corporate = forms.BooleanField(required=False
    )
    avatar = forms.ImageField(
        required=False)
    phone_number = PhoneNumberField(
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "is_corporate", "avatar", "phone_number")


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Your username')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
