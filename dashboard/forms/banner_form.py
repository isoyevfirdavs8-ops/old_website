from django import forms
from main.models import Banner


class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner

        fields = [
            "title",
            "subtitle",
            "description",
            "image",
            "button_text",
            "button_url",
            "order",
            "is_active",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "subtitle": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),

            "button_text": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "button_url": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "order": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }