from django import forms
from django.contrib.auth.models import User

from main.models import Profile


class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [

            "username",

            "first_name",

            "last_name",

            "email",

            "is_active",

            "is_staff",

            "is_superuser",

        ]

        widgets = {

            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "is_staff": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "is_superuser": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

        }


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [

            "role",

            "phone",

            "address",

            "date_of_birth",

            "gender",

            "telegram",

            "avatar",

        ]

        widgets = {

            "role": forms.Select(
                attrs={"class":"form-select"}
            ),

            "phone": forms.TextInput(
                attrs={"class":"form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":3
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "gender": forms.Select(
                attrs={"class":"form-select"}
            ),

            "telegram": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),

        }