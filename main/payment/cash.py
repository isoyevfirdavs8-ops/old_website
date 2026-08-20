from main.payment.gateway import PaymentGateway
from main.services.payment_service import PaymentService


class CashGateway(PaymentGateway):

    def create_payment(self, payment):

        PaymentService.mark_paid(payment)

        payment.order.status = "Pending"

        payment.order.save(update_fields=["status"])

        return {

            "type": "cash",

            "redirect": "checkout_success",

            "order_id": payment.order.id,

        }

    def verify_payment(self, request):

        return {

            "success": True,

        }

    def cancel_payment(self, payment):

        PaymentService.cancel(payment)

        return {

            "success": True,

        }