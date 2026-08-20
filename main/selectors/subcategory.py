from main.models import SubCategory


def get_subcategories():

    return (
        SubCategory.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by(
            "ordering",
            "name"
        )
    )


def get_subcategory(subcategory_id):

    return (
        SubCategory.objects
        .filter(
            id=subcategory_id,
            is_active=True
        )
        .first()
    )


def get_subcategory_by_slug(slug):

    return (
        SubCategory.objects
        .filter(
            slug=slug,
            is_active=True
        )
        .first()
    )


def get_category_subcategories(category_id):

    return (
        SubCategory.objects
        .filter(
            category_id=category_id,
            is_active=True
        )
        .order_by(
            "ordering",
            "name"
        )
    )