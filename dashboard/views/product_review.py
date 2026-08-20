

from django.contrib import messages

from django.shortcuts import (
    get_object_or_404,
    redirect,
)

from django.views import View

from dashboard.forms.product_review import ProductReviewForm

from main.models import (
    Product,
    ProductReview,
)


class ProductReviewCreateView(View):

    def post(self, request, product_id):


        product = get_object_or_404(
            Product,
            id=product_id,
        )

        form = ProductReviewForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():


            review = form.save(
                commit=False
            )
            print(review.avatar)

            review.product = product

            review.save()

            messages.success(
                request,
                "Review added successfully."
            )

        else:

            messages.error(
                request,
                "Review could not be created."
            )

        return redirect(
            "product_manage",
            pk=product.id,
        )


from main.models import ProductReview


class ProductReviewDeleteView(View):

    def post(self, request, pk):

        review = get_object_or_404(
            ProductReview,
            pk=pk,
        )

        product_id = review.product.id

        review.delete()

        messages.success(
            request,
            "Review deleted successfully."
        )

        return redirect(
            "product_manage",
            pk=product_id,
        )