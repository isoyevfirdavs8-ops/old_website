from main.utils.telegram import send_telegram_message


class TelegramService:

    @staticmethod
    def send_new_order(order):

        text = (
            "🛒 <b>Yangi buyurtma</b>\n\n"
            f"🆔 #{order.id}\n"
            f"👤 {order.full_name}\n"
            f"📞 {order.phone}\n"
            f"📧 {order.email or '-'}\n\n"
            f"📍 {order.address}\n\n"
            f"🚚 Yetkazish: {order.get_delivery_type_display()}\n"
            f"💳 To'lov: {order.get_payment_method_display()}\n\n"
            "<b>Mahsulotlar:</b>\n"
        )

        for item in order.items.select_related(
            "product",
            "size",
        ):

            text += (
                f"\n"
                f"• {item.product.title}\n"
                f"   📏 Size: {item.size.size}\n"
                f"   🔢 Qty: {item.quantity}\n"
                f"   💰 {item.price:,} so'm\n"
            )

        text += (

            "\n"
            "━━━━━━━━━━━━━━━━━━\n"

            f"💵 Subtotal: {order.subtotal:,} so'm\n"

            f"🚚 Delivery: {order.delivery_price:,} so'm\n"

            f"🎁 Discount: {order.discount:,} so'm\n"

            f"💳 Total: {order.total_price:,} so'm"

        )

        send_telegram_message(text)


@staticmethod
def send_payment_success(order):

    text = f"""
✅ PAYMENT SUCCESS

Order #{order.id}

Customer: {order.full_name}

Phone: {order.phone}

Amount: {order.total_price}
"""

    send_telegram_message(text)