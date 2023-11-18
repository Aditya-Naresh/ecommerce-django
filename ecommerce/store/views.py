from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from wishlist.models import Wishlist
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

def store(request, category_slug = None, brand_slug = None):
    brands = None
    categories = None
    products = None
    reviews = None
    items_per_page = 6

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
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available = True).order_by('id')
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id, status = True)


    

    context = {
            'products':paged_products,
            'product_count':product_count,
            'reviews': reviews,
        }    
    return render(request, 'store/store.html', context)


# ============================================================= PRODUCT DETAIL ======================================================================================


def product_detail(request, brand_slug, product_slug):
    try:
        single_product = Product.objects.get(brand__slug = brand_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = False
    else:
        orderproduct = False


    # Get reviews
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)
    product_gallery = Images.objects.filter(product_id = single_product.id) 
    colors = Variation.objects.filter(product = single_product).values('color__id', 'color__name', 'color__code').distinct()
    size = Variation.objects.filter(product = single_product).values('size__id', 'size__name', 'price', 'color__id')
   
    context = {
        'single_product':single_product,
        'in_cart' :in_cart,
        'orderproduct':orderproduct,
        'reviews' : reviews,
        'product_gallery' : product_gallery,
        'sizes':size,
        'colors':colors,
        # 'variant':variant,
        
    }
    return render(request, 'store/product_detail.html', context)


#========================================== SEARCH =================================================================================================================

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

# =================================================  REVIEWS =========================================================================================================

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id= product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']

                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")
                return redirect(url)
            
# ============================================== BRAND LIST =======================================================================================================
def brand_list(request):
    brands = Brand.objects.all()
    context = {
        'brands' : brands
    }
    return render(request, 'store/brand_list.html', context)



# =================================================== CATEGORY LIST =================================================================================================
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'store/category_list.html', context)



# ==================================================== FILTER DATA ===========================================================================================================

def filter_data(request):
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    sizes=request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    sort = request.GET['sort']

    allProducts = Product.objects.all().order_by('-id')

    allProducts = allProducts.filter(price__gte = minPrice)
    allProducts = allProducts.filter(price__lte = maxPrice)
    if len(colors) > 0:
        allProducts = allProducts.filter(variation__variation_value__in=colors).distinct()

    if len(sizes) > 0:
        allProducts = allProducts.filter(variation__variation_value__in=sizes).distinct()

    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in =categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in =brands).distinct()

    if sort:
        allProducts = allProducts.order_by(sort)
        
    t = render_to_string('ajax/product-list.html', {'products': allProducts })
    return JsonResponse({'data' : t})





