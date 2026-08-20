from django import template

register = template.Library()


@register.filter
def in_wishlist(product, wishlist):

    return product.id in wishlist