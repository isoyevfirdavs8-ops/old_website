from django import forms

from main.models import ProductReview


class ProductReviewForm(forms.ModelForm):

    class Meta:

        model = ProductReview

        fields = [
            "name",
            "avatar",
            "rating",
            "comment",
            "verified_purchase",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer name",
                }
            ),

            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "rating": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Review...",
                }
            ),

            "verified_purchase": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }


