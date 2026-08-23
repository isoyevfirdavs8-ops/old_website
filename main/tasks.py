from celery import shared_task


@shared_task
def send_new_order_task(order_id):
    from main.models import Order
    from main.services.telegram_service import TelegramService

    order = Order.objects.get(id=order_id)
    TelegramService._send_new_order_sync(order)


@shared_task
def send_payment_success_task(order_id):
    from main.models import Order
    from main.services.telegram_service import TelegramService

    order = Order.objects.get(id=order_id)
    TelegramService._send_payment_success_sync(order)