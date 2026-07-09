from django import forms

from main.models import Category


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [

            "name",

            "name_ru",

        ]

        widgets = {

            "name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Category name"

                }

            ),

            "name_ru": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Russian name"

                }

            ),

        }