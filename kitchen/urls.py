from django.urls import path, include
from . import views 

urlpatterns = [
    path("<int:user_id>/create", views.create_kitchen, name="kitchen_create"),
    path("<int:pk>", views.kitchen_detail, name="kitchen_detail"),
]