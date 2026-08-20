from django.core.exceptions import ValidationError


def validate_quantity(value):

    if value < 1:

        raise ValidationError(

            "Quantity cannot be less than one."

        )