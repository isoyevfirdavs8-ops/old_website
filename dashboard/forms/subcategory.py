from django import forms

from main.models import SubCategory


class SubCategoryForm(forms.ModelForm):

    class Meta:

        model = SubCategory

        fields = [

            "category",

            "name",

            "name_ru",

            "image",

        ]

        widgets = {

            "category": forms.Select(

                attrs={

                    "class": "form-select"

                }

            ),

            "name": forms.TextInput(

                attrs={

                    "class": "form-control"

                }

            ),

            "name_ru": forms.TextInput(

                attrs={

                    "class": "form-control"

                }

            ),

            "image": forms.ClearableFileInput(

                attrs={

                    "class": "form-control"

                }

            ),

        }