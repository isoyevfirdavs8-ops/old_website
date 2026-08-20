from django import forms
from django.forms import inlineformset_factory

from main.models import ProductGallery, ProductColor


class ProductGalleryForm(forms.ModelForm):

    class Meta:

        model = ProductGallery

        fields = [
            "image",
        ]

        widgets = {

            "image": forms.ClearableFileInput(

                attrs={
                    "class": "form-control"
                }

            )

        }

ProductGalleryFormSet = inlineformset_factory(

    ProductColor,

    ProductGallery,

    form=ProductGalleryForm,

    extra=2,

    can_delete=True,

)
