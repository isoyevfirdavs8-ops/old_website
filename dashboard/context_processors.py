from main.models import Notification
from dashboard.navigation import MENU_ITEMS

def notifications(request):

    if not request.user.is_authenticated:

        return {}

    notifications = (
        Notification.objects
        .filter(
            user=request.user
        )[:5]
    )

    unread = (
        Notification.objects
        .filter(
            user=request.user,
            is_read=False
        )
        .count()
    )

    return {

        "navbar_notifications": notifications,

        "navbar_unread": unread

    }




def sidebar_menu(request):

    if not request.user.is_authenticated:

        return {
            "sidebar_menu": []
        }

    if request.user.is_superuser:

        return {
            "sidebar_menu": MENU_ITEMS
        }

    if not hasattr(request.user, "profile"):

        return {
            "sidebar_menu": []
        }

    role = request.user.profile.role

    menu = [

        item

        for item in MENU_ITEMS

        if role in item["roles"]

    ]

    return {

        "sidebar_menu": menu

    }