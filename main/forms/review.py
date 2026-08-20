from django import forms

from main.models import ProductReview


class ProductReviewForm(forms.ModelForm):

    class Meta:

        model = ProductReview

        fields = [
            "name",
            "rating",
            "comment",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer name",
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
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }


