from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import CartItem
from .models import Order
from .forms import OrderForm
import datetime
from django.contrib import messages


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
        total = (cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity
    tax = total * 0.02
    grand_total = total+tax
        
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            print('form:',form)
            if form.is_valid():
                # store all the billing information inside Order table
                data = Order() 
                print('data:',data)
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
                messages.success(request,'Order Placed Successfully')
                return redirect('dashboard')
            
            else:
                messages.error(request,form.errors)
                return redirect('checkout')
        except Exception as e:
            print(e)
            messages.error(request,'Some exception occured')
            return redirect('checkout')
    else:
        return redirect('home')
            