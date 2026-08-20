from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError
from main.services.inventory_service import InventoryService
from main.payment.signatures import (
    ClickSignatureService,
    PaymeSignatureService,
)
from main.models import Payment
from main.services.order_status_service import OrderStatusService
from main.services.payment_service import PaymentService
from main.services.payment_transaction_service import (
    PaymentTransactionService,
)
from main.utils.activity import create_activity
from main.utils.notification import create_notification
from main.utils.telegram import send_telegram_message


class PaymentCallbackService:

    @classmethod
    @transaction.atomic
    def process(
        cls,
        *,
        provider,
        payment_id,
        transaction_id,
        amount,
        signature,
        ):

        # 1. Signature
        cls.verify_signature(
            provider,
            payment_id,
            transaction_id,
            amount,
            signature,
        )

        # 2. Payment
        payment = cls.get_payment(
            payment_id,
        )

        # 3. Amount
        cls.verify_amount(
            payment,
            amount,
        )

        # 4. Status
        cls.verify_status(
            payment,
        )

        # 5. Transaction

        payment_transaction = cls.verify_transaction(

            payment=payment,

            provider=provider,

            transaction_id=transaction_id,

            request_data={

                "provider": provider,

                "payment_id": payment_id,

                "transaction_id": transaction_id,

                "amount": amount,

            },

        )

        if PaymentTransactionService.is_processed(

                payment_transaction,

        ):
            return {

                "success": True,

                "payment_id": payment.id,

                "order_id": payment.order.id,

                "message": "Duplicate callback ignored.",

            }

        # 5. Transaction
        if PaymentTransactionService.is_processed(

                payment_transaction,

        ):
            return {

                "success": True,

                "payment_id": payment.id,

                "order_id": payment.order.id,

                "message": "Duplicate callback ignored.",

            }

        try:

            # 6. Payment Paid
            PaymentService.mark_paid(
                payment,
            )

            # 7. Transaction Success
            PaymentTransactionService.success(

                payment_transaction,

                {

                    "message": "Payment completed successfully",

                },

            )

        except Exception as e:

            PaymentService.mark_failed(
                payment,
                str(e),
            )

            InventoryService.release(
                payment.order,
            )

            PaymentTransactionService.failed(

                payment_transaction,

                {

                    "error": str(e),

                },

            )





            raise

        # 8. Order Confirm
        cls.confirm_order(
            OrderStatusService.change_status(

                order=payment.order,

                new_status="confirmed",

                user=None,

            )
        )


        # 9. Activity Log
        cls.create_logs(
            payment,
        )

        # 10. Notification
        cls.send_notifications(
            payment,
        )

        return {

            "success": True,

            "payment_id": payment.id,

            "order_id": payment.order.id,

        }

    @staticmethod
    def verify_signature(
            provider,
            payment_id,
            transaction_id,
            amount,
            signature,
    ):

        if provider == "click":

            return ClickSignatureService.verify(

                payment_id=payment_id,

                transaction_id=transaction_id,

                amount=amount,

                signature=signature,

            )

        elif provider == "payme":

            return PaymeSignatureService.verify(

                payment_id=payment_id,

                transaction_id=transaction_id,

                amount=amount,

                signature=signature,

            )

        elif provider == "cash":

            return True

        raise ValidationError(
            "Unknown payment provider."
        )

    @staticmethod
    def get_payment(payment_id):

        try:

            return Payment.objects.select_related(
                "order",
                "order__user",
            ).get(
                id=payment_id,
            )

        except Payment.DoesNotExist:

            raise ValidationError(
                "Payment not found."
            )


    @staticmethod
    def verify_amount(
            payment,
            amount,
    ):

        if payment.amount != Decimal(str(amount)):
            raise ValidationError(
                "Payment amount does not match order total."
            )


    @staticmethod
    def verify_status(payment):

        if payment.status == "paid":
            raise ValidationError(
                "Payment has already been completed."
            )

        if payment.status == "expired":
            raise ValidationError(
                "Payment has expired."
            )

        if payment.status == "cancelled":
            raise ValidationError(
                "Payment has been cancelled."
            )

        if payment.status == "failed":
            raise ValidationError(
                "Payment has already failed."
            )







    @staticmethod
    def verify_transaction(
            payment,
            provider,
            transaction_id,
            request_data=None,
    ):

        return PaymentTransactionService.create(

            payment=payment,

            provider=provider,

            transaction_id=transaction_id,

            request_data=request_data,

        )


    @staticmethod
    def confirm_order(payment):

        OrderStatusService.change_status(

            order=payment.order,

            new_status="confirmed",

            user=None,

        )

    @staticmethod
    def create_logs(payment):

        order = payment.order

        if order.user:

            create_activity(

                order.user,

                "payment_completed",

                f"Payment #{payment.id} completed.",

            )

    @staticmethod
    def send_notifications(payment):

        order = payment.order

        if order.user:

            create_notification(

                order.user,

                "Payment Successful",

                f"Your payment for Order #{order.id} has been confirmed.",

            )

        send_telegram_message(

            f"""
✅ PAYMENT SUCCESS

Order: #{order.id}

Payment: #{payment.id}

Amount: {payment.amount}

Provider: {payment.provider}
"""

        )