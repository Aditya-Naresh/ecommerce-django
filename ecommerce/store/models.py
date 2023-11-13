from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.utils.text import slugify
from decimal import Decimal

from offers.models import ProductOffer

# Create your models here.

# Brand
class Brand(models.Model):
    brand_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='photos/brands')


    def save(self, *args, **kwargs):
        # Generate the slug based on the name if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.brand_name)

        super(Brand, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('products_by_brand', args=[self.slug])

    def __str__(self) -> str:
        return self.brand_name



class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    offer = models.ForeignKey(ProductOffer, on_delete=models.CASCADE, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



    def calculate_discounted_price(self):
        if self.category.offer:
            if self.category.offer.offer_type == 'PERCENT':
                discounted_price = self.price - (self.price * (self.category.offer.discount_rate / 100))
            elif self.category.offer.offer_type == 'FIXED':
                discounted_price = self.price -  self.category.offer.discount_rate
        elif self.offer:
            if self.offer.offer_type == 'PERCENT':
                discounted_price = self.price - (self.price * (self.offer.discount_rate/100))
            elif self.offer.offer_type == 'FIXED':
                discounted_price = self.price - self.offer.discount_rate
        
        else :
            discounted_price = self.price

        return Decimal(discounted_price)


    def save(self, *args, **kwargs):
        # Generate the slug based on the name if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.product_name)
        self.discounted_price = self.calculate_discounted_price()
        super(Product, self).save(*args, **kwargs)


    def get_url(self):
        return reverse('product_detail', args=[self.brand.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name
    

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average = Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])

        return avg 

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count = Count('rating'))
        count = 0

        if reviews['count'] is not None:
            count = float(reviews['count'])

        return count 


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category = 'color', is_active = True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category = 'size', is_active = True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return self.variation_value
    



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject =models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self) -> str:
        return self.subject
    


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)


    class Meta:
        verbose_name_plural = 'product galleries'

    def __str__(self) -> str:
        return self.product.product_name
