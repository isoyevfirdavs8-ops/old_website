from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from dashboard.forms import BranchForm
from main.models import Branch


def branch_list(request):
    branches = (
        Branch.objects
        .select_related("subcategory")
        .order_by("name")
    )

    return render(
        request,
        "dashboard/branch/list.html",
        {
            "branches": branches
        }
    )


def branch_create(request):

    form = BranchForm(
        request.POST or None
    )

    if form.is_valid():
        form.save()

        return redirect("branch_list")

    return render(
        request,
        "dashboard/branch/create.html",
        {
            "form": form
        }
    )

def branch_update(request, pk):

    branch = get_object_or_404(
        Branch,
        pk=pk
    )

    form = BranchForm(
        request.POST or None,
        instance=branch
    )

    if form.is_valid():

        form.save()

        return redirect("branch_list")

    return render(
        request,
        "dashboard/branch/update.html",
        {
            "form": form,
            "branch": branch,
        }
    )

def branch_delete(request, pk):

    branch = get_object_or_404(
        Branch,
        pk=pk
    )

    if request.method == "POST":

        branch.delete()

        return redirect("branch_list")

    return render(
        request,
        "dashboard/branch/delete.html",
        {
            "branch": branch,
        },
    )