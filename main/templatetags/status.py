from django import template

register = template.Library()


@register.filter
def badge(status):

    colors = {

        "Pending": "warning",

        "Processing": "primary",

        "Delivered": "success",

        "Cancelled": "danger",

    }

    return colors.get(status, "secondary")