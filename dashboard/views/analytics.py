from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from dashboard.mixins import RoleRequiredMixin
from main.models import (
    Order,
    Product,
    Category, Activity,
)
from django.utils import timezone

from main.models import OrderItem

class AnalyticsView(LoginRequiredMixin,
    RoleRequiredMixin,TemplateView):
    allowed_roles = [
        "admin",
        "managers",
    ]

    template_name = "dashboard/analytics/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["revenue"] = (
            Order.objects.aggregate(
                total=Sum("total_price")
            )["total"] or 0
        )

        context["orders"] = Order.objects.count()

        context["products"] = Product.objects.count()

        context["category"] = Category.objects.count()

        monthly = (
            Order.objects
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("total_price"))
            .order_by("month")
        )

        context["months"] = [
            item["month"].strftime("%b")
            for item in monthly
        ]

        context["sales"] = [
            item["total"] or 0
            for item in monthly
        ]
        context["pending_count"] = Order.objects.filter(
            status="Pending"
        ).count()

        context["processing_count"] = Order.objects.filter(
            status="Processing"
        ).count()

        context["delivered_count"] = Order.objects.filter(
            status="Delivered"
        ).count()

        context["cancelled_count"] = Order.objects.filter(
            status="Cancelled"
        ).count()

        context["top_products"] = (
            OrderItem.objects
            .values(
                "product__title"
            )
            .annotate(
                sold=Sum("quantity"),
                revenue=Sum("price")
            )
            .order_by("-sold")[:5]
        )

        context["low_stock_products"] = (
            Product.objects
            .filter(quantity__lte=5)
            .order_by("quantity")[:5]
        )

        context["latest_orders"] = (
            Order.objects
            .order_by("-created_at")[:6]
        )

        context["top_customers"] = (
            Order.objects
            .values(
                "full_name"
            )
            .annotate(
                orders=Count("id"),
                spent=Sum("total_price")
            )
            .order_by("-spent")[:5]
        )

        category_sales = (
            OrderItem.objects
            .values(
                "product__category__name"
            )
            .annotate(
                sold=Sum("quantity"),
                revenue=Sum("price")
            )
            .order_by("-sold")
        )

        context["category_sales"] = category_sales

        monthly_revenue = (
            Order.objects.filter(
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year,
                status="Delivered"
            )
            .aggregate(total=Sum("total_price"))
        )

        goal = 50000000

        current = monthly_revenue["total"] or 0

        percent = min(
            round(current * 100 / goal),
            100
        )

        context["goal"] = goal
        context["current"] = current
        context["goal_percent"] = percent

        context["activities"] = Activity.objects.select_related(
            "user"
        )[:8]

        return context
