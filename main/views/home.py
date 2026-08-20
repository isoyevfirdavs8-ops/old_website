from django.shortcuts import render

from main.models import Banner

from main.selectors import (
    get_products,
    get_categories,
    get_subcategories,
    get_category_products,
    get_subcategory_products,
    search_products,
)


def home(request):

    products = get_products()

    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    query = request.GET.get("q")

    if category_id:
        products = get_category_products(category_id)

    if subcategory_id:
        products = get_subcategory_products(subcategory_id)

    if query:
        products = search_products(query)

    context = {
        "products": products,
        "categories": get_categories(),
        "subcategories": get_subcategories(),
        "banners": Banner.objects.filter(
            is_active=True
        ).order_by("order"),
        "wishlist_products":
            request.session.get("wishlist", []),
    }

    return render(
        request,
        "home.html",
        context,
    )