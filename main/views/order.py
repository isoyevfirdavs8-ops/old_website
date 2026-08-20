from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from main.models import Order, OrderItem, Payment
from main.utils.cart import get_cart_data


@transaction.atomic
def create_order(request):

    context = get_cart_data(request)

    if not context["cart"]:
        return redirect("cart")
    order = Order.objects.create(

        user=request.user
        if request.user.is_authenticated
        else None,

        full_name=request.POST["full_name"],

        phone=request.POST["phone"],

        email=request.POST.get("email"),

        address=request.POST["address"],

        note=request.POST.get("note", ""),

        payment_method=request.POST["payment_method"],

        delivery_type=request.POST["delivery_type"],

        delivery_price=0,

        discount=0,
    )
    for item in context["cart"].values():

        OrderItem.objects.create(

            order=order,

            product=item["product"],

            size=item["size"],

            quantity=item["qty"],

            price=item["price"],

        )

        for item in context["cart"].values():
            OrderItem.objects.create(

                order=order,

                product=item["product"],

                size=item["size"],

                quantity=item["qty"],

                price=item["price"],

            )

            Payment.objects.create(

                order=order,

                amount=order.total_price,

                provider=order.payment_method,

            )

            request.session["cart"] = {}

            request.session.modified = True
            return redirect(
                "checkout_success",
                order.id,
            )




@login_required
@require_POST
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    order.delete()
    return redirect('profile')