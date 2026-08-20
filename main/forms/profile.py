from django import forms
from django.contrib.auth.models import User

from main.models import Profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ism",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Familiya",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email",
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "phone",
            "address",
            "date_of_birth",
            "gender",
            "telegram",
        )

        widgets = {
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+998 90 123 45 67",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Manzil",
            }),
            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "gender": forms.Select(attrs={
                "class": "form-select",
            }),
            "telegram": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "@username",
            }),
            "avatar": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
        }