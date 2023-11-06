from django.contrib import admin
from .models import *
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    

# Brand
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    list_display = ('brand_name', 'slug')

admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'brand', 'modified_date', 'is_available')
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductGalleryInline]

admin.site.register(Product, ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')
admin.site.register(Variation, VariationAdmin)




admin.site.register(ReviewRating)

admin.site.register(ProductGallery)