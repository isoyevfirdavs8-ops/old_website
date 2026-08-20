from django.shortcuts import render
from main.models import Product


def search(request):

    q = request.GET.get("q", "")

    products = Product.objects.all()

    if q:
        products = products.filter(title__icontains=q)

    return render(
        request,
        "search.html",
        {
            "products": products,
            "query": q,
        },
    )