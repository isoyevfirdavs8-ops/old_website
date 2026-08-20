from email import message

from main.models import Activity


def create_activity(user, action, description):

    if not user or not user.is_authenticated:
        return

    Activity.objects.create(

        user=user,

        action=action,

        message=message,

    )