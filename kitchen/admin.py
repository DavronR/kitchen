from django.contrib import admin
from .models import Kitchen, Item, Day 

@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_filter = ['created', 'updated']


 

admin.site.register(Day)
admin.site.register(Item)