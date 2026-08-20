from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Product, ProductColor, ProductSize


def add_to_cart(request, id):

    if request.method != "POST":
        return redirect("product_detail", id=id)

    product = get_object_or_404(
        Product,
        pk=id,
    )

    color_id = request.POST.get("color")

    size_id = request.POST.get("size")

    qty = int(request.POST.get("qty", 1))

    if not size_id:

        messages.error(
            request,
            "Please select a size.",
        )

        return redirect(
            "product_detail",
            id=id,
        )

    product_size = get_object_or_404(
        ProductSize,
        pk=size_id,
        color__product=product,
    )

    cart = request.session.get(
        "cart",
        {},
    )

    key = str(product_size.id)

    if key in cart:

        cart[key]["qty"] += qty

        if cart[key]["qty"] > product_size.stock:
            cart[key]["qty"] = product_size.stock

    else:

        cart[key] = {

            "product_id": product.id,
            "size_id": product_size.id,
            "qty": min(qty, product_size.stock),
            "color_id": color_id,

        }

    request.session["cart"] = cart
    request.session.modified = True

    cart_count = sum(
        item["qty"]
        for item in cart.values()
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({

            "success": True,

            "cart_count": cart_count,

            "message": "Added to cart",

        })

    messages.success(
        request,
        "Product added to cart.",
    )

    return redirect("cart")


from main.utils.cart import get_cart_data


def cart_view(request):
    context = get_cart_data(request)

    return render(
        request,
        "main/cart/cart.html",
        context,
    )

@require_POST
def update_cart(request):

    key = request.POST.get("key")
    action = request.POST.get("action")

    cart = request.session.get("cart", {})

    if key not in cart:

        return JsonResponse({

            "success": False,

            "message": "Item not found.",

        })

    item = cart[key]

    try:

        product_size = ProductSize.objects.select_related(
            "color__product",
        ).get(
            id=item["size_id"],
        )

    except ProductSize.DoesNotExist:

        return JsonResponse({

            "success": False,

            "message": "Product not found.",

        })

    qty = item["qty"]

    if action == "increase":

        if qty < product_size.stock:

            qty += 1

    elif action == "decrease":

        if qty > 1:

            qty -= 1

    item["qty"] = qty

    cart[key] = item

    request.session["cart"] = cart
    request.session.modified = True

    subtotal = product_size.color.product.final_price * qty

    cart_total = 0
    cart_count = 0

    for value in cart.values():

        try:

            size = ProductSize.objects.select_related(
                "color__product",
            ).get(
                id=value["size_id"],
            )

            cart_total += (
                size.color.product.final_price *
                value["qty"]
            )

            cart_count += value["qty"]

        except ProductSize.DoesNotExist:

            continue

    return JsonResponse({

        "success": True,

        "qty": qty,

        "subtotal": subtotal,

        "total": cart_total,

        "cart_count": cart_count,

        "stock": product_size.stock,

    })


@require_POST
def remove_cart(request):

    key = request.POST.get("key")

    cart = request.session.get(
        "cart",
        {},
    )

    if key not in cart:

        return JsonResponse({

            "success": False,

        })

    del cart[key]

    request.session["cart"] = cart
    request.session.modified = True

    cart_total = 0
    cart_count = 0

    for value in cart.values():

        try:

            size = ProductSize.objects.select_related(
                "color__product",
            ).get(
                id=value["size_id"],
            )

            cart_total += (

                size.color.product.final_price *
                value["qty"]

            )

            cart_count += value["qty"]

        except ProductSize.DoesNotExist:

            continue

    return JsonResponse({

        "success": True,

        "total": cart_total,

        "cart_count": cart_count,

    })