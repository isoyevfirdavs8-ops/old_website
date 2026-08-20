from main.forms import LoginForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from main.forms.register import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from main.forms import UserUpdateForm, ProfileUpdateForm
from main.models import Order


@login_required
def profile(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    context = {
        "orders": orders,
    }

    return render(
        request,
        "main/profile/profile.html",
        context,
    )


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Profil muvaffaqiyatli yangilandi."
            )

            return redirect("profile")

    else:
        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            instance=profile,
        )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(
        request,
        "main/profile/edit_profile.html",
        context,
    )


def logout_view(request):
    logout(request)
    return redirect('home')









def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Xush kelibsiz! Akkauntingiz muvaffaqiyatli yaratildi."
            )

            return redirect("profile")

    else:
        form = RegisterForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "main/register/register.html",
        context,
    )





def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)

                messages.success(
                    request,
                    "Xush kelibsiz!"
                )

                return redirect("profile")

            messages.error(
                request,
                "Username yoki parol noto'g'ri."
            )

    context = {
        "form": form,
    }

    return render(
        request,
        "main/register/login.html",
        context,
    )