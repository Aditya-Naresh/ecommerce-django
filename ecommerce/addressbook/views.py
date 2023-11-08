from django.shortcuts import render,redirect
from .models import *
from .forms import *
# Create your views here.

def activate(request,address_id):
    addresses = UserAddressBook.objects.filter(user = request.user)
    for add in addresses:
        add.status = False
        add.save()
    
    active_address = UserAddressBook.objects.get(id = address_id)
    active_address.status = True
    active_address.save()

    return redirect('checkout')


def add_address(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')
    form = UserAddressForm()
    context = {
        'form':form
    }
    return render(request, 'addressbook/addressform.html',context)



def edit_address(request, address_id):
    address = UserAddressBook.objects.get(id = address_id, user= request.user)

    form = UserAddressForm(instance = address)


    context = {
        'form': form
    }

    return render(request, "addressbook/addressform.html", context)