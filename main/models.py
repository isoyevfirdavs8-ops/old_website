from django.contrib.auth.models import User

from main.managers import ProductManager
from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(max_length=100)

    name_ru = models.CharField(
        max_length=100,
        blank=True
    )
    use_mega_menu = models.BooleanField(
        default=False)

    slug = models.SlugField(
        unique=True,
        blank=True

    )



    is_active = models.BooleanField(
        default=True
    )

    ordering = models.PositiveIntegerField(
        default=0
    )

    class Meta:

        ordering = ["ordering", "name"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class SubCategory(models.Model):

    PAGE_TYPES = (
        ("product", "Product"),
        ("branch", "Branch"),
        ("career", "Career"),

    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(max_length=100)

    name_ru = models.CharField(
        max_length=100,
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="subcategories/",
        blank=True,
        null=True
    )



    ordering = models.PositiveIntegerField(
        default=0
    )

    page_type = models.CharField(
        max_length=20,
        choices=PAGE_TYPES,
        default="product"
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["ordering", "name"]



    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "subcategory_products",
            args=[self.id]
        )

    def __str__(self):
        return self.name



class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    # Tabs
    shipping = models.TextField(
        blank=True,
        verbose_name="Yetkazib berish"
    )

    payment = models.TextField(
        blank=True,
        verbose_name="To'lov"
    )

    specification = models.TextField(
        blank=True,
        verbose_name="Qo'shimcha ma'lumot"
    )

    price = models.PositiveIntegerField()

    discount = models.PositiveIntegerField(
        default=0
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = ProductManager()

    @property
    def average_rating(self):
        result = self.reviews.filter(
            is_active=True
        ).aggregate(
            Avg("rating")
        )

        return result["rating__avg"] or 0

    @property
    def review_count(self):
        return self.reviews.filter(
            is_active=True
        ).count()

    @property
    def five_star(self):
        return self.reviews.filter(
            rating=5,
            is_active=True
        ).count()

    @property
    def final_price(self):
        return self.price - (
            self.price * self.discount // 100
        )

    @property
    def first_image(self):
        image = self.gallery.first()
        return image.image.url if image else ""

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="colors",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=50)

    code = models.CharField(
        max_length=7,
        help_text="#000000"
    )

    def __str__(self):
        return f"{self.product.title} - {self.name}"

class ProductSize(models.Model):

    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    color = models.ForeignKey(
        ProductColor,
        related_name="sizes",
        on_delete=models.CASCADE,
    )

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
    )

    stock = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["color", "size"],
                name="unique_color_size",
            )
        ]

    def __str__(self):
        return f"{self.color} - {self.size}"




class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="gallery",
        on_delete=models.CASCADE
    )

    color = models.ForeignKey(
        ProductColor,
        related_name="images",
        on_delete=models.CASCADE
    )


    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product.title} - {self.color.name}"



class ProductReview(models.Model):

    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    avatar = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, "★"),
            (2, "★★"),
            (3, "★★★"),
            (4, "★★★★"),
            (5, "★★★★★"),
        ]
    )

    comment = models.TextField()

    verified_purchase = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return f"{self.name} ({self.rating})"



class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"



