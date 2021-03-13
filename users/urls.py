from django.urls import path, include
from . import views 

urlpatterns = [
    path("kitchen/register", views.KitchenSignupView.as_view(), name="kitchen_register"),
    path("customer/register", views.CustomerSignupView.as_view(), name="customer_register"),
    path("account/", views.sign_up, name="sign_up"),
    path("account/login", views.user_login, name="login"),
    path("account/logout", views.logout_user, name="logout"),
    path("", views.home, name="home"),
]