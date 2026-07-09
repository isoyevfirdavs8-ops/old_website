from django import forms
from main.models import Product




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("owner",)

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "discount": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_discount(self):
        discount = self.cleaned_data["discount"]

        if discount < 0 or discount > 100:
            raise forms.ValidationError(
                "Discount 0 va 100 oralig'ida bo'lishi kerak."
            )

        return discount

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Narx 0 dan katta bo'lishi kerak."
            )

        return price

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 0:
            raise forms.ValidationError(
                "Miqdor manfiy bo'lishi mumkin emas."
            )

        return quantity




