from django.core.exceptions import ValidationError


def validate_image_size(image):

    if image.size > 5 * 1024 * 1024:

        raise ValidationError(

            "Maximum image size is 5 MB."

        )