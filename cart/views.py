from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal

# Create your views here.

def cart_detail(request):
    cart = request.session.get("cart", None)
    if cart is None:
        cart = {} 
        request.session["cart"] = cart 
    
    return render(request, "cart/detail.html", {"cart": cart})


def cart_remove(request, item):
    cart = request.session.get("cart", None)
    if cart is None:
        messages.danger(request, f'No Item to remove!')
        request.session["cart"] = {}
        return redirect("cart_detail")
    else:
        ex_item = cart.get(item, None)
        if item is None:
            return redirect("cart_detail")
        cart.pop(item, None)
        request.session["cart"] = cart 
        request.session.modified = True 
        messages.success(request, f'Item has been removed!')
        return redirect("cart_detail")


def check_out(request):
    if not request.user.is_authenticated:
        messages.warning(request, f'Please Sign in before proceeding to checkout')
        return redirect("login")
    if request.user.is_kitchen:
        messages.warning(request,"Please sign in as customer")
        return redirect("login")

    cart = request.session.get("cart", None)
    if cart is None:
        messages.danger(request, f'No Item to Buy!')
        return redirect("cart_detail")
    else:
        total_price = sum([Decimal(i["price"]) for i in cart.values()])
        total_items = len(cart)
        request.session["cart"] = {} 
        request.session.modified = True
        messages.success(request, f'Your order({total_items} Items) will be ready in 20 minutes!')
        messages.success(request, f'Total Price: {total_price}')
        return redirect("home")