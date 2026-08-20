
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.views import View

from dashboard.forms.product_color import ProductColorForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from dashboard.forms import (
    ProductForm,

    ProductColorFormSet,
    ProductColorForm, ProductSizeForm,
)
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from main.models import (
    Product,
    ProductColor,

)

from dashboard.forms.product_review import ProductReviewForm
from main.models import ProductReview


from dashboard.forms.product import (
    ProductForm,


)
from dashboard.mixins import RoleRequiredMixin

from main.models import (

    ProductSize,
    SubCategory,
)


from main.utils import (
    create_activity,
    create_notification,
)



def load_subcategories(request, category_id):

    subcategories = (
        SubCategory.objects
        .filter(category_id=category_id)
        .values(
            "id",
            "name",
        )
    )

    return JsonResponse(
        list(subcategories),
        safe=False,
    )

class ProductListView(
    RoleRequiredMixin,
    ListView,
):

    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    model = Product

    template_name = "dashboard/products/list.html"

    context_object_name = "products"

    paginate_by = 20

    def get_queryset(self):

        queryset = (
            Product.objects
            .select_related(
                "category",
                "subcategory",
                "owner",
            )
            .prefetch_related(
                "gallery",
                "colors__sizes",
            )
            .order_by("-created_at")
        )

        user = self.request.user

        if user.is_superuser:
            return queryset

        role = user.profile.role

        if role in [
            "admin",
            "managers",
        ]:
            return queryset

        if role == "seller":
            return queryset.filter(
                owner=user
            )

        return Product.objects.none()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        context["total_products"] = queryset.count()

        context["total_stock"] = (
                ProductSize.objects.filter(
                    color__product__in=queryset
                ).aggregate(
                    total=Sum("stock")
                )["total"] or 0
        )

        return context

class ProductCreateView(
    RoleRequiredMixin,
    CreateView,
):
    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    model = Product
    form_class = ProductForm
    template_name = "dashboard/products/form.html"

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        user = self.request.user

        if (
            not user.is_superuser
            and user.profile.role == "seller"
        ):
            form.fields["category"].queryset = (
                user.profile.categories.all()
            )

        return form

    @transaction.atomic
    def form_valid(self, form):

        form.instance.owner = self.request.user

        self.object = form.save()

        create_activity(
            self.request.user,
            "product_created",
            f'Product "{self.object.title}" created.'
        )

        create_notification(
            self.request.user,
            "New Product",
            f'"{self.object.title}" created successfully.'
        )

        messages.success(
            self.request,
            "Product created successfully."
        )

        return redirect(
            reverse(
                "product_manage",
                kwargs={
                    "pk": self.object.pk
                }
            )
        )

class ProductUpdateView(
    RoleRequiredMixin,
    UpdateView,
):

    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    model = Product

    form_class = ProductForm

    template_name = "dashboard/products/form.html"

    success_url = reverse_lazy("product_list")

    def get_queryset(self):

        qs = Product.objects.all()

        user = self.request.user

        if user.is_superuser:
            return qs

        role = user.profile.role

        if role in ["admin", "managers"]:
            return qs

        if role == "seller":
            return qs.filter(owner=user)

        return qs.none()

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        user = self.request.user

        if (
            not user.is_superuser
            and user.profile.role == "seller"
        ):

            form.fields["category"].queryset = (
                user.profile.categories.all()
            )

        return form

    @transaction.atomic
    def form_valid(self, form):

        self.object = form.save()

        create_activity(
            self.request.user,
            "product_updated",
            f'Product "{self.object.title}" updated.'
        )

        create_notification(
            self.request.user,
            "Product Updated",
            f'"{self.object.title}" updated successfully.'
        )

        messages.success(
            self.request,
            "Product updated successfully."
        )

        return redirect(
            "product_manage",
            pk=self.object.pk
        )

class ProductDeleteView(
    RoleRequiredMixin,
    DeleteView,
):

    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    model = Product

    template_name = "dashboard/products/delete.html"

    success_url = reverse_lazy("product_list")

    def get_queryset(self):

        qs = Product.objects.all()

        user = self.request.user

        if user.is_superuser:
            return qs

        role = user.profile.role

        if role in ["admin", "managers"]:
            return qs

        if role == "seller":
            return qs.filter(owner=user)

        return qs.none()

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()

        title = self.object.title

        create_activity(
            request.user,
            "product_deleted",
            f'Product "{title}" deleted.'
        )

        create_notification(
            request.user,
            "Product Deleted",
            f'"{title}" deleted successfully.'
        )

        messages.success(
            request,
            "Product deleted successfully."
        )

        return super().delete(request, *args, **kwargs)


class ProductDetailView(
    RoleRequiredMixin,
    DetailView,
):

    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    model = Product

    template_name = "dashboard/products/detail.html"

    context_object_name = "product"

    def get_queryset(self):

        qs = (
            Product.objects
            .select_related(
                "category",
                "subcategory",
                "owner",
            )
            .prefetch_related(
                "gallery",
                "colors__sizes",
            )
        )

        user = self.request.user

        if user.is_superuser:
            return qs

        role = user.profile.role

        if role in ["admin", "managers"]:
            return qs

        if role == "seller":
            return qs.filter(owner=user)

        return qs.none()



class ProductManageView(
    RoleRequiredMixin,
    TemplateView,
):

    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    template_name = "dashboard/products/manage.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        product = get_object_or_404(
            Product,
            pk=self.kwargs["pk"]
        )

        context["product"] = product

        context["review_form"] = ProductReviewForm()

        context["reviews"] = (
            ProductReview.objects.filter(
                product=product
            )
        )

        context["color_form"] = ProductColorForm()

        context["size_form"] = ProductSizeForm()

        context["colors"] = (
            ProductColor.objects
            .filter(product=product)
            .prefetch_related("images", "sizes")
        )

        return context
class ProductSizeCreateView(
    RoleRequiredMixin,
    View,
):
    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    def post(self, request, color_id):

        color = get_object_or_404(ProductColor, pk=color_id)

        form = ProductSizeForm(request.POST)

        if form.is_valid():

            size = form.save(commit=False)
            size.color = color
            size.save()

            messages.success(request, "Size added successfully.")

        else:

            messages.error(request, "Please fix the errors below.")

        return redirect("product_manage", pk=color.product.id)


class ProductSizeDeleteView(
    RoleRequiredMixin,
    View,
):
    allowed_roles = [
        "admin",
        "managers",
        "seller",
    ]

    def post(self, request, pk):

        size = get_object_or_404(ProductSize, pk=pk)

        product_id = size.color.product.id

        size.delete()

        messages.success(request, "Size deleted successfully.")

        return redirect("product_manage", pk=product_id)