
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from main.models import (
    ProductColor,
    Product,
)
from main.models import ProductGallery

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from dashboard.forms import (
    ProductForm,

    ProductColorFormSet,
)
from main.models import Product, ProductGallery, ProductColor


class ProductGalleryCreateView(LoginRequiredMixin, View):

    def post(self, request, color_id):

        color = get_object_or_404(ProductColor, pk=color_id)

        files = request.FILES.getlist("images")

        for image in files:

            ProductGallery.objects.create(
                product=color.product,
                color=color,
                image=image,
            )

        messages.success(request, "Images uploaded successfully.")

        return redirect("product_manage", pk=color.product.id)


class ProductGalleryDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        image = get_object_or_404(ProductGallery, pk=pk)

        product_id = image.product.id

        image.delete()

        messages.success(request, "Image deleted successfully.")

        return redirect("product_manage", pk=product_id)





