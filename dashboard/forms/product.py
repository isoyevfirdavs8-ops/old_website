from django import forms
from django.forms import inlineformset_factory

from main.models import (
    Product,
    ProductImage,
    ProductSize,
)


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            "category",
            "subcategory",
            "title",
            "description",
            "price",
            "discount",
            "color",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_category",
                }
            ),

            "subcategory": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_subcategory",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 100,
                }
            ),

            "color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Black",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["subcategory"].queryset = (
            Product._meta.get_field(
                "subcategory"
            ).remote_field.model.objects.none()
        )

        if self.instance.pk and self.instance.category:

            self.fields["subcategory"].queryset = (
                self.instance.category.subcategories.all()
            )

        elif "category" in self.data:

            try:

                category_id = int(
                    self.data.get("category")
                )

                self.fields["subcategory"].queryset = (
                    Product._meta.get_field(
                        "subcategory"
                    ).remote_field.model.objects.filter(
                        category_id=category_id
                    )
                )

            except:

                pass


class ProductImageForm(forms.ModelForm):

    class Meta:

        model = ProductImage

        fields = [
            "image",
        ]

        widgets = {

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            )

        }


class ProductSizeForm(forms.ModelForm):

    class Meta:

        model = ProductSize

        fields = [
            "size",
            "stock",
        ]

        widgets = {

            "size": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

        }


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