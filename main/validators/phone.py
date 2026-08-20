import re

from django.core.exceptions import ValidationError


def validate_phone(value):

    pattern = r"^\+998\d{9}$"

    if not re.match(pattern, value):

        raise ValidationError(

            "Phone number must be in +998901234567 format."

        )