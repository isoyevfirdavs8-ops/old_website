from django.utils.text import slugify


def generate_slug(title):

    return slugify(title)