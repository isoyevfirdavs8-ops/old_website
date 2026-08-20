from django.shortcuts import (
    render,
    get_object_or_404,
)

from main.models import SubCategory

from main.selectors import (
    get_subcategory_careers,
)


def career_list(
    request,
    subcategory_id
):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
    )

    context = {

        "subcategory": subcategory,

        "careers":
            get_subcategory_careers(
                subcategory.id
            ),

    }

    return render(
        request,
        "main/career/list.html",
        context,
    )