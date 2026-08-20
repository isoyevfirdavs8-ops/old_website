from django.core.exceptions import ValidationError


class OrderValidator:

    @staticmethod
    def validate(request, cart_context):

        OrderValidator.validate_cart(cart_context)

        OrderValidator.validate_otp(request)

        OrderValidator.validate_customer(request)

        OrderValidator.validate_stock(cart_context)

    @staticmethod
    def validate_cart(cart_context):

        if not cart_context["cart"]:

            raise ValidationError(
                "Your cart is empty."
            )

    @staticmethod
    def validate_otp(request):

        if not request.session.get("otp_verified"):

            raise ValidationError(
                "Please verify your phone number."
            )

    @staticmethod
    def validate_customer(request):

        if not request.POST.get("full_name"):

            raise ValidationError(
                "Full name is required."
            )

        if not request.POST.get("phone"):

            raise ValidationError(
                "Phone number is required."
            )

        if not request.POST.get("address"):

            raise ValidationError(
                "Address is required."
            )

    @staticmethod
    def validate_stock(cart_context):

        for item in cart_context["cart"].values():

            size = item["size"]

            qty = item["qty"]

            if qty > size.stock:

                raise ValidationError(

                    f"{item['product'].title} "
                    f"({size.size}) has only "
                    f"{size.stock} item(s) left."

                )