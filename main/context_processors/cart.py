def cart(request):

    cart = request.session.get("cart", {})

    total_items = sum(

        item["qty"]

        for item in cart.values()

    )

    return {

        "cart_count": total_items

    }

