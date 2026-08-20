from main.payment.gateway import PaymentGateway
from main.services.payment_service import PaymentService
from main.services.click_service import ClickService


class ClickGateway(PaymentGateway):

    def create_payment(self, payment):

        PaymentService.mark_waiting(payment)

        return {

            "type": "redirect",

            "redirect": ClickService.payment_url(

                payment,

            ),

        }

    def verify_payment(self, request):

        return ClickService.verify(

            request,

        )

    def cancel_payment(self, payment):

        PaymentService.cancel(

            payment,

        )

        return {

            "success": True,

        }