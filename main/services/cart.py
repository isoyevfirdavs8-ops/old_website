class CartService:

    @staticmethod
    def get_cart(request):

        return request.session.get(
            "cart",
            {}
        )

    @staticmethod
    def save_cart(request, cart):

        request.session["cart"] = cart

        request.session.modified = True

    @staticmethod
    def clear(request):

        request.session["cart"] = {}

        request.session.modified = True