from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name




class SubCategory(models.Model):
    category= models.ForeignKey(
        Category, on_delete=models.CASCADE,related_name='subcategories'
    )
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True)


    image = models.ImageField(
        upload_to='subcategory/',
        blank=True,
        null=True)

    def __str__(self):
        return self.name





class Product(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()

    discount = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def final_price(self):
        return self.price - (self.price * self.discount // 100)

    def __str__(self):
        return self.title



class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL','XXL'),
    ]
    stock = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "size"],
                name="unique_product_size"
            )
        ]

    def __str__(self):
        return f"{self.product.title} - {self.size}"

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="product_gallery/"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title






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


class Sharh(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sharh')
    name = CharField(max_length=50)
    about = models.TextField()
    rating = models.CharField(max_length=5)

    def __str__(self):
        return self.about

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
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class Order(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=30)

    address = models.TextField()

    total_price = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def calculate_total(self):
        total = sum(
            item.total for item in self.items.all()
        )

        self.total_price = total

        self.save(update_fields=["total_price"])

        return total

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    size = models.ForeignKey(
        ProductSize,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField()

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
            f"({self.size.size})"
        )



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

        ("manager", "Manager"),

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