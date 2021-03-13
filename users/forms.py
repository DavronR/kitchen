from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import User
from kitchen.models import Kitchen, Day


class KitchenSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2", ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_kitchen = True
        user.is_active = False
        user.save()
        return user


class CustomerSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    password = forms.CharField(label="Password", max_length=200, widget=forms.PasswordInput)


