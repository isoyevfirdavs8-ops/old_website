from main.payment.cash import CashGateway
from main.payment.click import ClickGateway
from main.payment.payme import PaymeGateway


class PaymentFactory:

    gateways = {

        "cash": CashGateway,

        "click": ClickGateway,

        "payme": PaymeGateway,

    }

    @classmethod
    def get_gateway(cls, provider):

        gateway = cls.gateways.get(provider)

        if gateway is None:

            raise ValueError(

                f"Unsupported payment provider: {provider}"

            )

        return gateway()