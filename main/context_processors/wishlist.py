def wishlist(request):

    wishlist = request.session.get(

        "wishlist",

        []

    )

    return {

        "wishlist_count": len(wishlist),

        "wishlist_products": wishlist,

    }