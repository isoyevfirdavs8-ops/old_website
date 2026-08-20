import requests

from django.conf import settings


class PaymeClient:

    BASE_URL = "https://checkout.paycom.uz/api"

    def __init__(self):

        self.merchant_id = settings.PAYME_MERCHANT_ID

        self.secret_key = settings.PAYME_SECRET_KEY

    def create_invoice(self, order):

        """
        Keyinchalik Payme API chaqiriladi.
        """

        return {

            "success": True,

            "invoice_id": None,

            "payment_url": "",

        }

    def verify(self, data):

        """
        Callback verify
        """

        return True