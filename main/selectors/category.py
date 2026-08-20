from main.models import Category


def get_categories():

    return (
        Category.objects
        .filter(is_active=True)
        .prefetch_related("subcategories")
        .order_by("ordering")
    )


def get_category(category_id):

    return (
        Category.objects
        .filter(
            id=category_id,
            is_active=True
        )
        .first()
    )


def get_category_by_slug(slug):

    return (
        Category.objects
        .filter(
            slug=slug,
            is_active=True
        )
        .first()
    )