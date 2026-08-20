from django.core.exceptions import ValidationError


def validate_price(price):

    if price <= 0:

        raise ValidationError(

            "Price must be greater than zero."

        )