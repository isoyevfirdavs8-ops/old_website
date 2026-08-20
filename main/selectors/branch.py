from main.models import Branch


def get_branches():

    return (
        Branch.objects
        .select_related("subcategory")
    )


def get_branch(branch_id):

    return (
        Branch.objects
        .filter(id=branch_id)
        .first()
    )


def get_subcategory_branches(subcategory_id):

    return (
        Branch.objects
        .filter(
            subcategory_id=subcategory_id
        )
    )