class Branch(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    work_time = models.CharField(max_length=40)

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Career(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return self.name




class Banner(models.Model):

    title = models.CharField(
        max_length=200,

    )

    subtitle = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="banners/"
    )

    button_text = models.CharField(
        max_length=50,
        blank=True
    )

    button_url = models.CharField(
        max_length=255,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["order"]

        verbose_name = "Banner"

        verbose_name_plural = "Banners"

    def __str__(self):

        return self.title



class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("waiting_payment", "Waiting Payment"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipping", "Shipping"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_CHOICES = (
        ("cash", "Naqd"),
        ("click", "Click"),
        ("payme", "Payme"),
    )

    DELIVERY_CHOICES = (
        ("courier", "Courier"),
        ("pickup", "Pickup"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=30
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    address = models.TextField()

    note = models.TextField(
        blank=True,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="cash",
    )

    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default="courier",
    )

    delivery_price = models.PositiveIntegerField(
        default=0
    )

    subtotal = models.PositiveIntegerField(
        default=0
    )

    discount = models.PositiveIntegerField(
        default=0
    )

    total_price = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def calculate_total(self):


        self.subtotal = sum(
            item.total for item in self.items.all()
        )

        total = (
            self.subtotal
            + self.delivery_price
            - self.discount
        )


        self.total_price = max(total, 0)

        self.save(
            update_fields=[
                "subtotal",
                "total_price",
            ]
        )

        return self.total_price

    @property
    def total_items(self):
        return sum(
            item.quantity for item in self.items.all()
        )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
    )

    size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return (
            f"{self.product.title} "
            f"({self.size.size}) x {self.quantity}"
        )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class StockMovement(models.Model):

    MOVEMENT_CHOICES = (
        ("sale", "Sale"),
        ("refund", "Refund"),
        ("restock", "Restock"),
        ("manual", "Manual"),
    )

    product_size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        related_name="stock_movements",
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_CHOICES,
    )

    quantity = models.IntegerField()

    before_stock = models.PositiveIntegerField()

    after_stock = models.PositiveIntegerField()

    note = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.product_size} | "
            f"{self.movement_type} | "
            f"{self.quantity}"
        )

class OTPVerification(models.Model):

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    code = models.CharField(
        max_length=6
    )

    is_verified = models.BooleanField(
        default=False
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )



class Payment(models.Model):
    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("waiting", "Waiting"),

        ("paid", "Paid"),

        ("failed", "Failed"),

        ("expired", "Expired"),

        ("cancelled", "Cancelled"),

        ("refunded", "Refunded"),

    )

    PROVIDER_CHOICES = (
        ("cash", "Cash"),
        ("click", "Click"),
        ("payme", "Payme"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    failure_reason = models.TextField(

        blank=True,

        default="",

    )

    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
    )

    amount = models.PositiveIntegerField()

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting",
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.order.id} - {self.provider}"



