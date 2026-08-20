from django.conf import settings
from django.core.exceptions import ValidationError

from main.payment.signatures.base import SignatureService


class ClickSignatureService(SignatureService):

    @classmethod
    def verify(
        cls,
        *,
        payment_id,
        transaction_id,
        amount,
        signature,
    ):
        """
        Click Signature Verification

        TODO:
            Merchant Secret Key bilan
            haqiqiy MD5/HMAC algoritmi yoziladi.
        """

        if not signature:

            raise ValidationError(
                "Click signature is missing."
            )

        # Temporary
        return True