from django import forms
from django.forms import ModelForm
from users.models import User
from kitchen.models import Kitchen, Day, Item
from django.forms import modelformset_factory, formset_factory
from django.db import transaction

class KitchenCreateForm(ModelForm):
    days = forms.ModelMultipleChoiceField(
        queryset= Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Kitchen
        fields = ["name", "start_time", "end_time", "days", "image",]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}), 
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            "name": "Kitchen Name", 
            "days": "Open Days"
        }


    def save(self, commit=True):
        kitchen = super().save(commit=False)
        return kitchen

ItemFormSet = modelformset_factory(Item, fields=('name', 'isVeg', 'price'), extra=1)

class ItemAddForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "isVeg", "price"]
        labels = {
            "name": "Item Name",
            "isVeg": "Is Vegeterian",
        }


    def save(self, commit=True):
        item = super().save(commit=False)
        return item


class AddItemToCartForm(forms.Form):
    add_to_cart = forms.BooleanField(label="Add to cart")

    class Meta:
        widgets = {
            "add_to_cart": forms.CheckboxInput(attrs={"class": "form-check-input mt-2" })
        }

