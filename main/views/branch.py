import json

from django.shortcuts import (
    render,
    get_object_or_404,
)

from main.models import SubCategory

from main.selectors import (
    get_subcategory_branches,
)


def branch_list(
    request,
    subcategory_id
):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
    )

    branches = get_subcategory_branches(
        subcategory.id
    )

    context = {

        "subcategory": subcategory,

        "branches": branches,

        "branches_json": json.dumps([
            {
                "id": branch.id,
                "name": branch.name,
                "address": branch.address,
                "phone": branch.phone,
                "work_time": branch.work_time,
                "latitude": branch.latitude,
                "longitude": branch.longitude,
            }

            for branch in branches

        ])

    }

    return render(
        request,
        "main/branch/list.html",
        context,
    )