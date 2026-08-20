from django.core.management.base import BaseCommand

from main.services.payment_service import PaymentService


class Command(BaseCommand):

    help = "Expire old payments"

    def handle(self, *args, **kwargs):

        PaymentService.expire_old_payments()

        self.stdout.write(

            self.style.SUCCESS(

                "Expired payments checked."

            )

        )