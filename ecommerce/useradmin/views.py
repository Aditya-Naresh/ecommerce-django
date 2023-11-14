from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.models import Account
from .forms import *
from store.models import *
from django.utils.text import slugify
from orders.models import Order
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from orders.models import *
from offers.models import *
from coupon.models import Coupon



# Create your views here.

def decorator(request):
    return render(request, 'decorator.html')


@login_required(login_url='login')
def useradmin(request):
    if request.user.is_admin:
        return render(request, 'index.html')
    else:
        return redirect('decorator')
    
#=====================================================CUSTOMERS=================================================================

def customers(request):
    items_per_page = 10
    if request.user.is_admin:
        p = Paginator(Account.objects.filter(is_admin = False).order_by('id'), items_per_page)
        page = request.GET.get('page')
        customers = p.get_page(page)        
        context = {
            'customers':customers
        }
        return render(request,'users/customers.html', context)
    else:
        return redirect('decorator')
   #----------------------------------------------------------------------------------------------------------- 

def block_user(request,user_id):
    if request.user.is_admin:
        user = Account.objects.get(id = user_id)
        user.is_active = False
        user.is_blocked = True
        user.save()
        return redirect('customers')
    else:
        return redirect('decorator')
    
# -------------------------------------------------------------------------------------------------------------------


def unblock_user(request,user_id):
    if request.user.is_admin:
        user = Account.objects.get(id = user_id)
        user.is_active = True
        user.is_blocked = False
        user.save()
        return redirect('customers')
    else:
        return redirect('decorator')
    

# =====================================================================Admins====================================================


def admin_list(request):
    items_per_page = 10
    if request.user.is_admin:
        p = Paginator(Account.objects.filter(is_admin = True).order_by('id'), items_per_page)
        page = request.GET.get('page')
        admins = p.get_page(page)        
        context = {
            'admins':admins
        }
        return render(request,'users/admin_list.html', context)
    else:
        return redirect('decorator')
    
    # ---------------------------------------------------------------------------------

def delete_admin(request,user_id):
    if request.user.is_admin:
        user = Account.objects.get(id = user_id)
        user.delete()
        return redirect('admin_list')
    else:
        return redirect('decorator')    
    
# ------------------------------------------------------------------------------------------------

