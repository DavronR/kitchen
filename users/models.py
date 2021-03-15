from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_kitchen = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Answer(models.Model):
    user = models.ForeignKey(User, related_name="answers", on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, default="Yes")

    def __str__(self):
        return self.answer

