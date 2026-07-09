
from .models import Product
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return data
        return [data]


class ProductForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price',]



class RegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Telefon raqam"
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'password1', 'password2']