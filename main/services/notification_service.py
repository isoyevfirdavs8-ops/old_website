from main.utils.notification import create_notification


class NotificationService:

    @staticmethod
    def order_created(order):

        if not order.user:
            return

        create_notification(

            order.user,

            "Order Created",

            (
                f"Your order #{order.id} "
                "has been received successfully."
            ),

        )

    @staticmethod
    def order_processing(order):

        if not order.user:
            return

        create_notification(

            order.user,

            "Order Processing",

            (
                f"Order #{order.id} "
                "is being prepared."
            ),

        )

    @staticmethod
    def order_shipping(order):

        if not order.user:
            return

        create_notification(

            order.user,

            "Order Shipping",

            (
                f"Order #{order.id} "
                "has been shipped."
            ),

        )

    @staticmethod
    def order_delivered(order):

        if not order.user:
            return

        create_notification(

            order.user,

            "Order Delivered",

            (
                f"Order #{order.id} "
                "has been delivered."
            ),

        )

    @staticmethod
    def order_cancelled(order):

        if not order.user:
            return

        create_notification(

            order.user,

            "Order Cancelled",

            (
                f"Order #{order.id} "
                "has been cancelled."
            ),

        )