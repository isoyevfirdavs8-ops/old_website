from django.urls import path
from dashboard.views.product import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDetailView,
    ProductDeleteView,
    load_subcategories,
)

from dashboard.views import (
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryDeleteView,
    CategoryUpdateView, DashboardView,

)
from dashboard.views.subcategory import (
    SubCategoryListView,
    SubCategoryCreateView,
    SubCategoryDetailView,
    SubCategoryUpdateView,
    SubCategoryDeleteView,
)
from dashboard.views.users import (
    UserListView,
    UserDetailView,
)
from .views.analytics import AnalyticsView

from dashboard.views.order import (
    OrderListView,
    OrderDetailView,
    OrderStatusUpdateView, OrderInvoicePDFView,
)
from dashboard.views.users import UserUpdateView
from dashboard.views.notification import (
    NotificationAPIView,
    NotificationReadView,
)
from dashboard.views.users import UserDeleteView
from dashboard.views.users import UserListView
from dashboard.views.notification import NotificationAPIView
from dashboard.views.order import OrderInvoiceView
urlpatterns = [
path(
    "products/",
    ProductListView.as_view(),
    name="product_list"
),

path(
    "products/create/",
    ProductCreateView.as_view(),
    name="product_create"
),

path(
    "products/<int:pk>/",
    ProductDetailView.as_view(),
    name="product_detail"
),

path(
    "products/<int:pk>/update/",
    ProductUpdateView.as_view(),
    name="product_update"
),

path(
    "products/<int:pk>/delete/",
    ProductDeleteView.as_view(),
    name="product_delete"
),

path(
    "ajax/subcategories/<int:category_id>/",
    load_subcategories,
    name="load_subcategories"
),


path(

    "category/",

    CategoryListView.as_view(),

    name="category_list"

),
path(
    "category/create/",
    CategoryCreateView.as_view(),
    name="category_create",
),
path(
    "category/<int:pk>/",
    CategoryDetailView.as_view(),
    name="category_detail",
),
path(
    "category/<int:pk>/delete/",
    CategoryDeleteView.as_view(),
    name="category_delete",
),
path(
    "category/<int:pk>/edit/",
    CategoryUpdateView.as_view(),
    name="category_edit",

),
path(
    "",
    DashboardView.as_view(),
    name="dashboard"
),
    path(
        "orders/",
        OrderListView.as_view(),
        name="order_list",
    ),

    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order_detail",
    ),

    path(
        "orders/<int:pk>/status/",
        OrderStatusUpdateView.as_view(),
        name="order_status",
    ),
    path(
        "orders/<int:pk>/invoice/",
        OrderInvoiceView.as_view(),
        name="order_invoice",
    ),
path(
    "orders/<int:pk>/invoice/pdf/",
    OrderInvoicePDFView.as_view(),
    name="order_invoice_pdf",
),
path(
    "analytics/",
    AnalyticsView.as_view(),
    name="analytics"
),
path(
    "notifications/",
    NotificationAPIView.as_view(),
    name="notifications_api"
),
path(
    "notifications/<int:pk>/read/",
    NotificationReadView.as_view(),
    name="notification_read",
),
path(
    "users/",
    UserListView.as_view(),
    name="user_list"
),
path(
    "users/<int:pk>/",
    UserDetailView.as_view(),
    name="user_detail"
),
path(
    "users/<int:pk>/edit/",
    UserUpdateView.as_view(),
    name="user_edit"
),
path(
    "users/<int:pk>/delete/",
    UserDeleteView.as_view(),
    name="user_delete",
),


path(
    "subcategory/",
    SubCategoryListView.as_view(),
    name="subcategory_list",
),

path(
    "subcategory/create/",
    SubCategoryCreateView.as_view(),
    name="subcategory_create",
),

path(
    "subcategory/<int:pk>/",
    SubCategoryDetailView.as_view(),
    name="subcategory_detail",
),

path(
    "subcategory/<int:pk>/edit/",
    SubCategoryUpdateView.as_view(),
    name="subcategory_edit",
),

path(
    "subcategory/<int:pk>/delete/",
    SubCategoryDeleteView.as_view(),
    name="subcategory_delete",)

]