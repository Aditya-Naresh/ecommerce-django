from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from wishlist.models import Wishlist
from addressbook.forms import UserAddressForm
from addressbook.models import UserAddressBook
from django.contrib import messages
from coupon.forms import CouponForm

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id = product_id)
    wishlist_item = Wishlist.objects.filter(user = current_user, product=product)

    # check user authetication
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            wishlist_item.delete()
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product = product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass


        print(product_variation)
        is_cart_item_exists = CartItem.objects.filter(product = product, user = current_user)
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product= product, user = current_user)
            existing_variations_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variation.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variations_list:
                # increase Quantity
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item =CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()

            else:
                # Create 
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user
                )

                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()


        return redirect('cart')

# For guest user
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) #Session cart ID
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart)
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product= product, cart = cart)
            existing_variations_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variation.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variations_list:
                # increase Quantity
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item =CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()

            else:
                # Create 
                item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart
                )

                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()


        return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user = request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')





def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product, user = request.user,id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')




def cart(request, total=0, quantity = 0 , cart_items = None):
  
    tax_rate = 2
    tax = 0
    grand_total =0
    discount = 0
    coupon = None
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id  = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item .quantity)
            quantity += cart_item.quantity
            try:        
                discount = cart_item.cart.coupon.discount_price
                coupon_used = True
                coupon = cart_item.cart.coupon
            except:
                pass
        tax = (tax_rate * total)/100    
        grand_total = total + tax - discount
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantitiy' : quantity,
        'cart_items' : cart_items,
        'tax' :tax,
        'grand_total':grand_total,
       
    }
        
    return render(request, "carts/cart.html", context)


@login_required(login_url='login')
def checkout(request, total=0, quantity = 0 , cart_items = None):
    coupon_used = False
    discount_price = 0
    coupon = CouponForm(request.GET)
    coupon_obj = None
    code = None
    if coupon.is_valid():
        code = coupon.cleaned_data['code']
        coupon_obj = Coupon.objects.get(code = code)
        discount_price = coupon_obj.discount_price
        coupon_used = True
    coupon_form = CouponForm()


    try:
        tax_rate = 2
        tax = 0
        grand_total =0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id  = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item .quantity)
            quantity += cart_item.quantity

        tax = (tax_rate * total)/100         
        grand_total = total + tax 

        if coupon_obj is not None:
            if grand_total > coupon_obj.minimum_amount:
                grand_total -= discount_price
            else:
                coupon_used = False
                messages.warning(request, 'You should purchase more than $'+ str(coupon_obj.minimum_amount) +' to use this coupon')
    
    except ObjectDoesNotExist:
        pass

    try:
        address = UserAddressBook.objects.get(user=request.user, status = True)
        form = UserAddressForm(instance = address)
    except:
        form = UserAddressForm()



    try:    
        addresses = UserAddressBook.objects.filter(user=request.user)
    except UserAddressBook.DoesNotExist:
        addresses = None
    

  
    context = {
        'total':total,
        'quantitiy' : quantity,
        'cart_items' : cart_items,
        'tax' :tax,
        'grand_total':grand_total,
        'form':form,
        'addresses': addresses,
        'coupon_form':coupon_form,
        'coupon_used':coupon_used,
        'code' :code,
        'discount':discount_price
    }

    return render(request, 'carts/checkout.html', context)



