class WishlistService:

    @staticmethod
    def add(request, product_id):

        wishlist = request.session.get(
            "wishlist",
            []
        )

        if product_id not in wishlist:

            wishlist.append(product_id)

        request.session["wishlist"] = wishlist

    @staticmethod
    def remove(request, product_id):

        wishlist = request.session.get(
            "wishlist",
            []

        )

        if product_id in wishlist:

            wishlist.remove(product_id)

        request.session["wishlist"] = wishlist