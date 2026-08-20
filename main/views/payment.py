from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from main.payment.factory import PaymentFactory

from main.services.payment_service import PaymentService


@csrf_exempt
@require_POST
def click_callback(request):

    try:

        result = ClickService.verify(
            request,
        )

        return JsonResponse({

            "success": True,

            "payment_id": result["payment_id"],

            "order_id": result["order_id"],

        })

    except ValidationError as e:

        return JsonResponse(

            {

                "success": False,

                "error": str(e),

            },

            status=400,

        )

    except Exception:

        return JsonResponse(

            {

                "success": False,

                "error": "Internal Server Error",

            },

            status=500,

        )


@csrf_exempt
@require_POST
def payme_callback(request):

    try:

        result = PaymeService.verify(
            request,
        )

        return JsonResponse({

            "success": True,

            "payment_id": result["payment_id"],

            "order_id": result["order_id"],

        })

    except ValidationError as e:

        return JsonResponse(

            {

                "success": False,

                "error": str(e),

            },

            status=400,

        )

    except Exception:

        return JsonResponse(

            {

                "success": False,

                "error": "Internal Server Error",

            },

            status=500,

        )


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from main.models import Payment, Order
from main.services.click_service import ClickService
from main.services.payme_service import PaymeService


@login_required
def click_payment(request, payment_id):

    payment = get_object_or_404(

        Payment,

        id=payment_id,

        order__user=request.user,

    )

    payment_url = ClickService.payment_url(

        payment,

    )

    return redirect(

        payment_url,

    )


@login_required
def payme_payment(request, payment_id):

    payment = get_object_or_404(

        Payment,

        id=payment_id,

        order__user=request.user,

    )

    payment_url = PaymeService.payment_url(

        payment,

    )

    return redirect(

        payment_url,

    )

@login_required
def payment_page(request, payment_id):

    payment = get_object_or_404(

        Payment.objects.select_related(
            "order",
        ),

        id=payment_id,

        order__user=request.user,

    )

    return render(

        request,

        "main/payment/payment.html",

        {

            "payment": payment,

            "order": payment.order,

        },

    )

@login_required
@require_POST
def process_payment(request):

    payment = get_object_or_404(

        Payment,

        id=request.POST.get("payment_id"),

        order__user=request.user,

    )

    gateway = PaymentFactory.get_gateway(

        payment.provider,

    )

    response = gateway.create_payment(

        payment,

    )

    if response.get("type") == "redirect":

        return redirect(

            response["redirect"]

        )

    if response.get("type") == "cash":

        return redirect(

            response["redirect"],

            response["order_id"],

        )

    return redirect(
        "checkout_failed"
    )


@login_required
def retry_payment(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    payment = PaymentService.create_payment(

        order,

    )

    return redirect(

        "payment_page",

        payment.id,

    )


@login_required
def payment_history(request):

    payments = (

        Payment.objects

        .select_related(

            "order",

        )

        .filter(

            order__user=request.user,

        )

        .order_by(

            "-created_at",

        )

    )

    return render(

        request,

        "main/profile/payment_history.html",

        {

            "payments": payments,

        },

    )