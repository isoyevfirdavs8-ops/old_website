from django.urls import path

from dashboard import views

from dashboard.views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
    DashboardView,
)

from dashboard.views.analytics import AnalyticsView

from dashboard.views.career import (
    career_create,
    career_delete,
    career_list,
    career_update,
)

from dashboard.views.notification import (
    NotificationAPIView,
    NotificationReadView,
)

from dashboard.views.order import (
    OrderDetailView,
    OrderInvoicePDFView,
    OrderInvoiceView,
    OrderListView,
    OrderStatusUpdateView,
    dashboard_delete_order,
)

from dashboard.views.product import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductManageView,
    ProductSizeCreateView,
    ProductSizeDeleteView,
    ProductUpdateView,
    load_subcategories,
)

from dashboard.views.product_color import (
    ProductColorCreateView,
    ProductColorDeleteView,
)

from dashboard.views.product_gallery import (
    ProductGalleryCreateView,
    ProductGalleryDeleteView,
)

from dashboard.views.product_review import (
    ProductReviewCreateView,
    ProductReviewDeleteView,
)

from dashboard.views.settings import (
    contact_settings,
    general_settings,
    map_settings,
    seo_settings,
    settings_home,
    social_settings,
    system_settings,
)

from dashboard.views.subcategory import (
    SubCategoryCreateView,
    SubCategoryDeleteView,
    SubCategoryDetailView,
    SubCategoryListView,
    SubCategoryUpdateView,
)

from dashboard.views.users import (
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
)



urlpatterns = [

    # Dashboard
    path("", DashboardView.as_view(), name="dashboard"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),

    # Settings
    path("settings/", settings_home, name="settings_home"),
    path("settings/general/", general_settings, name="dashboard_general_settings"),
    path("settings/contact/", contact_settings, name="dashboard_contact_settings"),
    path("settings/social/", social_settings, name="dashboard_social_settings"),
    path("settings/map/", map_settings, name="dashboard_map_settings"),
    path("settings/seo/", seo_settings, name="dashboard_seo_settings"),
    path("settings/system/", system_settings, name="dashboard_system_settings"),

    # Categories
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("category/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("category/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),

    # SubCategories
    path("subcategory/", SubCategoryListView.as_view(), name="subcategory_list"),
    path("subcategory/create/", SubCategoryCreateView.as_view(), name="subcategory_create"),
    path("subcategory/<int:pk>/", SubCategoryDetailView.as_view(), name="subcategory_detail"),
    path("subcategory/<int:pk>/edit/", SubCategoryUpdateView.as_view(), name="subcategory_edit"),
    path("subcategory/<int:pk>/delete/", SubCategoryDeleteView.as_view(), name="subcategory_delete"),

    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/manage/", ProductManageView.as_view(), name="product_manage"),

    # Product Colors
    path("products/<int:pk>/color/create/", ProductColorCreateView.as_view(), name="product_color_create"),
    path("colors/<int:pk>/delete/", ProductColorDeleteView.as_view(), name="product_color_delete"),

    # Product Gallery
    path("gallery/<int:color_id>/create/", ProductGalleryCreateView.as_view(), name="product_gallery_create"),
    path("gallery/<int:pk>/delete/", ProductGalleryDeleteView.as_view(), name="product_gallery_delete"),

    # Product Sizes
    path("products/colors/<int:color_id>/sizes/create/", ProductSizeCreateView.as_view(), name="product_size_create"),
    path("products/sizes/<int:pk>/delete/", ProductSizeDeleteView.as_view(), name="product_size_delete"),

    # Reviews
    path("products/<int:product_id>/review/create/", ProductReviewCreateView.as_view(), name="product_review_create"),
    path("reviews/<int:pk>/delete/", ProductReviewDeleteView.as_view(), name="product_review_delete"),

    # Orders
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order_status"),
    path("orders/<int:pk>/invoice/", OrderInvoiceView.as_view(), name="order_invoice"),
    path("orders/<int:pk>/invoice/pdf/", OrderInvoicePDFView.as_view(), name="order_invoice_pdf"),
    path("delete-order/<int:pk>/", dashboard_delete_order, name="dashboard_delete_order"),

    # Users
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),

    # Notifications
    path("notifications/", NotificationAPIView.as_view(), name="notifications_api"),
    path("notifications/<int:pk>/read/", NotificationReadView.as_view(), name="notification_read"),

    # Careers
    path("careers/", career_list, name="career_list"),
    path("careers/create/", career_create, name="career_create"),
    path("careers/<int:pk>/update/", career_update, name="career_update"),
    path("careers/<int:pk>/delete/", career_delete, name="career_delete"),

    # Banners
    path("banners/", views.banner_list, name="banner_list"),
    path("banners/create/", views.banner_create, name="banner_create"),
    path("banners/<int:pk>/edit/", views.banner_update, name="banner_update"),
    path("banners/<int:pk>/delete/", views.banner_delete, name="banner_delete"),

    # Branches
    path("branches/", views.branch_list, name="branch_list"),
    path("branches/create/", views.branch_create, name="branch_create"),
    path("branches/<int:pk>/update/", views.branch_update, name="branch_update"),
    path("branches/<int:pk>/delete/", views.branch_delete, name="branch_delete"),

    # AJAX
    path("ajax/subcategories/<int:category_id>/", load_subcategories, name="load_subcategories"),
]