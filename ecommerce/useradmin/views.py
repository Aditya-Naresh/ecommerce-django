from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.models import Account


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
        return render(request, 'users/create_admin.html')
    else:
        return redirect('decorator')