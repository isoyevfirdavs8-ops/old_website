from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import  Category,SubCategory, ProductImage, Sharh, Career, Banner
from .forms import ProductForm, RegisterForm

from .models import Branch


from django.db import transaction


from main.models import (
    Product,
    ProductSize,
    Order,
    OrderItem,
)
from main.utils import (
    create_activity,
    create_notification,
    send_telegram_message,
)




def home(request,):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    query = request.GET.get('q')
    banners = Banner.objects.filter(active=True)

    wishlist_products = request.session.get('wishlist', [])

    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    selected_category = None


    if category_id:
        products = products.filter(category_id=category_id)

        try:
            selected_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            selected_category = None

    if subcategory_id:
        products = products.filter(
            subcategory_id=subcategory_id
        )

    if query:
        products = products.filter(
            title__icontains=query
        )

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        "subcategories": subcategories,
        'wishlist_products': wishlist_products,
        'selected_category': selected_category,
        'banners': banners,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    opinion = Sharh.objects.filter(product=product)

    return render(request, 'detail.html', {
        'product': product,
        'opinion': opinion
    })



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()

            files = request.FILES.getlist('images')

            for f in files:
                ProductImage.objects.create(product=product, image=f)

            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})



from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from main.models import Product, ProductSize


def add_to_cart(request, id):

    if request.method != "POST":
        return redirect("product_detail", id=id)

    product = get_object_or_404(
        Product,
        pk=id
    )

    size_id = request.POST.get("size")

    qty = int(
        request.POST.get("qty", 1)
    )

    if not size_id:

        messages.error(
            request,
            "Please select a size."
        )

        return redirect(
            "product_detail",
            id=id
        )

    product_size = get_object_or_404(
        ProductSize,
        pk=size_id,
        product=product
    )

    cart = request.session.get(
        "cart",
        {}
    )

    key = str(product_size.id)

    if key in cart:

        cart[key]["qty"] += qty

    else:

        cart[key] = {

            "product_id": product.id,

            "size_id": product_size.id,

            "qty": qty,

        }

    request.session["cart"] = cart

    messages.success(
        request,
        "Product added to cart."
    )

    return redirect("cart")


from django.shortcuts import render, redirect
from main.models import Product, ProductSize

from django.shortcuts import render
from main.models import Product, ProductSize


def cart_view(request):

    cart = request.session.get("cart", {})

    items = []
    total_price = 0
    keys_to_delete = []

    for key, item in cart.items():

        try:

            product = Product.objects.prefetch_related(
                "gallery"
            ).get(
                pk=item["product_id"]
            )

            product_size = ProductSize.objects.get(
                pk=item["size_id"]
            )

        except (Product.DoesNotExist, ProductSize.DoesNotExist, KeyError):

            keys_to_delete.append(key)

            continue

        # stock nazorati
        if item["qty"] > product_size.stock:

            cart[key]["qty"] = product_size.stock

        qty = cart[key]["qty"]

        subtotal = product.final_price * qty

        total_price += subtotal

        items.append({

            "key": key,

            "product": product,

            "size": product_size,

            "qty": qty,

            "subtotal": subtotal,

            "stock": product_size.stock,

        })

    for key in keys_to_delete:

        del cart[key]

    request.session["cart"] = cart

    request.session.modified = True

    return render(

        request,

        "cart.html",

        {

            "items": items,

            "total_price": total_price,

        }

    )

def remove_from_cart(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        del cart[key]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def update_cart(request):

    key = request.POST.get("key")
    action = request.POST.get("action")

    cart = request.session.get("cart", {})

    if key not in cart:
        return JsonResponse({"success": False})

    item = cart[key]

    try:
        product_size = ProductSize.objects.select_related(
            "product"
        ).get(
            id=item["size_id"]
        )

    except ProductSize.DoesNotExist:
        return JsonResponse({"success": False})

    qty = item["qty"]

    if action == "increase":

        if qty < product_size.stock:
            qty += 1

    elif action == "decrease":

        if qty > 1:
            qty -= 1

    item["qty"] = qty

    cart[key] = item

    request.session["cart"] = cart
    request.session.modified = True

    subtotal = product_size.product.final_price * qty

    total = 0

    for value in cart.values():

        try:

            ps = ProductSize.objects.select_related(
                "product"
            ).get(
                id=value["size_id"]
            )

            total += ps.product.final_price * value["qty"]

        except ProductSize.DoesNotExist:
            pass

    return JsonResponse({
        "success": True,
        "qty": qty,
        "subtotal": subtotal,
        "total": total,
        "stock": product_size.stock,
    })
@login_required
@transaction.atomic
def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Cart is empty.")
        return redirect("cart")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
        )

        telegram_message = f"""
🛒 Yangi buyurtma

👤 {full_name}
📞 {phone}
📍 {address}

📦 Mahsulotlar:
"""

        grand_total = 0

        for key, item in cart.items():

            product = Product.objects.get(
                pk=item["product_id"]
            )

            product_size = ProductSize.objects.get(
                product=product,
                pk=item["size_id"]
            )

            qty = int(item["qty"])

            if qty > product_size.stock:

                messages.error(
                    request,
                    f"{product.title} ({product_size.size}) uchun omborda faqat {product_size.stock} ta mavjud."
                )

                raise Exception("Stock not enough")

            OrderItem.objects.create(
                order=order,
                product=product,
                size=product_size,
                quantity=qty,
                price=product.final_price,
            )

            product_size.stock -= qty
            product_size.save()

            grand_total += product.final_price * qty

            telegram_message += (
                f"\n"
                f"• {product.title}\n"
                f"  Size: {product_size.size}\n"
                f"  Qty: {qty}\n"
            )

        order.total_price = grand_total
        order.save()

        create_activity(
            request.user,
            "order_created",
            f"Order #{order.id} created.",
        )

        if order.user:

            create_notification(
                order.user,
                "Order Created",
                f"Your order #{order.id} has been received.",
            )

        send_telegram_message(telegram_message)

        request.session["cart"] = {}

        messages.success(
            request,
            "Your order has been placed successfully."
        )

        return redirect("home")

    return render(
        request,
        "checkout.html",
    )
@login_required
def profile_view(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(
        request,
        'profile.html',
        {
            'orders': orders
        }
    )

@login_required
def toggle_wishlist(request, product_id):

    wishlist = request.session.get('wishlist', [])

    product_id = str(product_id)

    if product_id in wishlist:

        wishlist.remove(product_id)

    else:

        wishlist.append(product_id)

    request.session['wishlist'] = wishlist

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def wishlist_view(request):

    wishlist = request.session.get('wishlist', [])

    products = Product.objects.filter(
        id__in=wishlist
    )

    return render(request, 'wishlist.html', {
        'products': products
    })

def sharh(request):
    opinion = Sharh.objects.all()

    return render(request,'sharh.html',{'opinion':opinion})




def branches(request):
    subcategory_id = request.GET.get('subcategory')

    branches = Branch.objects.all()

    if subcategory_id:
        branches = branches.filter(
            subcategory_id=subcategory_id
        )

    return render(
        request,
        'xarita.html',
        {
            'branches': branches
        }
    )
def career(request):

    about = Career.objects.all()

    return render(request,'career.html',{'about':about})




@login_required
@require_POST
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    order.delete()
    return redirect('profile')
def logout_view(request):
    logout(request)
    return redirect('home')



def register_view(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        user = form.save()

        # Signal yaratgan profilni olamiz
        profile = user.profile

        profile.phone = form.cleaned_data["phone"]

        profile.save()

        return redirect("home")

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )

