from main.models import Notification


def notifications(request):
    if not request.user.is_authenticated:
        return {
            "notifications": [],
            "unread_notifications": 0,
        }

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    unread = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    return {
        "notifications": notifications,
        "unread_notifications": unread,
    }