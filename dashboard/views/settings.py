from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from main.models import SiteSettings


@staff_member_required
def general_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.site_name = request.POST.get(
            "site_name",
            ""
        )

        settings.site_description = request.POST.get(
            "site_description",
            ""
        )

        settings.phone = request.POST.get(
            "phone",
            ""
        )

        settings.email = request.POST.get(
            "email",
            ""
        )

        settings.address = request.POST.get(
            "address",
            ""
        )

        settings.working_hours = request.POST.get(
            "working_hours",
            ""
        )

        settings.meta_title = request.POST.get(
            "meta_title",
            ""
        )

        settings.meta_description = request.POST.get(
            "meta_description",
            ""
        )

        settings.meta_keywords = request.POST.get(
            "meta_keywords",
            ""
        )

        if request.FILES.get("logo"):

            settings.logo = request.FILES["logo"]

        if request.FILES.get("favicon"):

            settings.favicon = request.FILES["favicon"]

        settings.save()

        return redirect(
            "dashboard_settings"
        )

    return render(

        request,

        "dashboard/settings/general.html",

        {

            "settings": settings,

        },

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def settings_home(request):

    return render(

        request,

        "dashboard/settings/index.html",

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.phone = request.POST.get("phone")

        settings.email = request.POST.get("email")

        settings.address = request.POST.get("address")

        settings.working_hours = request.POST.get("working_hours")

        settings.save()

        messages.success(
            request,
            "Contact settings updated successfully."
        )

        return redirect("dashboard_contact_settings")

    return render(

        request,

        "dashboard/settings/contact.html",

        {

            "settings": settings,

        }

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def social_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.telegram = request.POST.get("telegram")

        settings.instagram = request.POST.get("instagram")

        settings.facebook = request.POST.get("facebook")

        settings.youtube = request.POST.get("youtube")

        settings.tiktok = request.POST.get("tiktok")

        settings.save()

        messages.success(

            request,

            "Social links updated successfully."

        )

        return redirect(

            "dashboard_social_settings"

        )

    return render(

        request,

        "dashboard/settings/social.html",

        {

            "settings": settings,

        }

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def map_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.latitude = request.POST.get(
            "latitude"
        )

        settings.longitude = request.POST.get(
            "longitude"
        )

        settings.save()

        messages.success(

            request,

            "Map location updated."

        )

        return redirect(

            "dashboard_map_settings"

        )

    return render(

        request,

        "dashboard/settings/map.html",

        {

            "settings": settings,

        }

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def seo_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.meta_title = request.POST.get(
            "meta_title"
        )

        settings.meta_description = request.POST.get(
            "meta_description"
        )

        settings.meta_keywords = request.POST.get(
            "meta_keywords"
        )

        settings.save()

        messages.success(

            request,

            "SEO settings updated."

        )

        return redirect(

            "dashboard_seo_settings"

        )

    return render(

        request,

        "dashboard/settings/seo.html",

        {

            "settings": settings,

        }

    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def system_settings(request):

    settings = SiteSettings.load()

    if request.method == "POST":

        settings.maintenance_mode = \
            "maintenance_mode" in request.POST

        settings.registration_open = \
            "registration_open" in request.POST

        settings.default_language = request.POST.get(

            "default_language"

        )

        settings.default_currency = request.POST.get(

            "default_currency"

        )

        settings.timezone = request.POST.get(

            "timezone"

        )

        settings.products_per_page = request.POST.get(

            "products_per_page"

        )

        settings.orders_per_page = request.POST.get(

            "orders_per_page"

        )

        settings.dashboard_theme = request.POST.get(

            "dashboard_theme"

        )

        settings.save()

        messages.success(

            request,

            "System settings updated."

        )

        return redirect(

            "dashboard_system_settings"

        )

    return render(

        request,

        "dashboard/settings/system.html",

        {

            "settings": settings,

        }

    )