from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from main.models import Category


def mega_menu(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    subcategories = category.subcategories.all().order_by("ordering")

    data = {
        "banner": category.image.url if category.image else "",
        "subcategories": [
            {
                "id": sub.id,
                "name": sub.name,
                "slug": sub.slug,
                "image": sub.image.url if sub.image else "",
            }
            for sub in subcategories
        ],
    }

    return JsonResponse(data)

from django.http import JsonResponse
from main.models import SubCategory


def subcategories_api(request):

    category_id = request.GET.get("category")

    data = list(
        SubCategory.objects.filter(
            category_id=category_id,
            is_active=True,
            page_type="product",
        ).values(
            "id",
            "name",
        )
    )

    return JsonResponse(data, safe=False)