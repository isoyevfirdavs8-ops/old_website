from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
)
from django.db.models import Sum
from main.models import (
    Payment,
    PaymentTransaction,
    OrderStatusHistory, Activity,
)
from django.urls import reverse_lazy
from django.contrib import messages

from django import forms
from django.shortcuts import get_object_or_404, redirect
from dashboard.forms.order import OrderStatusForm


from dashboard.mixins import RoleRequiredMixin
from main.models import Order
from django.db.models import Q
from django.http import HttpResponse, request

from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from main.services.order_history_service import OrderHistoryService
from main.services.order_status_service import OrderStatusService
from main.utils import create_notification, create_activity


class OrderListView(LoginRequiredMixin,
    RoleRequiredMixin,ListView):
    allowed_roles = [
        "admin",
        "managers",
        "staff",
    ]

    model = Order

    template_name = "dashboard/orders/list.html"

    context_object_name = "orders"

    paginate_by = 20

    def get_queryset(self):

        queryset = (
            Order.objects
            .select_related("user")
            .prefetch_related("items", "items__product")
            .order_by("-created_at")
        )

        # =====================
        # Object-Level Permission
        # =====================

        user = self.request.user

        if not user.is_superuser:

            role = user.profile.role

            if role == "seller":

                queryset = queryset.filter(
                    items__product__owner=user
                ).distinct()

            elif role not in ["admin", "managers", "staff"]:

                queryset = queryset.none()

        # =====================
        # Search
        # =====================

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(

                Q(id__icontains=search) |
                Q(full_name__icontains=search) |
                Q(phone__icontains=search)

            )

        # =====================
        # Status Filter
        # =====================

        status = self.request.GET.get("status")

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get("search", "")

        context["selected_status"] = self.request.GET.get(
            "status",
            ""
        )

        context["total_orders"] = Order.objects.count()

        context["pending_orders"] = Order.objects.filter(
            status="pending"
        ).count()

        context["confirmed_orders"] = Order.objects.filter(
            status="confirmed"
        ).count()

        context["preparing_orders"] = Order.objects.filter(
            status="preparing"
        ).count()

        context["shipped_orders"] = Order.objects.filter(
            status="shipped"
        ).count()

        context["delivered_orders"] = Order.objects.filter(
            status="delivered"
        ).count()

        context["cancelled_orders"] = Order.objects.filter(
            status="cancelled"
        ).count()

        return context
class OrderDetailView(LoginRequiredMixin,
    RoleRequiredMixin,DetailView):
    allowed_roles = [
        "admin",
        "managers",
        "staff",
    ]

    model = Order

    template_name = "dashboard/orders/detail.html"

    context_object_name = "order"

    def get_queryset(self):

        queryset = (
            Order.objects
            .select_related("user")
            .prefetch_related(
                "items",
                "items__product",
            )
        )

        user = self.request.user

        if user.is_superuser:
            return queryset

        role = user.profile.role

        if role in ["admin", "managers", "staff"]:
            return queryset

        if role == "seller":
            return queryset.filter(
                items__product__owner=user
            ).distinct()

        return queryset.none()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["form"] = OrderStatusForm(
            instance=self.object
        )

        user = self.request.user

        # Items
        if (
                not user.is_superuser
                and user.profile.role == "seller"
        ):

            items = self.object.items.filter(
                product__owner=user
            )

        else:

            items = self.object.items.all()

        context["items"] = items

        context["total_quantity"] = (
                items.aggregate(
                    total=Sum("quantity")
                )["total"] or 0
        )

        # Payment
        payment = Payment.objects.filter(
            order=self.object
        ).first()

        context["payment"] = payment

        context["transactions"] = (
            PaymentTransaction.objects.filter(
                payment__order=self.object
            ).order_by("-created_at")
        )

        context["payment_transactions"] = (
            payment.transactions.all().order_by("-created_at")
            if payment else []
        )

        context["payment_audits"] = (
            payment.audits.all().order_by("-created_at")
            if payment else []
        )

        # Status History
        context["status_history"] = (
            OrderStatusHistory.objects.filter(
                order=self.object
            ).select_related("changed_by")
        )

        # Activity
        context["activities"] = (
            Activity.objects.filter(
                user=self.object.user
            ).order_by("-created_at")[:20]
        )

        return context


