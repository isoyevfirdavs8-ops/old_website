import requests

from django.conf import settings

from main.models import Activity, Notification


def send_telegram_message(text):

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {

        "chat_id": settings.TELEGRAM_CHAT_ID,

        "text": text

    }

    requests.post(url, data=data)


def create_activity(

    user,

    action,

    message

):

    Activity.objects.create(

        user=user,

        action=action,

        message=message

    )


def create_notification(

    user,

    title,

    message

):

    Notification.objects.create(

        user=user,

        title=title,

        message=message

    )