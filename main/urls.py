from django.urls import path
from main import views
from django.contrib.auth import views as auth_views



urlpatterns = [


    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove_from_cart/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile_view, name='profile'),
path('logout/', views.logout_view, name='logout'),
path('register/', views.register_view, name='register'),
path('wishlist/', views.wishlist_view, name='wishlist'),
path('toggle-wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
path('sharh',views.sharh,name='sharh'),
path('branches/', views.branches, name='branches'),
path('career/',views.career,name='career'),
path('delete-order/<int:order_id>/',views.delete_order,name='delete_order'),
path("cart/update/",views.update_cart,name="update_cart"
),


]