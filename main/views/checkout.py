from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from django.utils import timezone

from main.models import OTPVerification, Order
from main.services.checkout_service import CheckoutService
from main.utils.cart import get_cart_data
from main.utils.otp import generate_otp, get_expiry_time
from main.utils.sms import SMSService

@login_required
@transaction.atomic

def checkout(request):

    context = get_cart_data(request)

    if not context["cart"]:

        messages.error(

            request,

            "Your cart is empty."

        )

        return redirect("cart")

    context["delivery_price"] = 0

    context["discount"] = 0

    context["total_price"] = (

        context["cart_total"]

        + context["delivery_price"]

        - context["discount"]

    )

    if request.method == "POST":

        try:

            response = CheckoutService(

                request,

                context,

            ).checkout()

            if response["type"] == "cash":

                return redirect(
                    response["redirect"],
                    response["order_id"],
                )

            elif response["type"] == "redirect":

                return redirect(
                    response["redirect"]
                )

            return redirect(response["redirect"])

        except ValidationError as e:

            messages.error(

                request,

                str(e),

            )

            return redirect("checkout")

    return render(

        request,

        "main/checkout/checkout.html",

        context,

    )

@require_POST
def send_otp(request):

    phone = request.POST.get("phone", "").strip()

    if not phone:

        return JsonResponse({
            "success": False,
            "message": "Phone number is required."
        })

    code = generate_otp()

    otp, created = OTPVerification.objects.update_or_create(
        phone=phone,
        defaults={
            "code": code,
            "is_verified": False,
            "expires_at": get_expiry_time(),
        },
    )

    SMSService.send(phone, code)

    return JsonResponse({
        "success": True,
        "message": "Verification code sent."
    })

from django.utils import timezone


@require_POST
def verify_otp(request):

    phone = request.POST.get("phone", "").strip()

    code = request.POST.get("code", "").strip()

    try:

        otp = OTPVerification.objects.get(
            phone=phone
        )

    except OTPVerification.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "OTP not found."
        })

    if otp.expires_at < timezone.now():

        return JsonResponse({
            "success": False,
            "message": "OTP expired."
        })

    if otp.code != code:

        return JsonResponse({
            "success": False,
            "message": "Invalid code."
        })

    otp.is_verified = True
    otp.save(update_fields=["is_verified"])

    request.session["otp_verified"] = True
    request.session["verified_phone"] = phone

    return JsonResponse({
        "success": True,
        "message": "Phone verified."
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from main.models import Order


@login_required
def checkout_success(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    return render(

        request,

        "main/checkout/success.html",

        {

            "order": order,

        },

    )


@login_required
def checkout_failed(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    return render(

        request,

        "main/checkout/failed.html",

        {

            "order": order,

        }

    )

