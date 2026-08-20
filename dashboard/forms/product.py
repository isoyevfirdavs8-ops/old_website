from django import forms
from django.forms import inlineformset_factory

from main.models import Product, ProductColor, ProductSize


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "category",
            "subcategory",
            "title",
            "description",
            "shipping",
            "payment",
            "specification",
            "price",
            "discount",
        ]

        widgets = {
            "category": forms.Select(
                attrs={"class": "form-select"},
            ),
            "subcategory": forms.Select(
                attrs={"class": "form-select"},
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product title",
                },
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5},
            ),
            "shipping": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
            "payment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
            "specification": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "min": 0},
            ),
            "discount": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 100},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Boshlang'ich holatda subcategory bo'sh
        self.fields["subcategory"].queryset = (
            Product._meta.get_field("subcategory")
            .remote_field.model.objects.none()
        )

        # Tahrirlash rejimida — mavjud category asosida subcategory'larni to'ldirish
        if self.instance.pk and self.instance.category_id:
            self.fields["subcategory"].queryset = (
                self.instance.category.subcategories.all()
            )

        # POST orqali category tanlangan bo'lsa (yaratish yoki validatsiya xatosidan keyin)
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = (
                    Product._meta.get_field("subcategory")
                    .remote_field.model.objects.filter(
                        category_id=category_id
                    )
                )
            except (ValueError, TypeError):
                pass

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError(
                "Narx 0 dan katta bo'lishi kerak."
            )
        return price

    def clean_discount(self):
        discount = self.cleaned_data["discount"]
        if discount < 0 or discount > 100:
            raise forms.ValidationError(
                "Discount 0 va 100 oralig'ida bo'lishi kerak."
            )
        return discount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if subcategory and category and subcategory.category_id != category.id:
            self.add_error(
                "subcategory",
                "Tanlangan subcategory ushbu category'ga tegishli emas.",
            )

        return cleaned_data