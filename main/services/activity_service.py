from main.utils.activity import create_activity


class ActivityService:

    @staticmethod
    def order_created(order):

        if not order.user:
            return

        create_activity(

            order.user,

            "order_created",

            f"Order #{order.id} created."

        )

    @staticmethod
    def order_cancelled(order):

        if not order.user:
            return

        create_activity(

            order.user,

            "order_cancelled",

            f"Order #{order.id} cancelled."

        )

    @staticmethod
    def order_delivered(order):

        if not order.user:
            return

        create_activity(

            order.user,

            "order_delivered",

            f"Order #{order.id} delivered."

        )