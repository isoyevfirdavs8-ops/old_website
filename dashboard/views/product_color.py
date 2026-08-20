from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from dashboard.forms import ProductColorForm, ProductColorFormSet

from main.models import (
    Product,
    ProductColor,
)

class ProductColorCreateView(View):
    def post(self, request, pk):
        product = get_object_or_404(
            Product,
            pk=pk,
            owner=request.user,   # faqat o'ziga tegishli mahsulotga ruxsat
        )

        form = ProductColorForm(request.POST)

        if form.is_valid():
            color = form.save(commit=False)
            color.product = product
            color.save()
            messages.success(request, "Color created successfully.")
        else:
            messages.error(request, "Xatolik: forma noto'g'ri to'ldirilgan.")

        return redirect("product_manage", pk=product.pk)


class ProductColorDeleteView(View):
    def post(self, request, pk):
        color = get_object_or_404(
            ProductColor,
            pk=pk,
            product__owner=request.user,   # faqat o'ziga tegishli rangni o'chira oladi
        )

        product_id = color.product.id
        color.delete()

        messages.success(request, "Color deleted.")
        return redirect("product_manage", pk=product_id)