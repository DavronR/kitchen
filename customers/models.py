from django.db import models
from django.conf import settings
from kitchen.models import Item 

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"Customer({self.user.username})"

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_complete = models.BooleanField(default=False)
    is_pickup = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Order(Customer: {self.customer.user.username})"