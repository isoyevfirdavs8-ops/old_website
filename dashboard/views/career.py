from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from dashboard.forms import CareerForm
from main.models import Career


@permission_required("main.view_career", raise_exception=True)
def career_list(request):

    careers = Career.objects.select_related(
        "subcategory"
    ).order_by("id")

    return render(
        request,
        "dashboard/career/list.html",
        {
            "careers": careers
        }
    )

@permission_required("main.add_career", raise_exception=True)
def career_create(request):

    if request.method == "POST":

        form = CareerForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Career created successfully."
            )

            return redirect("career_list")

    else:

        form = CareerForm()

    return render(
        request,
        "dashboard/career/create.html",
        {
            "form": form
        }
    )

@permission_required("main.change_career", raise_exception=True)
def career_update(request, pk):

    career = get_object_or_404(
        Career,
        pk=pk
    )

    if request.method == "POST":

        form = CareerForm(
            request.POST,
            instance=career
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Career updated successfully."
            )

            return redirect("career_list")

    else:

        form = CareerForm(
            instance=career
        )

    return render(
        request,
        "dashboard/career/update.html",
        {
            "form": form,
            "career": career,
        },
    )

@permission_required("main.delete_career", raise_exception=True)
def career_delete(request, pk):

    career = get_object_or_404(
        Career,
        pk=pk
    )

    if request.method == "POST":

        career.delete()

        messages.success(
            request,
            "Career deleted successfully."
        )

        return redirect("career_list")

    return render(
        request,
        "dashboard/career/delete.html",
        {
            "career": career
        }
    )