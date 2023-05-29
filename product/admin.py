from django.contrib import admin
from .models import Product, Category, Cart, Payment, Order
from django.urls import reverse
from django.utils.html import format_html
import admin_thumbnails
# Register your models here.


@admin.register(Category)
@admin_thumbnails.thumbnail('category_image')
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}



admin.site.register(Product, ProductAdmin)


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_display_links = ['user']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount']

@admin_thumbnails.thumbnail('image')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

