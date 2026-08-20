


import logging

logger = logging.getLogger(__name__)


class SMSService:
    """
    SMS xizmatining asosiy klassi.

    Keyinchalik bu yerga Eskiz, PlayMobile yoki
    boshqa SMS API ulanadi.
    """

    @staticmethod
    def send(phone, code):
        """
        Hozircha OTP kodni terminalga chiqaradi.

        Keyinchalik shu metod ichida haqiqiy
        SMS API ishlaydi.
        """

        message = (
            f"Your verification code is: {code}\n"
            f"This code expires in 5 minutes."
        )

        logger.info(
            f"SMS -> {phone}: {message}"
        )

        print("=" * 60)
        print(f"PHONE : {phone}")
        print(f"OTP   : {code}")
        print("=" * 60)

        return True