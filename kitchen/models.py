from django.db import models
from django.conf import settings


class Day(models.Model):
    MONDAY = 1
    TUESDSDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7 

    DAY_CHOICES = (
        (MONDAY, "Monday"),
        (TUESDSDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    )

    id = models.PositiveIntegerField(choices=DAY_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Kitchen(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.ManyToManyField(Day, related_name="days")
    image = models.ImageField(upload_to="kitchen_images")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        

    def __str__(self):
        return f"Kitchen({self.name})"

class Item(models.Model):
    name = models.CharField(max_length=250)
    isVeg = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    kithen = models.ForeignKey(Kitchen, related_name="items", on_delete=models.CASCADE)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"Item({self.name})"



