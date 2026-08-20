from django import forms
from django.forms import inlineformset_factory

from main.models import ProductColor, ProductSize


class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = [
            "size",
            "stock",
        ]
        widgets = {
            "size": forms.Select(
                attrs={"class": "form-select"},
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "min": 0},
            ),
        }


ProductSizeFormSet = inlineformset_factory(
    ProductColor,
    ProductSize,
    form=ProductSizeForm,
    extra=1,
    can_delete=True,
)