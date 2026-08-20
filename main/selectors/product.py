from django.db.models import Q

from main.models import Product


def get_products():

    return (
        Product.objects
        .active()
        .select_related(
            "category",
            "subcategory",
        )
        .prefetch_related(
            "gallery",
            "colors__sizes",
        )
    )


def get_product(product_id):

    return (
        get_products()
        .filter(
            id=product_id
        )
        .first()
    )


def get_category_products(category_id):

    return (
        get_products()
        .filter(
            category_id=category_id
        )
    )


def get_subcategory_products(subcategory_id):

    return (
        get_products()
        .filter(
            subcategory_id=subcategory_id
        )
    )


def search_products(query):

    return (
        get_products()
        .filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    )