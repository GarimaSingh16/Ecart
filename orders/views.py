from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from carts.models import CartItem
from store.models import Product
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def place_order(request,total = 0 , quantity=0 ):
    current_user = request.user
    
    # if the cart_items/cart_count less than or equal to 0 , then redirect user back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    grand_total = 0
    tax = 0
    total = 0 
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity
    tax = total * 0.02
    grand_total = total+tax
        
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            if form.is_valid():
                # store all the billing information inside Order table
                data = Order() 
                # print('data:',data)
                data.user = current_user           
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.pincode = form.cleaned_data['pincode']
                data.order_note = form.cleaned_data['order_note']
                data.order_total = grand_total 
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                
                # Generating order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime('%Y%m%d') #20210305 - 2021-year,10=month,05=date
                
                order_number = current_date + str(data.id)
                
                data.order_number = order_number
                data.save()
                # messages.success(request,'Order Placed Successfully')
                
                order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
                
                grand_total = 0
                tax = 0
                total = 0 
                for cart_item in cart_items:
                    total += (cart_item.product.price * cart_item.quantity)
                    quantity+=cart_item.quantity
                tax = total * 0.02
                grand_total = total+tax
                
                context = {
                    'order' : order,
                    'cart_items':cart_items,
                    'grand_total':grand_total,
                    'tax':tax,
                    'total_price':total
                }
                
                return render(request,'orders/payment.html',context)
            
            else:
                messages.error(request,form.errors)
                return redirect('checkout')
        except Exception as e:
            print(e)
            messages.error(request,'Some exception occured')
            return redirect('checkout')
    else:
        return redirect('home')
            
            
@login_required(login_url='login')    
def payments(request):
    
    if request.method == 'POST':
    
        body = json.loads(request.body)
        # print(body)
        # {'orderID': '20250627109', 'transID': '4U46067363729015F', 'payment_method': 'PayPal', 'status': 'COMPLETED'}
        
        order = Order.objects.get(user=request.user,is_ordered=False, order_number = body['orderID'])
        
        # store transaction details inside Payment model
        payment = Payment(
            user = request.user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total ,
            status = body['status']
        )
        
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # Move the cart items to Oder Product table
        cart_items = CartItem.objects.filter(user=request.user)
        
        for cart_item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.user = order.user 
            order_product.product_id = cart_item.product_id
            order_product.quantity = cart_item.quantity
            
            order_product.product_price = cart_item.product.price
            
            order_product.ordered = True
            
            # As variation is a many to any field , we will assign the value after saving the object
            
            order_product.save()
            
            cart_item = CartItem.objects.get(id=cart_item.id)
            product_variation = cart_item.variation.all()
            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variation.set(product_variation)
            order_product.save()
            
        
            # Reduce the quantity of the sold products
            product = Product.objects.get(id=cart_item.product.id)
            product.stock-=cart_item.quantity
            product.save()
        
        # Clear cart
        
        CartItem.objects.filter(user=request.user).delete()
        
        # Send order recieved email to customer
        
        mail_subject = "Thank you for ordering"
        message = render_to_string('orders/order_recieved_email.html',{
            'user':request.user,
            'order':order
        })
        
        to_email = request.user.email
        send_email = EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()
        
        # Send order number and transaction id back to sendData() via JsonResponse
        data = {
            'order_number':order.order_number,
            'transID': payment.payment_id,
            
            # 'order':order,
            # 'orderProducts':OrderProduct.objects.filter(order=order,payment=payment)
        }
        # it will go to the place where it has come
        return JsonResponse(data)
    
    else:
        return redirect('payments')
    
    
def order_complete(request):
    
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number,is_ordered = True)
        
        order_products = OrderProduct.objects.filter(order_id=order.id)
        # if order products does't work then use :
        # order_id=order.order_id
        
        return render(request,'orders/order_complete.html',{'order':order,'order_products':order_products})
        
    except Exception as e:
        print(e)
        return HttpResponse("<h1>Exception Occured</h1>")
    
    
    
        
    
    
        