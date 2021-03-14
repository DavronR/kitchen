from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib import messages

from .forms import KitchenSignupForm, CustomerSignupForm, LoginForm
from .models import User
from kitchen.models import Kitchen


class KitchenSignupView(CreateView):
    model = User 
    form_class = KitchenSignupForm
    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "kitchen"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('kitchen_create', user.id)


class CustomerSignupView(CreateView):
    model = User 
    form_class = CustomerSignupForm
    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "customer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(request, f'Your account has been created!')
        return redirect('home')


def sign_up(request):
    return render(request, "users/account.html")


def home(request):
    kitchens = Kitchen.objects.all()
    return render(request, "users/home.html", {"kitchens": kitchens})

def user_login(request):
    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username", None)
            password = data.get("password", None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    return render(request, "users/login.html",{"form": form})


def logout_user(request):
    messages.success(request, f'You have been logged out.')
    logout(request)
    return redirect("home")