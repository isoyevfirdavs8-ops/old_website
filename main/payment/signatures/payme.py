from django.core.exceptions import ValidationError

from main.payment.signatures.base import SignatureService


class PaymeSignatureService(SignatureService):

    @classmethod
    def verify(
        cls,
        **kwargs,
    ):

        signature = kwargs.get("signature")

        if not signature:

            raise ValidationError(
                "Payme signature is missing."
            )

        # Temporary
        return True