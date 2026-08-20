from django.core.exceptions import ValidationError
from django.db import transaction

from main.models import OrderStatusHistory
from main.utils import create_activity, create_notification


class OrderStatusService:

    TRANSITIONS = {

        "pending": [
            "confirmed",
            "cancelled",
        ],

        "confirmed": [
            "preparing",
            "cancelled",
        ],

        "preparing": [
            "shipped",
        ],

        "shipped": [
            "delivered",
        ],

        "delivered": [],

        "cancelled": [],
    }

    @classmethod
    @transaction.atomic
    def change_status(
        cls,
        *,
        order,
        new_status,
        user=None,
        note="",
    ):

        allowed = cls.TRANSITIONS.get(
            order.status,
            [],
        )

        if new_status not in allowed:

            raise ValidationError(

                f"Cannot change order status "

                f"from '{order.status}' "

                f"to '{new_status}'."

            )

        old_status = order.status

        order.status = new_status

        order.save(
            update_fields=[
                "status",
            ]
        )

        OrderStatusHistory.objects.create(

            order=order,

            old_status=old_status,

            new_status=new_status,

            changed_by=user,

            note=note,

        )

        if order.user:

            create_notification(

                order.user,

                "Order Status Updated",

                f"Your order is now {new_status.title()}.",

            )

        if user:

            create_activity(

                user,

                "order_status",

                f"Order #{order.id}: "

                f"{old_status} → {new_status}",

            )

        return order