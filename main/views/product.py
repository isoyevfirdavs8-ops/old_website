from django.shortcuts import get_object_or_404


from main.models import Product
from django.shortcuts import redirect, render

from dashboard.forms.product import ProductForm
from main.forms.review import ProductReviewForm

from main.models import (
    Product,
    ProductReview,
)
def product_detail(request, id):

    product = get_object_or_404(
        Product.objects.prefetch_related(
            "colors__images",
            "colors__sizes",
        ),
        id=id,
    )

    colors = product.colors.all()

    related_products = (
        Product.objects
        .filter(
            subcategory=product.subcategory
        )
        .exclude(id=product.id)[:4]
    )
    reviews = ProductReview.objects.filter(
        product=product,
        is_active=True,
    )

    context = {

        "product": product,

        "colors": colors,

        "related_products": related_products,

        "reviews": reviews,

        "review_form": ProductReviewForm(),

    }

    return render(

        request,

        "main/product/detail.html",

        context,

    )





def add_product(request):

    if request.method == "POST":

        form = ProductForm(

            request.POST,

            request.FILES,

        )

        if form.is_valid():

            form.save()

            return redirect("home")

    else:

        form = ProductForm()

    return render(

        request,

        "add_product.html",

        {

            "form": form

        }

    )
