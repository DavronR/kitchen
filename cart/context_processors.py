
def cart(request):
    cart = request.session.get("cart", None)
    if cart is None:
        cart = {}
        request.session["cart"] = cart  
    return {"cart": cart}
