from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse  
from carts.models import CartItem
from .forms import OrderForm
from .models import *
import datetime
import json

from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

def render_to_pdf(template_path, context):
    template = get_template(template_path)
    html = template.render(context)
    response = BytesIO()
    
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        response,
        pagesize='letter'  # Set the page size to letter (8.5 x 11 inches)
    )
    
    if not pdf.err:
        response.seek(0)
        return response
    return None

def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    payment = Payment.objects.get(payment_id=order.payment.payment_id)
    subtotal = 0

    for item in ordered_products:
        subtotal += item.product_price * item.quantity


    context = {
        'order': order,
        'order_number': order.order_number,
        'transID': payment.payment_id,
        'ordered_products': ordered_products,
        'subtotal': subtotal,
        'status': payment.status
    }

    template_path = 'orders/invoice.html'  # Replace with the path to your HTML template
    pdf_response = render_to_pdf(template_path, context)

    if pdf_response:
        response = HttpResponse(pdf_response.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_{order.order_number}.pdf'
        return response

    # Handle the case where PDF generation fails
    return HttpResponse('PDF generation failed', status=500)




def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered = False, order_number = body['orderID'])
    # Transactions details 
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move Cart Items to Order Product 
    cart_items = CartItem.objects.filter(user = request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)

        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()
        
    # Reduce the Stock
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
    #  Clear Cart
    CartItem.objects.filter(user = request.user).delete()

    # Send order recieved mail to customer
    mail_subject = 'Order Placed'
    message = render_to_string('orders/order_received_email.html',{
        'user':request.user,
        'order': order,
    })            
    to_email = request.user.email
    send_mail = EmailMessage(mail_subject, message, to = [to_email])
    send_mail.send()
    

    # Send order number and transaction id back to send Data

    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,

    }
    return JsonResponse(data)

def place_order(request, total=0, quantity = 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
        
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.pincode = form.cleaned_data["pincode"]
            data.order_note = form.cleaned_data["order_note"]
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate Order No
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")

            ordernumber = current_date + str(data.id)
            data.order_number = ordernumber
            data.save()


            order = Order.objects.get(user = current_user, is_ordered=False, order_number = ordernumber)
            
            context = {
                'order' : order,
                'cart_items': cart_items,
                'total' : total,
                'tax':tax,
                'grand_total': grand_total
            }

            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')










def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id = transID)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context ={
            'order':order,
            'ordered_products': ordered_products,
            'order_number':order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal' :subtotal,
        }



    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

    return render(request, 'orders/order_complete.html', context)
