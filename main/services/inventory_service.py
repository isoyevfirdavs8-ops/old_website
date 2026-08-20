from django.db import transaction
from django.core.exceptions import ValidationError


class InventoryService:

    @staticmethod
    @transaction.atomic
    def reserve(order):
        return True

        # for item in order.items.select_related("size"):
        #
        #     product_size = item.size
        #
        #     if product_size.stock < item.quantity:
        #
        #         raise ValidationError(
        #             f"{item.product.title} ({product_size.size}) is out of stock."
        #         )
        #
        #     product_size.stock -= item.quantity
        #
        #     product_size.save(
        #         update_fields=[
        #             "stock",
        #         ]
        #     )

    @staticmethod
    @transaction.atomic
    def release(order):

        for item in order.items.select_related("size"):

            product_size = item.size

            product_size.stock += item.quantity

            product_size.save(
                update_fields=[
                    "stock",
                ]
            )

    @staticmethod
    def commit(order):
        """
        Stock reserve qilinganligi sababli
        qo'shimcha amal kerak emas.

        Kelajakda warehouse yoki audit log
        qo'shilsa shu yer ishlatiladi.
        """
        return True