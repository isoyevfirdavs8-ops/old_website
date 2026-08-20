import requests

from django.conf import settings


class ClickClient:

    BASE_URL = "https://api.click.uz/v2"

    def __init__(self):

        self.service_id = settings.CLICK_SERVICE_ID

        self.merchant_id = settings.CLICK_MERCHANT_ID

        self.secret_key = settings.CLICK_SECRET_KEY

    def create_invoice(self, order):

        """
        Keyinchalik Click API chaqiriladi.
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