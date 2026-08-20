from main.models import Career


def get_careers():

    return (
        Career.objects
        .select_related("subcategory")
    )


def get_career(career_id):

    return (
        Career.objects
        .filter(id=career_id)
        .first()
    )


def get_subcategory_careers(subcategory_id):

    return (
        Career.objects
        .filter(
            subcategory_id=subcategory_id
        )
    )