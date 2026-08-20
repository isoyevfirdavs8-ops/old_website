from main.payment.gateway import PaymentGateway
from main.services.payment_service import PaymentService
from main.services.payme_service import PaymeService


class PaymeGateway(PaymentGateway):

    def create_payment(self, payment):

        PaymentService.mark_waiting(payment)

        return {

            "type": "redirect",

            "redirect": PaymeService.payment_url(

                payment,

            ),

        }

    def verify_payment(self, request):

        return PaymeService.verify(

            request,

        )

    def cancel_payment(self, payment):

        PaymentService.cancel(

            payment,

        )

        return {

            "success": True,

        }