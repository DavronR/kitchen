from django.urls import path
from . import views 

urlpatterns = [
    path("detail", views.cart_detail, name="cart_detail"),
    path("remove/<item>", views.cart_remove, name="cart_remove"),
    path("checkout", views.check_out, name="check_out"),
]