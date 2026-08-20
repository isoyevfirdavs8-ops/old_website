from django.core.exceptions import ValidationError
from django.db import transaction

from main.models import ProductSize, StockMovement


class StockService:

    @staticmethod
    @transaction.atomic
    def decrease_stock(order, cart):

        for item in cart.values():

            size = ProductSize.objects.select_for_update().get(
                pk=item["size"].pk
            )

            qty = item["qty"]

            if qty > size.stock:

                raise ValidationError(
                    f"{size.color.product.title} ({size.size}) stock is not enough."
                )

            before = size.stock

            size.stock -= qty

            size.save(update_fields=["stock"])

            StockMovement.objects.create(

                product_size=size,

                order=order,

                movement_type="sale",

                quantity=qty,

                before_stock=before,

                after_stock=size.stock,

                note="Customer order",

            )