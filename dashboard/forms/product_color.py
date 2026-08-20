from django import forms
from django.forms import inlineformset_factory

from main.models import Product, ProductColor


class ProductColorForm(forms.ModelForm):

    class Meta:

        model = ProductColor

        fields = [
            "name",
            "code",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={"class": "form-control"},
            ),

            "code": forms.TextInput(
                attrs={"class": "form-control", "type": "color"},
            ),

        }


ProductColorFormSet = inlineformset_factory(
    Product,
    ProductColor,
    form=ProductColorForm,
    extra=1,
    can_delete=True,
)