class OrderStatusUpdateView(LoginRequiredMixin,
    RoleRequiredMixin,UpdateView):
    allowed_roles = [
        "admin",
        "managers",
        "staff",
    ]

    model = Order

    fields = ["status"]

    template_name = "dashboard/orders/detail.html"

    def get_queryset(self):

        queryset = Order.objects.all()

        user = self.request.user

        if user.is_superuser:
            return queryset

        role = user.profile.role

        if role in ["admin", "managers", "staff"]:
            return queryset

        return queryset.none()

    def form_valid(self, form):

        old_status = self.get_object().status

        response = super().form_valid(form)

        if old_status != self.object.status:

            OrderHistoryService.create(

                order=self.object,

                old_status=old_status,

                new_status=self.object.status,

                user=self.request.user,

            )

            create_activity(

                self.request.user,

                "order_status_changed",

                f"Order #{self.object.id} status changed from "
                f"{old_status} to {self.object.status}.",

            )

            if self.object.user:
                create_notification(

                    self.object.user,

                    "Order Updated",

                    f"Your order #{self.object.id} status is now "
                    f"{self.object.status}.",

                )

        messages.success(

            self.request,

            "Order status updated successfully.",

        )

        return response

    def get_success_url(self):

        return reverse_lazy(

            "order_detail",

            kwargs={

                "pk": self.object.pk

            }

        )



class OrderInvoiceView(DetailView):

    model = Order

    template_name = "dashboard/orders/invoice.html"

    context_object_name = "order"



    def get_queryset(self):

        queryset = (
            Order.objects
            .select_related("user")
            .prefetch_related(
                "items",
                "items__product",
            )
        )

        user = self.request.user

        if user.is_superuser:
            return queryset

        role = user.profile.role

        if role in ["admin", "managers", "staff"]:
            return queryset

        if role == "seller":
            return queryset.filter(
                items__product__owner=user
            ).distinct()

        return queryset.none()

class OrderInvoicePDFView(LoginRequiredMixin,
    RoleRequiredMixin,View):
    allowed_roles = [
        "admin",
        "managers",
        "staff",
    ]

    def get(self, request, pk):

        queryset = Order.objects.prefetch_related(
            "items",
            "items__product"
        )

        user = request.user

        if not user.is_superuser:

            role = user.profile.role

            if role == "seller":

                queryset = queryset.filter(
                    items__product__owner=user
                ).distinct()

            elif role not in ["admin", "managers", "staff"]:

                queryset = queryset.none()

        order = get_object_or_404(queryset, pk=pk)

        response = HttpResponse(
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="Invoice_{order.id}.pdf"'

        pdf = SimpleDocTemplate(
            response,
            pagesize=(210 * mm, 297 * mm)
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                f"<b>Invoice #{order.id}</b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph(
                f"<b>Customer:</b> {order.full_name}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Phone:</b> {order.phone}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Address:</b> {order.address}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        data = [

            [
                "Product",
                "Size",
                "Qty",
                "Price",
                "Total"
            ]

        ]

        for item in order.items.all():

            data.append([

                item.product.title,

                item.size,

                item.quantity,

                item.price,

                item.total

            ])

        data.append([

            "", "", "",

            "Grand Total",

            order.total_price

        ])

        table = Table(data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -2), colors.beige),

                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ])

        )

        elements.append(table)

        pdf.build(elements)

        return response


def dashboard_delete_order(request, pk):
    if request.method != "POST":
        return redirect("order_detail", pk=pk)

    order = get_object_or_404(Order, pk=pk)

    order.delete()

    messages.success(request, "Order deleted successfully.")

    return redirect("order_list")