def create_admin(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form  = AdminForm(request.POST)
            if form.is_valid():
                admin = form.save(commit=False)
                admin.is_admin = True
                admin.is_staff = True
                admin.is_active = True
                admin.is_superadmin =True
                admin.is_blocked = False
                admin.save()
                return redirect('admin_list')
        form = AdminForm()
        context = {
            "form":form,
        }
        return render(request, 'users/create_admin.html', context)
    else:
        return redirect('decorator')
    

# =================================================CATEGORIES===========================================================
def categories(request):
    items_per_page = 15
    p = Paginator(Category.objects.all(), items_per_page)
    page = request.GET.get('page')
    categories = p.get_page(page)
    context = {
        'categories':categories
    }
    return render(request,'categories/categories.html',context)

# -----------------------------------------------------------------------------------------------------------

def edit_category(request,cat_id):
    cat = Category.objects.get(id=cat_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance = cat)

        if form.is_valid():
            form.save()
            return redirect('categories')
    
    
    form = CategoryForm(instance=cat)

    context = {
        "form":form
    }
    return render(request, 'categories/category_form.html', context )

# ----------------------------------------------------------------------------------------------------------------

def delete_category(request, cat_id):
    cat = Category.objects.get(id=cat_id)
    cat.delete()
    return redirect('categories')

# -----------------------------------------------------------------------------------------------------------------

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form  = CategoryForm()
    context = {
        'form': form
    }
    return render(request,'categories/category_form.html', context)





# =================================================================================BRANDS=========================================
def brands(request):
    items_per_page = 15
    p = Paginator(Brand.objects.all(), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)
    context = {
        'data':data
    }
    return render(request, 'brands/brands.html', context)


# ------------------------------------------------------------------------------------------------------------------

def edit_brand(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance = brand)

        if form.is_valid():
            form.save()
            return redirect('brands')
    
    
    form = BrandForm(instance=brand)

    context = {
        "form":form
    }
    return render(request, 'brands/brand_form.html', context )

# -----------------------------------------------------------------------------------------------
def delete_brand(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand.delete()
    return redirect('brands')

# ------------------------------------------------------------------------------------------------------

def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('brands')
    form = BrandForm()
    context = {
        'form':form,
    }
    return render(request, 'brands/brand_form.html', context)


# ===========================================================PRODUCTS==============================================
def products(request):
    items_per_page = 15
    p = Paginator(Product.objects.all(), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)
    context={
        "data": data
    }
    return render(request, 'products/products.html', context)

# ------------------------------------------------------------------------------------------------------------------

def edit_product(request, product_id):

    product = Product.objects.get(pk = product_id)
    images = ProductGallery.objects.filter(product = product_id)
    image_form = ImageForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance = product)
        images = request.FILES.getlist('Images')

        if form.is_valid():
            for image in images:
                pic = ProductGallery.objects.create(
                    product = product,
                    image = image
                )
            form.save()
            
            return redirect('products')

    form = ProductForm(instance = product)

    context = {
        'form':form,
        'image_form':image_form,
        'images':images
    }

    return render(request, 'products/product_form.html',context)


def delete_image(request, image_id):
    image = ProductGallery.objects.get(id = image_id)
    product_id = image.product.pk

    url = reverse('edit_product', kwargs={'product_id': product_id})

    image.delete()

    return redirect(url)
  


# --------------------------------------------------------------------------------------------------------

def delete_product(request,product_id):
    product = Product.objects.get(id = product_id)
    product.delete()
    return redirect('products')

# -----------------------------------------------------------------------------------
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('Images')
        if form.is_valid():
            product = form.save()
            for image in images:
                pic = ProductGallery.objects.create(
                    product = product,
                    image = image
                )
            return redirect('products')
    form  = ProductForm()
    image_form = ImageForm()
    context = {
        'form':form,
        'image_form':image_form
    }
    return render(request,'products/product_form.html',context)



# =============================================PRODUCT VARIATIONS==================================
def variations(request):
    items_per_page = 15
    p = Paginator(Variation.objects.all(), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)
    context={
        "data": data
    }
    
    return render(request,'product_variations/variations.html', context)


# -------------------------------------------------------------------------------------------------

def edit_variation(request, variation_id):
    variation = Variation.objects.get(id = variation_id)

    if request.method == 'POST':
        form = VariationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('variations')

    form = VariationForm(instance=variation)

    context = {
        'form':form
    }

    return render(request, 'product_variations/variation_form.html', context)


# ---------------------------------------------------------------------------------------

def delete_variation(request, variation_id):
    variation = Variation.objects.get(id = variation_id)
    variation.delete()
    return redirect('variations')


# ---------------------------------------------------------------------------------------


def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('variations')
    
    form = VariationForm()

    context = {
        'form': form
    }

    return render(request,'product_variations/variation_form.html', context)




# ==============================================================================ORDERS==========================================================================




def orders(request):
    items_per_page = 15
    p = Paginator(Order.objects.all().order_by('-created_at'), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)

    context = {
        'data':data
    }
    return render(request,'orders/orders.html', context)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

def ship(request, order_id):
    order = Order.objects.get(id = order_id)

    order.status = 'Shipped'
    order.save()
    current_site = get_current_site(request)
    email = order.email
    mail_subject = 'Order Shipped'
    message = render_to_string('orders/shipped_mail.html',{
        'order':order,
        'domain' : current_site,
    })            
    to_email = email
    send_mail = EmailMessage(mail_subject, message, to = [to_email])
    send_mail.send()

    return redirect('orders')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

def order_detail(request, order_id):
    order = Order.objects.get(id = order_id)
    products = OrderProduct.objects.filter(order = order)

    total_price = order.order_total
    if order.coupon:
        total_price -= order.coupon.discount_price
    subtotal = 0
    for product in products:
        subtotal += product.quantity * product.product_price


    context = {
        'order': order,
        'products': products,
        'total_price': total_price,
        'subtotal':subtotal
    }
    return render(request, 'orders/order_detail.html', context)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def new_orders(request):
    items_per_page = 20
    p = Paginator(Order.objects.filter(status = 'New'), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)    
    context = {
        'data': data
    }
    return render(request, 'orders/new_orders.html', context)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def cancelled_orders(request):
    items_per_page = 15
    p = Paginator(Order.objects.filter(status = 'Cancelled').order_by('-created_at'), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)

    context = {
        'data':data
    }
    return render(request, 'orders/cancelled_orders.html', context)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def restock(request, order_id):
    order = Order.objects.get(id = order_id)
    order_products = OrderProduct.objects.filter(order = order)

    for order_product in order_products:
        product = order_product.product
        print(product.stock)
        product.stock += order_product.quantity

        product.save()
        print(product.stock)

    order.restock = True
    order.save()

    return redirect('cancelled_orders')




# =========================================================================== PRODUCT OFFER ==========================================================================================

def product_offer(request):
    items_per_page = 20
    p = Paginator(ProductOffer.objects.all().order_by('-id'), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)  
    context = {
        'data': data
    }
    return render(request, 'product_offer/product_offer.html', context)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_product_offer(request):
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('product_offer')
    form  = ProductOfferForm()

    context = {
        'form':form
    }

    return render(request, 'product_offer/product_offer_form.html', context)



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_product_offer(request, product_offer_id):
    productOffer = ProductOffer.objects.get(id = product_offer_id)
    if request.method == 'POST':
        form = ProductOfferForm(request.POST, instance=productOffer)

        if form.is_valid():
            form.save()
            return redirect('product_offer')
    form = ProductOfferForm(instance=productOffer)
    context = {
        'form':form
    }

    return render(request, 'product_offer/product_offer_form.html', context)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_product_offer(request, product_offer_id):
    product_offer = ProductOffer.objects.get(id = product_offer_id)
    product_offer.delete()
    return redirect('product_offer')

# ===================================================== CATEGORY OFFER ===============================================================================================================

def category_offer(request):
    items_per_page = 20
    p = Paginator(CategoryOffer.objects.all().order_by('-id'), items_per_page)
    page = request.GET.get('page')
    data = p.get_page(page)  
    context = {
        'data': data
    }
    return render(request, 'category_offer/category_offer.html', context)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def add_category_offer(request):
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('category_offer')
    form  = CategoryOfferForm()

    context = {
        'form':form
    }

    return render(request, 'category_offer/category_offer_form.html', context)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def edit_category_offer(request, category_offer_id):
    catOffer = CategoryOffer.objects.get(id = category_offer_id)
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST, instance=catOffer)

        if form.is_valid():
            form.save()
            return redirect('category_offer')
    form = CategoryOfferForm(instance=catOffer)
    context = {
        'form':form
    }

    return render(request, 'category_offer/category_offer_form.html', context)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_category_offer(request, category_offer_id):
    catOffer =  CategoryOffer.objects.get(id = category_offer_id)

    catOffer.delete()
    return redirect('category_offer')


# ===================================== COUPONS =============================================================================================================================================================================

def coupons(request):
    data = Coupon.objects.all()
    context = {
        'data':data
    }
    return render(request, 'coupons/coupons.html', context)



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('coupons')
    form = CouponForm()

    context = {
        'form':form
    }

    return render(request, 'coupons/coupon_form.html',context)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id = coupon_id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupons')
    form = CouponForm(instance=coupon)
    context = {
        'form':form
    }
    return render(request, 'coupons/coupon_form.html', context)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.delete()

    return redirect('coupons')