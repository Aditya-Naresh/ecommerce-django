from django.shortcuts import render
from store.models import Product
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    products = Product.objects.filter(is_available = True)
    context = {
        'products':products
    }
    return render(request, "home/home.html", context)