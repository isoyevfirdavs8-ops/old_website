from django.shortcuts import render, get_object_or_404

from main.models import Category

from main.selectors import (
    get_category_products,
    get_category_subcategories,
)


def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug,
        is_active=True
    )

    context = {

        "category": category,

        "products": get_category_products(
            category.id
        ),

        "subcategories":
            get_category_subcategories(
                category.id
            ),

        "wishlist_products":
            request.session.get(
                "wishlist",
                []
            ),

    }

    return render(
        request,
        "main/category_products.html",
        context,
    )