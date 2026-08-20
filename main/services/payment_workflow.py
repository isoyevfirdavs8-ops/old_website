from main.services.payment_service import PaymentService
from main.services.notification_service import NotificationService
from main.services.activity_service import ActivityService
from main.services.telegram_service import TelegramService
from main.services.order_log_service import OrderLogService


class PaymentWorkflow:

    @staticmethod
    def payment_success(payment, transaction_id=""):

        PaymentService.mark_paid(
            payment,
            transaction_id,
        )

        order = payment.order

        OrderLogService.create(

            order=order,

            old_status="Waiting Payment",

            new_status="Paid",

            user=None,

            comment="Payment successful",

        )

        NotificationService.order_created(
            order,
        )

        ActivityService.order_created(
            order,
        )

        TelegramService.send_payment_success(
            order,
        )

        return payment

    @staticmethod
    def payment_failed(payment):

        PaymentService.mark_failed(
            payment,
        )

        OrderLogService.create(

            order=payment.order,

            old_status="Waiting Payment",

            new_status="Cancelled",

            comment="Payment failed",

        )

        return payment

    @staticmethod
    def payment_cancelled(payment):

        PaymentService.cancel(
            payment,
        )

        OrderLogService.create(

            order=payment.order,

            old_status="Waiting Payment",

            new_status="Cancelled",

            comment="Payment cancelled",

        )

        return payment