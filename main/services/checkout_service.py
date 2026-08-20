from django.contrib import messages
from main.validators.order_validator import OrderValidator
from main.services.order_service import OrderService
from main.payment.factory import PaymentFactory
from main.services.payment_service import PaymentService
from main.services.inventory_service import InventoryService

class CheckoutService:

    def __init__(self, request, cart_context):

        self.request = request

        self.cart_context = cart_context

    def checkout(self):
        OrderValidator.validate(
            self.request,
            self.cart_context,
        )

        service = OrderService(
            self.request,
            self.cart_context,
        )

        order = service.create_order()

        InventoryService.reserve(
            order,
        )

        payment = PaymentService.create_payment(
            order,
        )

        gateway = PaymentFactory.get_gateway(
            payment.provider,
        )

        payment_response = gateway.create_payment(
            payment,
        )

        self.request.session["cart"] = {}
        self.request.session.modified = True

        self.request.session.pop("otp_verified", None)
        self.request.session.pop("verified_phone", None)

        messages.success(
            self.request,
            "Your order has been placed successfully.",
        )

        return payment_response