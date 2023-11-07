from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.models import Account
from .forms import *
from store.models import *
from django.utils.text import slugify



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