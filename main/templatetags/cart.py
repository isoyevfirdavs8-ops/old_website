from django import template

register = template.Library()


@register.filter
def cart_count(cart):

    if not cart:
        return 0

    return sum(item["qty"] for item in cart.values())