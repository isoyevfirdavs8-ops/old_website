from main.utils.notification import create_notification


class NotificationService:

    @staticmethod
    def order_created(user, order):

        create_notification(

            user,

            "Order Created",

            f"Order #{order.id} created."

        )