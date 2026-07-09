from django import forms
from main.models import Order


class OrderStatusForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = ["status"]

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            )
        }