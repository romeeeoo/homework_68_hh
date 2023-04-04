from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput
    )
    is_corporate = forms.BooleanField(
        required=False)
    avatar = forms.ImageField(
        required=False)
    phone_number = PhoneNumberField(required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "is_corporate", "avatar", "phone_number")


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Your username')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number']
