from django.shortcuts import render, get_object_or_404
from .models import *
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.

def store(request, category_slug = None, brand_slug = None):
    brands = None
    categories = None
    products = None
    items_per_page = 1

    if category_slug is not None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories, is_available = True).order_by('id')
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count
    elif brand_slug is not None:
        brands = get_object_or_404(Brand, slug = brand_slug)
        products = Product.objects.filter(brand =brands, is_available = True).order_by('id')
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available = True).order_by('id')
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()



    context = {
            'products':paged_products,
            'product_count':product_count,
        }    
    return render(request, 'store/store.html', context)






def product_detail(request, brand_slug, product_slug):
    try:
        single_product = Product.objects.get(brand__slug = brand_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'in_cart' :in_cart
    }
    return render(request, 'store/product_detail.html', context)




def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains = keyword) |
                Q(product_name__icontains = keyword) |
                Q(brand__brand_name__icontains = keyword) |
                Q(category__category_name__icontains = keyword)
            )
            product_count = products.count()

    context = {
        'products':products,
        'product_count' :product_count
    }
    return render(request, 'store/store.html', context)