from django import forms
from main.models import Category


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "name",
            "name_ru",
            "slug",

            "ordering",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "name_ru": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "slug": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "ordering": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }