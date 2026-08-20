from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.forms.banner_form import BannerForm
from main.models import Banner


@login_required
def banner_list(request):

    banners = Banner.objects.all().order_by("order")

    return render(
        request,
        "dashboard/banner/index.html",
        {
            "banners": banners,
        },
    )


@login_required
def banner_create(request):

    if request.method == "POST":

        form = BannerForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Banner successfully created."
            )

            return redirect("banner_list")

    else:

        form = BannerForm()

    return render(
        request,
        "dashboard/banner/create.html",
        {
            "form": form,
        },
    )


@login_required
def banner_update(request, pk):

    banner = get_object_or_404(
        Banner,
        pk=pk,
    )

    if request.method == "POST":

        form = BannerForm(
            request.POST,
            request.FILES,
            instance=banner,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Banner updated successfully."
            )

            return redirect("banner_list")

    else:

        form = BannerForm(instance=banner)

    return render(
        request,
        "dashboard/banner/update.html",
        {
            "form": form,
            "banner": banner,
        },
    )


@login_required
def banner_delete(request, pk):

    banner = get_object_or_404(
        Banner,
        pk=pk,
    )

    if request.method == "POST":

        banner.delete()

        messages.success(
            request,
            "Banner deleted successfully."
        )

        return redirect("banner_list")

    return render(
        request,
        "dashboard/banner/delete.html",
        {
            "banner": banner,
        },
    )
