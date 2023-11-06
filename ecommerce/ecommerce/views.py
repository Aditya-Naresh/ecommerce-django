from django.shortcuts import render
from store.models import Product,ReviewRating
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    products = Product.objects.filter(is_available = True).order_by('created_date')
 
    for single_product in products:
        review = ReviewRating.objects.filter(product_id = single_product.id, status = True)
        
    context = {
        'products':products,
        'review': review
    }
    return render(request, "home/home.html", context)