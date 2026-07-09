
from django.contrib import admin

from .models import Product, ProductImage, ProductSize, Category, Sharh, SubCategory,Branch,Career,Banner
from .models import Order, OrderItem,Profile
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(Category)
admin.site.register(Sharh)
admin.site.register(SubCategory)
admin.site.register(Branch)
admin.site.register(Career)
admin.site.register(Banner)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)


