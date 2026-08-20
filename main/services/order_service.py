from django.db import transaction
from django.core.exceptions import ValidationError
from main.services.telegram_service import TelegramService
from main.models import Order, OrderItem
from main.services.payment_service import PaymentService
from main.services.stock_service import StockService
from main.services.notification_service import NotificationService
from main.services.activity_service import ActivityService
from main.services.order_log_service import OrderLogService



class OrderService:

    def __init__(self, request, cart_context):

        self.request = request

        self.cart = cart_context["cart"]

        self.cart_total = cart_context["cart_total"]

        self.delivery_price = 0

        self.discount = 0

        self.order = None

    @transaction.atomic
    def create_order(self):

        self._create_order()

        self._create_order_items()

        StockService.decrease_stock(
            self.order,
            self.cart,
        )

        self._calculate_total()

        TelegramService.send_new_order(
            self.order
        )

        NotificationService.order_created(
            self.order,
        )

        ActivityService.order_created(
            self.order,
        )

        OrderLogService.create(
            order=self.order,
            new_status=self.order.status,
            user=self.request.user,
            comment="Order created",
        )

        return self.order

    def _create_order(self):

        self.order = Order.objects.create(

            user=(
                self.request.user
                if self.request.user.is_authenticated
                else None
            ),

            full_name=self.request.POST.get("full_name"),

            phone=self.request.POST.get("phone"),

            email=self.request.POST.get("email"),

            address=self.request.POST.get("address"),

            note=self.request.POST.get("note", ""),

            payment_method=self.request.POST.get(
                "payment_method",
                "cash",
            ),

            delivery_type=self.request.POST.get(
                "delivery_type",
                "courier",
            ),

            delivery_price=self.delivery_price,

            discount=self.discount,

        )


    def _create_order_items(self):

        for item in self.cart.values():
            OrderItem.objects.create(

                order=self.order,

                product=item["product"],

                size=item["size"],

                quantity=item["qty"],

                price=item["price"],

            )

    def _calculate_total(self):

        subtotal = sum(

            item.total

            for item in self.order.items.all()

        )

        self.order.subtotal = subtotal

        self.order.total_price = (

            subtotal

            + self.delivery_price

            - self.discount

        )

        if self.order.payment_method == "cash":

            self.order.status = "Pending"

        else:

            self.order.status = "Waiting Payment"

        self.order.save()