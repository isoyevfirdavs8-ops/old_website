import requests

from django.conf import settings


def send_telegram_message(text):

    url = (

        f"https://api.telegram.org/bot"

        f"{settings.BOT_TOKEN}/sendMessage"

    )

    requests.post(

        url,

        data={

            "chat_id": settings.CHAT_ID,

            "text": text,

        }

    )