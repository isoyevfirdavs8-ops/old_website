from main.models import Wishlist


def get_user_wishlist(user):

    return (
        Wishlist.objects
        .filter(user=user)
        .select_related("product")
    )