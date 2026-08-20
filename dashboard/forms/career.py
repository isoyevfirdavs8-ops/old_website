from django import forms

from main.models import Career


class CareerForm(forms.ModelForm):

    class Meta:

        model = Career

        fields = "__all__"

        widgets = {
            "subcategory": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6
                }
            ),
        }