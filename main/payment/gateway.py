from abc import ABC, abstractmethod


class PaymentGateway(ABC):

    @abstractmethod
    def create_payment(self, payment):
        pass

    @abstractmethod
    def verify_payment(self, request):
        pass

    @abstractmethod
    def cancel_payment(self, payment):
        pass