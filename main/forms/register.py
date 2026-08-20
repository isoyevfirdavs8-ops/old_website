from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import Profile


class RegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+998 90 123 45 67",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "phone",
            "password1",
            "password2",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "Bu telefon raqami allaqachon ro'yxatdan o'tgan."
            )

        return phone

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = user.profile
        profile.phone = self.cleaned_data["phone"]

        if commit:
            profile.save()

        return user