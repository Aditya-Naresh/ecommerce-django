from django.contrib import admin
from .models import Product, Brand
# Register your models here.

# Brand
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    list_display = ('brand_name', 'slug')

admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'brand', 'modified_date', 'is_available')
    prepopulated_fields = {'slug' : ('product_name',)}

admin.site.register(Product, ProductAdmin)
