from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView
from django.contrib import messages

from .forms import KitchenCreateForm, ItemAddForm, ItemFormSet, AddItemToCartForm, AddToCartForm
from users.models import User
from kitchen.models import Kitchen, Item
from django.forms import formset_factory

def add(cart, item, quantity=1):
    item["quantity"] = quantity
    item["price"] = str(item["price"])
    cart[item["id"]] = item
    return cart 


def get_cart(request):
    cart = request.session.get("cart", None)
    if cart is None:
        cart = {} 
        request.session["cart"] = cart
        request.session.modified = True
    return cart

def kitchen_detail(request, pk):
    cart = get_cart(request)
    cart_form = AddToCartForm()
    kitchen = get_object_or_404(Kitchen, pk=pk)
    items = kitchen.items.all()
    item_formset = formset_factory(AddItemToCartForm, extra=5, max_num=6)
    formset = item_formset(initial=[
        {"id": i.id, "name": i.name, "price": i.price, "kitchen": i.kithen.user.id, "add_to_cart": False} for i in items 
    ])
    zipped_items = zip(items, formset)
    if request.method == "POST":
        cart = get_cart(request)
        cart_form = AddToCartForm(request.POST)
        formset = item_formset(request.POST)
        if formset.is_valid():
            for f in formset:
                data = f.cleaned_data
                if data and data["add_to_cart"]:
                    add(cart, data)
            request.session.modified = True 
            messages.success(request, f'You have {len(cart)} items to your cart!')
            return redirect("cart_detail")
    return render(request, "kitchen/detail.html", {"kitchen": kitchen, "zipped_items": zipped_items, "formset": formset, "cart_form": cart_form})

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
                messages.success(request, f'Your Kitchen has been been created!')
            return redirect("home")
    else:
        formset = ItemFormSet(queryset=Item.objects.none())
        form = KitchenCreateForm()
    return render(request, "kitchen/create.html", {"user_id": user_id, "form": form, "formset": formset})
        

