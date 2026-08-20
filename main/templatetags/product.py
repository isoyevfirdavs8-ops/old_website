from django import template

register = template.Library()


@register.filter
def first_image(product):

    image = product.gallery.first()

    if image:
        return image.image.url

    return ""