from main.models import Order


def get_orders():

    return (
        Order.objects
        .select_related("user")
        .prefetch_related(
            "items",
            "items__product",
        )
    )


def get_order(pk):

    return (
        Order.objects
        .select_related("user")
        .prefetch_related(
            "items",
            "items__product",
        )
        .get(pk=pk)
    )


def latest_orders(limit=10):

    return (
        Order.objects
        .select_related("user")
        .prefetch_related(
            "items",
            "items__product",
        )
        .order_by("-created_at")[:limit]
    )