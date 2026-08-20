from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from django.utils import timezone
from datetime import timedelta
from main.models import Product, Order, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from dashboard.mixins import RoleRequiredMixin


class DashboardView(
    LoginRequiredMixin,
    RoleRequiredMixin,
    TemplateView,
):

    allowed_roles = [
        "admin",
        "managers",
    ]

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["products_count"] = Product.objects.count()
        context["orders_count"] = Order.objects.count()
        context["categories_count"] = Category.objects.count()
        context["users_count"] = User.objects.count()

        context["latest_products"] = Product.objects.order_by("-id")[:5]
        context["latest_orders"] = Order.objects.order_by("-id")[:5]


        monthly = (
            Order.objects
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("total_price"))
            .order_by("month")
        )

        context["months"] = [
            i["month"].strftime("%b")
            for i in monthly
        ]

        context["sales"] = [
            i["total"] or 0
            for i in monthly
        ]


        return context