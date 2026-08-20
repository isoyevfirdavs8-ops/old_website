from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)


from main.models import SubCategory

from main.selectors import (
    get_subcategory_products,
    get_category_subcategories,
    get_subcategory_branches,
    get_subcategory_careers,
)

def subcategory_products(
    request,
    subcategory_id
):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
        is_active=True,
    )

    page_type = subcategory.page_type

    if page_type == "product":


        return render(
            request,
            "main/category_products.html",
            {
                "subcategory": subcategory,

                "products":
                    get_subcategory_products(
                        subcategory.id
                    ),

                "subcategories":
                    get_category_subcategories(
                        subcategory.category_id
                    ),

                "wishlist_products":
                    request.session.get(
                        "wishlist",
                        []
                    ),
            }
        )

    elif page_type == "career":

        return render(
            request,
            "main/career/list.html",
            {
                "subcategory": subcategory,

                "careers":
                    get_subcategory_careers(
                        subcategory.id
                    ),

                "subcategories":
                    get_category_subcategories(
                        subcategory.category_id
                    ),
            }
        )


    elif page_type == "branch":

        import json

        branches = get_subcategory_branches(

            subcategory.id

        )

        return render(

            request,

            "main/branch/list.html",

            {

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

        )


    return redirect("home")