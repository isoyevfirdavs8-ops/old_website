
from django.utils import timezone

from main.models import PaymentTransaction


class PaymentTransactionService:

    @staticmethod
    def create(
        *,
        payment,
        provider,
        transaction_id,
        request_data=None,
    ):
        transaction = PaymentTransaction.objects.filter(

            transaction_id=transaction_id,

        ).first()

        if transaction:
            return transaction

        return PaymentTransaction.objects.create(

            payment=payment,

            provider=provider,

            transaction_id=transaction_id,

            request_data=request_data or {},

            status="pending",

        )


    @staticmethod
    def success(
            transaction,
            response_data=None,
    ):
        transaction.status = "success"

        transaction.response_data = response_data or {}

        transaction.processed_at = timezone.now()

        transaction.save(

            update_fields=[

                "status",

                "response_data",

                "processed_at",

            ]

        )

    @staticmethod
    def failed(
        transaction,
        response_data=None,
    ):

        transaction.status = "failed"

        transaction.response_data = response_data or {}

        transaction.save(

            update_fields=[
                "status",
                "response_data",
            ]

        )

    @staticmethod
    def is_processed(transaction):
        return transaction.processed_at is not None