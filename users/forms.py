from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import User
from kitchen.models import Kitchen, Day


class KitchenSignupForm(UserCreationForm):
    sec1 = forms.CharField(label="Security Question", 
                    widget = forms.TextInput(attrs={'readonly':'readonly', "class": "form-control"}), initial="What is your pet's name?")
    sec2 = forms.CharField(label="Security Question", 
                    widget = forms.TextInput(attrs={'readonly':'readonly', "class": "form-control"}), initial="What is your childhood nickname?")
    answer1 = forms.CharField(label="Answer", max_length=200)
    answer2 = forms.CharField(label="Answer", max_length=200)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", 
                        "password1", "password2", "sec1", "answer1", "sec2", "answer2", ]


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_kitchen = True
        user.is_active = False
        user.save()
        return user


class CustomerSignupForm(UserCreationForm):
    sec1 = forms.CharField(label="Security Question", 
                    widget = forms.TextInput(attrs={'readonly':'readonly', "class": "form-control"}), initial="What is your pet's name?")
    sec2 = forms.CharField(label="Security Question", 
                    widget = forms.TextInput(attrs={'readonly':'readonly', "class": "form-control"}), initial="What is your childhood nickname?")
    answer1 = forms.CharField(label="Answer", max_length=200)
    answer2 = forms.CharField(label="Answer", max_length=200)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", 
                        "password1", "password2", "sec1", "answer1", "sec2", "answer2", ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200)
    password = forms.CharField(label="Password", max_length=200, widget=forms.PasswordInput)


