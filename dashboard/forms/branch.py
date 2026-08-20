from django import forms

from main.models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            "subcategory",
            "name",
            "address",
            "phone",
            "work_time",
            "latitude",
            "longitude",
        ]

        widgets = {
            "subcategory": forms.Select(
                attrs={"class": "form-select"}
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Branch name"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "work_time": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "09:00 - 23:00"
                }
            ),

            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any"
                }
            ),

            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any"
                }
            ),
        }