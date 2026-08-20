from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from main.models import Product


@login_required
def toggle_wishlist(request, product_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
            },
            status=400,
        )

    wishlist = request.session.get(
        "wishlist",
        [],
    )

    product_id = str(product_id)

    if product_id in wishlist:

        wishlist.remove(product_id)

        liked = False

    else:

        wishlist.append(product_id)

        liked = True

    request.session["wishlist"] = wishlist
    request.session.modified = True

    return JsonResponse(
        {
            "success": True,
            "liked": liked,
            "count": len(wishlist),
        }
    )


@login_required
def wishlist_view(request):

    wishlist = request.session.get(
        "wishlist",
        [],
    )

    products = Product.objects.filter(
        id__in=wishlist
    )

    return render(
        request,
        "main/wishlist/wishlist.html",
        {
            "products": products,
        },
    )