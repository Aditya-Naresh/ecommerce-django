from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

# Brand
class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='photos/brands')

    def get_url(self):
        return reverse('products_by_brand', args=[self.slug])

    def __str__(self) -> str:
        return self.brand_name



class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.brand.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name