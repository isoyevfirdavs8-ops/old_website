

import random
import string
from datetime import timedelta

from django.utils import timezone


OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 5


def generate_otp(length=OTP_LENGTH):
    """
    6 xonali OTP kod yaratadi.

    Example:
        483921
    """
    return "".join(
        random.choices(
            string.digits,
            k=length,
        )
    )


def get_expiry_time(minutes=OTP_EXPIRE_MINUTES):
    """
    OTP tugash vaqtini qaytaradi.

    Default: 5 minut
    """
    return timezone.now() + timedelta(minutes=minutes)


def is_expired(otp):
    """
    OTP muddati tugaganmi?

    Returns:
        True / False
    """
    return timezone.now() >= otp.expires_at


def can_resend(otp, seconds=60):
    """
    OTP ni qayta yuborish mumkinmi?

    Default: 60 soniyadan keyin.
    """
    next_send = otp.created_at + timedelta(seconds=seconds)
    return timezone.now() >= next_send


def mask_phone(phone):
    """
    Telefon raqamini yashiradi.

    +998901234567
        ↓
    +99890*****67
    """
    if len(phone) < 7:
        return phone

    return (
        phone[:6]
        + "*" * (len(phone) - 8)
        + phone[-2:]
    )


def mask_email(email):
    """
    Emailni yashiradi.

    example@gmail.com
        ↓
    ex*****@gmail.com
    """
    if "@" not in email:
        return email

    username, domain = email.split("@", 1)

    if len(username) <= 2:
        hidden = "*" * len(username)
    else:
        hidden = username[:2] + "*" * (len(username) - 2)

    return f"{hidden}@{domain}"


def generate_reference():
    """
    OTP request uchun unikal reference.

    Example:
        OTP-593184
    """
    return f"OTP-{random.randint(100000, 999999)}"