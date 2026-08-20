from main.models import Product, ProductColor, ProductSize


def get_cart_data(request):
    session_cart = request.session.get("cart", {})

    cart = {}
    cart_total = 0
    cart_count = 0
    keys_to_delete = []

    for key, value in session_cart.items():

        try:
            product = Product.objects.prefetch_related(
                "gallery"
            ).get(
                id=value["product_id"]
            )

            size = ProductSize.objects.select_related(
                "color"
            ).get(
                id=value["size_id"]
            )

        except (
            Product.DoesNotExist,
            ProductSize.DoesNotExist,
            KeyError,
        ):
            keys_to_delete.append(key)
            continue

        qty = value["qty"]

        if qty > size.stock:
            qty = size.stock
            session_cart[key]["qty"] = qty

        subtotal = product.final_price * qty

        color = None

        if value.get("color_id"):
            color = ProductColor.objects.filter(
                id=value["color_id"]
            ).first()

        cart[key] = {
            "product": product,
            "size": size,
            "color": color,
            "qty": qty,
            "price": product.final_price,
            "total": subtotal,
        }

        cart_total += subtotal
        cart_count += qty

    for key in keys_to_delete:
        session_cart.pop(key, None)

    request.session["cart"] = session_cart
    request.session.modified = True

    return {
        "cart": cart,
        "cart_total": cart_total,
        "cart_count": cart_count,
    }