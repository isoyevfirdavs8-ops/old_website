

from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from main.models import Payment
from main.services.inventory_service import InventoryService


class PaymentService:
    @staticmethod
    def verify(request):
        return {

            "success": True,

        }


        
    @staticmethod
    @transaction.atomic
    def create_payment(order):

        payment = Payment.objects.create(

            order=order,

            amount=order.total_price,

            provider=order.payment_method,

            status="pending",

        )

        return payment

    @staticmethod
    def mark_waiting(payment):

        payment.status = "waiting"

        payment.save(

            update_fields=["status"]

        )

    @staticmethod
    def mark_paid(payment):

        payment.status = "paid"

        payment.save(

            update_fields=["status"]

        )


    @staticmethod
    def mark_failed(
            payment,
            reason="",
    ):
        payment.status = "failed"

        payment.failure_reason = reason

        payment.save(

            update_fields=[

                "status",

                "failure_reason",

            ]

        )

    @staticmethod
    def cancel(payment):

        payment.status = "cancelled"

        payment.save(

            update_fields=["status"]

        )

    @staticmethod
    def retry(order):
        Payment.objects.filter(

            order=order,

            status="pending",

        ).update(

            status="cancelled",

        )

        return Payment.objects.create(

            order=order,

            amount=order.total_price,

            provider=order.payment_method,

            status="pending",

        )

    @staticmethod
    def expire_old_payments():
        expire_time = timezone.now() - timedelta(
            minutes=20,

        )


        payments = Payment.objects.filter(

            status="waiting",

            created_at__lt=expire_time,

        )

        for payment in payments:
            payment.status = "expired"

            payment.failure_reason = (
                "Payment timeout."
            )

            payment.save(

                update_fields=[

                    "status",

                    "failure_reason",

                ]

            )

            InventoryService.release(
                payment.order,
            )

