from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)


from dashboard.forms.product import (
    ProductForm,
    ProductImageForm,
    ProductSizeForm,
)
from dashboard.mixins import RoleRequiredMixin

from main.models import (
    Product,
    ProductImage,
    ProductSize,
    SubCategory,
)

from main.utils import (
    create_activity,
    create_notification,
)


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
)

ProductSizeFormSet = inlineformset_factory(
    Product,
    ProductSize,
    form=ProductSizeForm,
    extra=1,
    can_delete=True,
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
        "manager",
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
                "sizes",
            )
            .order_by("-created_at")
        )

        user = self.request.user

        if user.is_superuser:
            return queryset

        role = user.profile.role

        if role in [
            "admin",
            "manager",
        ]:
            return queryset

        if role == "seller":
            return queryset.filter(
                owner=user
            )

        return Product.objects.none()

    def get_context_data(
            self,
            **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        queryset = self.get_queryset()

        context["total_products"] = queryset.count()

        context["total_stock"] = ProductSize.objects.filter(
            product__in=queryset
        ).aggregate(total=Sum("stock"))["total"] or 0

        return context
class ProductCreateView(
    RoleRequiredMixin,
    CreateView,
):

    allowed_roles = [
        "admin",
        "manager",
        "seller",
    ]

    model = Product

    form_class = ProductForm

    template_name = "dashboard/products/form.html"

    success_url = reverse_lazy("product_list")

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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.POST:

            context["image_formset"] = ProductImageFormSet(
                self.request.POST,
                self.request.FILES,
                prefix="gallery",
            )

            context["size_formset"] = ProductSizeFormSet(
                self.request.POST,
                prefix="sizes",
            )

        else:

            context["image_formset"] = ProductImageFormSet(
                prefix="gallery",
            )

            context["size_formset"] = ProductSizeFormSet(
                prefix="sizes",
            )

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()

        image_formset = context["image_formset"]

        size_formset = context["size_formset"]

        form.instance.owner = self.request.user

        if (
            image_formset.is_valid()
            and size_formset.is_valid()
        ):

            self.object = form.save()

            image_formset.instance = self.object
            image_formset.save()

            size_formset.instance = self.object
            size_formset.save()

            create_activity(
                self.request.user,
                "product_created",
                f'Product "{self.object.title}" created.',
            )

            create_notification(
                self.request.user,
                "New Product",
                f'"{self.object.title}" created successfully.',
            )

            messages.success(
                self.request,
                "Product created successfully.",
            )

            return redirect(
                self.success_url
            )

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )

class ProductUpdateView(
    RoleRequiredMixin,
    UpdateView,
):

    allowed_roles = [
        "admin",
        "manager",
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

        if role in ["admin", "manager"]:
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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.POST:

            context["image_formset"] = ProductImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix="gallery",
            )

            context["size_formset"] = ProductSizeFormSet(
                self.request.POST,
                instance=self.object,
                prefix="sizes",
            )

        else:

            context["image_formset"] = ProductImageFormSet(
                instance=self.object,
                prefix="gallery",
            )

            context["size_formset"] = ProductSizeFormSet(
                instance=self.object,
                prefix="sizes",
            )

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()

        image_formset = context["image_formset"]

        size_formset = context["size_formset"]

        if (
            image_formset.is_valid()
            and size_formset.is_valid()
        ):

            self.object = form.save()

            image_formset.instance = self.object
            image_formset.save()

            size_formset.instance = self.object
            size_formset.save()

            create_activity(
                self.request.user,
                "product_updated",
                f'Product "{self.object.title}" updated.',
            )

            create_notification(
                self.request.user,
                "Product Updated",
                f'"{self.object.title}" updated successfully.',
            )

            messages.success(
                self.request,
                "Product updated successfully.",
            )

            return redirect(
                self.success_url
            )

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )

class ProductDeleteView(
    RoleRequiredMixin,
    DeleteView,
):

    allowed_roles = [
        "admin",
        "manager",
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

        if role in ["admin", "manager"]:
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
        "manager",
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
                "sizes",
            )
        )

        user = self.request.user

        if user.is_superuser:
            return qs

        role = user.profile.role

        if role in ["admin", "manager"]:
            return qs

        if role == "seller":
            return qs.filter(owner=user)

        return qs.none()