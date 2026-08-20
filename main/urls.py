from django.urls import path


from main import views
from main.views.checkout import send_otp, verify_otp, checkout_success, checkout_failed


urlpatterns = [

    # --- Home / Product / Category ---
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path("subcategory/<int:subcategory_id>/",views.subcategory_products,name="subcategory_products",),
    path("api/subcategories/",views.subcategories_api,name="subcategories_api",),

    path('api/mega-menu/<int:category_id>/', views.mega_menu, name='mega_menu_api'),
    path('search/', views.search, name='search'),



    # --- Cart ---
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.update_cart, name='cart_update'),
    path('cart/remove/', views.remove_cart, name='cart_remove'),

    # --- Wishlist ---
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('toggle-wishlist/<int:product_id>/', views.toggle_wishlist, name='wishlist_toggle'),

    # --- Auth ---
    path('register/', views.register_view, name='register'),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),

    # --- Profile ---
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # --- Orders ---
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),

    # --- Checkout ---
    path('checkout/checkout/', views.checkout, name='checkout'),
    path('checkout/send-otp/', send_otp, name='send_otp'),
    path('checkout/verify-otp/', verify_otp, name='verify_otp'),
    path('checkout/success/<int:order_id>/', checkout_success, name='checkout_success'),
    path('checkout/failed/', checkout_failed, name='checkout_failed'),

    # --- Payment ---
    path('payment/<int:payment_id>/', views.payment_page, name='payment_page'),
    path('payment/process/', views.process_payment, name='process_payment'),
    path('payment/retry/<int:order_id>/', views.retry_payment, name='retry_payment'),
    path('payments/', views.payment_history, name='payment_history'),
    path('payment/click/<int:payment_id>/', views.click_payment, name='click_payment'),
    path('payment/click/callback/', views.click_callback, name='click_callback'),
    path('payment/payme/<int:payment_id>/', views.payme_payment, name='payme_payment'),
    path('payment/payme/callback/', views.payme_callback, name='payme_callback'),



]