class Activity(models.Model):

    ACTIONS = [

        ("order_created", "Order Created"),
        ("order_delivered", "Order Delivered"),
        ("product_created", "Product Created"),
        ("product_updated", "Product Updated"),
        ("product_deleted", "Product Deleted"),
        ("category_created", "Category Created"),
        ("user_registered", "User Registered"),

    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=50,
        choices=ACTIONS
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.message



class Notification(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.title




class Profile(models.Model):
    categories = models.ManyToManyField(
        "Category",
        blank=True,
        related_name="allowed_sellers"
    )

    ROLE_CHOICES = (

        ("admin", "Admin"),

        ("managers", "Manager"),

        ("staff", "Staff"),

        ("seller", "Seller"),

        ("customer", "Customer"),

    )

    GENDER_CHOICES = (

        ("male", "Male"),

        ("female", "Female"),

    )

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="profile"

    )

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES,

        default="customer"

    )

    avatar = models.ImageField(

        upload_to="users/",

        blank=True,

        null=True

    )

    phone = models.CharField(

        max_length=20,

        blank=True

    )

    address = models.TextField(

        blank=True

    )

    date_of_birth = models.DateField(

        blank=True,

        null=True

    )

    gender = models.CharField(

        max_length=10,

        choices=GENDER_CHOICES,

        blank=True

    )

    telegram = models.CharField(

        max_length=100,

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return self.user.username





class OrderLog(models.Model):

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="logs",

    )

    old_status = models.CharField(

        max_length=30,

        blank=True,

    )

    new_status = models.CharField(

        max_length=30,

    )

    changed_by = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="order_logs",

    )

    comment = models.TextField(

        blank=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = ["created_at"]

    def __str__(self):

        return (

            f"#{self.order.id}"

            f" {self.old_status}"

            f" → "

            f"{self.new_status}"

        )









class PaymentTransaction(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    payment = models.ForeignKey(
        "Payment",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    provider = models.CharField(
        max_length=30,
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
    )

    processed_at = models.DateTimeField(

        null=True,

        blank=True,

    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    request_data = models.JSONField(
        default=dict,
        blank=True,
    )

    response_data = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Payment Transaction"

        verbose_name_plural = "Payment Transactions"

    def __str__(self):

        return f"{self.provider} | {self.transaction_id}"



class PaymentAudit(models.Model):

    STATUS_CHOICES = (

        ("success", "Success"),

        ("failed", "Failed"),

    )

    payment = models.ForeignKey(

        "Payment",

        on_delete=models.CASCADE,

        related_name="audits",

    )

    provider = models.CharField(

        max_length=20,

    )

    endpoint = models.CharField(

        max_length=255,

    )

    ip_address = models.GenericIPAddressField(

        null=True,

        blank=True,

    )

    user_agent = models.TextField(

        blank=True,

        default="",

    )

    request_headers = models.JSONField(

        default=dict,

        blank=True,

    )

    request_body = models.JSONField(

        default=dict,

        blank=True,

    )

    response_body = models.JSONField(

        default=dict,

        blank=True,

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

    )

    error = models.TextField(

        blank=True,

        default="",

    )

    duration_ms = models.PositiveIntegerField(

        default=0,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = [

            "-created_at",

        ]

    def __str__(self):

        return f"{self.provider} - {self.status}"


class OrderStatusHistory(models.Model):

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="status_history",

    )

    old_status = models.CharField(

        max_length=20,

        blank=True,

    )

    new_status = models.CharField(

        max_length=20,

    )

    changed_by = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    note = models.TextField(

        blank=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Order Status History"

        verbose_name_plural = "Order Status Histories"

    def __str__(self):

        return f"#{self.order.id} {self.old_status} → {self.new_status}"





class SiteSettings(models.Model):

    # =====================================
    # GENERAL
    # =====================================

    site_name = models.CharField(
        max_length=150,
        default="Dunyo Textile"
    )

    site_description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="settings/logo/",
        blank=True,
        null=True
    )

    favicon = models.ImageField(
        upload_to="settings/favicon/",
        blank=True,
        null=True
    )

    # =====================================
    # CONTACT
    # =====================================

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    working_hours = models.CharField(
        max_length=150,
        blank=True
    )

    # =====================================
    # SOCIAL
    # =====================================

    telegram = models.URLField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    facebook = models.URLField(
        blank=True
    )

    youtube = models.URLField(
        blank=True
    )

    tiktok = models.URLField(
        blank=True
    )

    # =====================================
    # MAP
    # =====================================

    latitude = models.FloatField(
        default=41.3111
    )

    longitude = models.FloatField(
        default=69.2797
    )

    map_zoom = models.PositiveSmallIntegerField(
        default=12
    )

    # =====================================
    # SEO
    # =====================================

    meta_title = models.CharField(
        max_length=200,
        blank=True
    )

    meta_description = models.TextField(
        blank=True
    )

    meta_keywords = models.TextField(
        blank=True
    )

    # =====================================
    # SYSTEM
    # =====================================

    default_language = models.CharField(
        max_length=20,
        choices=[
            ("uz", "Uzbek"),
            ("en", "English"),
            ("ru", "Russian"),
        ],
        default="uz"
    )

    default_currency = models.CharField(
        max_length=10,
        choices=[
            ("UZS", "UZS"),
            ("USD", "USD"),
            ("EUR", "EUR"),
        ],
        default="UZS"
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Tashkent"
    )

    products_per_page = models.PositiveIntegerField(
        default=12
    )

    orders_per_page = models.PositiveIntegerField(
        default=20
    )

    dashboard_theme = models.CharField(
        max_length=20,
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
        ],
        default="dark"
    )

    maintenance_mode = models.BooleanField(
        default=False
    )

    registration_open = models.BooleanField(
        default=True
    )

    # =====================================
    # EXTRA
    # =====================================

    copyright_text = models.CharField(
        max_length=255,
        default="© Dunyo Textile. All rights reserved."
    )

    footer_text = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================
    # META
    # =====================================

    class Meta:

        verbose_name = "Site Settings"

        verbose_name_plural = "Site Settings"

    # =====================================
    # SINGLETON
    # =====================================

    def save(self, *args, **kwargs):

        self.pk = 1

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):

        obj, created = cls.objects.get_or_create(pk=1)

        return obj

    def __str__(self):

        return "Website Settings"