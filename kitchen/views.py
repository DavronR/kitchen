from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView

from .forms import KitchenCreateForm, ItemAddForm, ItemFormSet, AddItemToCartForm
from users.models import User
from kitchen.models import Kitchen, Item
from django.forms import formset_factory


def kitchen_detail(request, pk):
    kitchen = get_object_or_404(Kitchen, pk=pk)
    items = kitchen.items.all()
    item_formset = formset_factory(AddItemToCartForm, extra=5, max_num=6)
    formset = item_formset()
    zipped_items = zip(items, formset)
    return render(request, "kitchen/detail.html", {"kitchen": kitchen, "zipped_items": zipped_items})

def create_kitchen(request, user_id): 
    if request.method == "POST":
        form = KitchenCreateForm(request.POST, request.FILES)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            user = User.objects.get(pk=user_id)
            kitchen = form.save()
            kitchen.user = user
            kitchen.user.is_active = True
            kitchen.save() 
            kitchen.days.add(*form.cleaned_data.get("days"))
            kitchen.save() 
            user.save()
            for f in formset:
                item = f.save(commit=False)
                item.kithen = kitchen 
                item.save()
            return redirect("home")
    else:
        formset = ItemFormSet(queryset=Item.objects.none())
        form = KitchenCreateForm()
    return render(request, "kitchen/create.html", {"user_id": user_id, "form": form, "formset": formset})
        
