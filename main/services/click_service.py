from django.conf import settings

from main.services.payment_callback_service import (
    PaymentCallbackService,
)


class ClickService:

    @staticmethod
    def payment_url(payment):

        return (
            f"{settings.CLICK_PAYMENT_URL}"
            f"?merchant_id={settings.CLICK_MERCHANT_ID}"
            f"&payment_id={payment.id}"
            f"&amount={payment.amount}"
        )

    @staticmethod
    def verify(request):

        return PaymentCallbackService.process(

            provider="click",

            payment_id=request.POST.get("payment_id"),

            transaction_id=request.POST.get("transaction_id"),

            amount=request.POST.get("amount"),

            signature=request.POST.get("sign"),

        )