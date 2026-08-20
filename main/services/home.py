from django.db.models import Prefetch

from main.models import (
    Banner,
    Category,
    Product,
    SubCategory,
)


def get_home_data(category_id=None,
                  subcategory_id=None,
                  query=None):

    products = (
        Product.objects
        .select_related(
            "category",
            "subcategory",
        )
        .prefetch_related(
            "gallery",
            "colors__sizes",
        )
    )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    if subcategory_id:
        products = products.filter(
            subcategory_id=subcategory_id
        )

    if query:
        products = products.filter(
            title__icontains=query
        )

    banners = Banner.objects.filter(
        active=True
    )

    categories = (
        Category.objects
        .prefetch_related(
            "products",
            "subcategories",
        )
    )

    subcategories = SubCategory.objects.all()

    return {
        "products": products,
        "categories": categories,
        "subcategories": subcategories,
        "banners": banners,
    }