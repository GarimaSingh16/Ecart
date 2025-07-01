from django.http import HttpResponse
from django.shortcuts import redirect, render
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

# this is a private function as there is underscore(_) before the function name. Remember wherever we want to access this function we need to use the underscore before is as it is written while making it private.

def _cart_id(request):
    
    # getting session key which is present inside the cookies if we look in inspect.
    cart = request.session.session_key
    
    if not cart:
        # if cart don't have any value or have None vale which means session key doesn't exist then we will create one in that case.
        
        cart = request.session.create()
        
    return cart



def cart(request,total_amount=0,cart_items=None,tax=0):
    grand_total=0
    try :    
        
        if request.user.is_authenticated :
            is_cart_item_exists = CartItem.objects.filter(user=request.user).exists()
            if is_cart_item_exists:
                cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            else:
                cart_items = CartItem.objects.filter(cart=cart,is_active = True)
                
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        # print(cart)
            
            cart_items = CartItem.objects.filter(cart=cart,is_active = True)
            print(cart_items)
        # total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.product.price * cart_item.quantity 
        tax = total_amount * 0.02
        grand_total = total_amount+tax
    except ObjectDoesNotExist:
        pass    
    except Exception as e:
        print(e)
    
    context={
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'total_price':total_amount
        }
    return render(request,'store/cart.html',context)
        


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    
    current_user=request.user
    
    # with the help of this we will store its values in CartItem model in models.py of Cart
    product_variation = []
    
    # for get request and to check if everything is working fine or not
    
    # color = request.GET.get('color')
    # size = request.GET.get('size')
    
    # return HttpResponse([color,'<br/>',size])
    
    if request.method == 'POST':
        # color = request.POST.get('color')
        # size = request.POST.get('size')
        # return HttpResponse([color,'<br/>',size])
            
    
        for item in request.POST:
            key=item
            value=request.POST.get(key)
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact = key , variation_value__iexact = value)
                # print(variation.variation_category,variation.variation_value)
                
                # print(variation)
                product_variation.append(variation)
                
                
            except Exception as e:
                # print(e)
                pass
    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id present in the session by using _cart_id() method which is a private method.
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    print(cart) 
    
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product = product,cart=cart).exists()
    
    if product.stock > 0 or is_cart_item_exists:
        
       
            # if any product present in the cart then it will increase the quantity by 1.
            
                if current_user.is_authenticated:
                    cart_items = CartItem.objects.filter(product=product,user=current_user)
                else:
                    cart_items = CartItem.objects.filter(product = product,cart=cart)
                
                # existing variations -> will come from database
                # current variation -> product_variation list
                # item_id -> will come from database
                
                ex_var_list = []
                id=[]
                
                for cart_item in cart_items:
                    ex_vari_queryset = cart_item.variation.all()
                    # without list -> product_variation in ex_var_list will return false
                    ex_var_list.append(list(ex_vari_queryset))
                    # print(ex_var_list)
                    id.append(cart_item.id)
                
                if  product_variation in ex_var_list:
                    index = ex_var_list.index(product_variation)
                    print(index)
                    item_id = id[index]
                    print(id)
                    item = CartItem.objects.get(product=product,id=item_id)
                    item.quantity += 1
                    item.save()
                    # save item or add item to database
                    
                else:
                    
                    if current_user.is_authenticated:
                        cart_item = CartItem.objects.create(
                        product = product,
                        quantity = 1,
                        cart=cart,
                        user=current_user
                        )
                        
                    else:
                        cart_item = CartItem.objects.create(
                        product = product,
                        quantity = 1,
                        cart=cart,

                        )
                    if len(product_variation ) > 0:
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                        # *product_variation will split the items and then work upon it.
                    cart_item.save()
                        
                return redirect('cart')    
                
    else:
        return redirect('product_detail',product.category.slug,product.slug)

def subt_cart(request,product_id,cart_item_id):
    product = Product.objects.get(id=product_id)
    
    try:
        if request.user.is_authenticated:
            is_cart_item_exists = CartItem.objects.filter(product = product,user=request.user,id=cart_item_id).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product = product,user=request.user,id=cart_item_id )
                
        else:
            try :
                cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id present in the session by using _cart_id() method which is a private method. 
                
            except Cart.DoesNotExist:
                cart = Cart.objects.delete(
                    cart_id = _cart_id(request)
                )
            cart.save()
    # if any product present in the cart then it will decrease the quantity by 1.
            cart_item = CartItem.objects.get(product = product,cart=cart,id=cart_item_id )
        cart_item.quantity -=1
        cart_item.save()
        # save item or add item to database
        
    except ObjectDoesNotExist:
        pass
    return redirect('cart') 

def remove_cart(request,product_id,cart_items_id):
    product = Product.objects.get(id=product_id)
    
    try:
        if request.user.is_authenticated:
            is_cart_item_exists = CartItem.objects.filter(product = product,user=request.user,id=cart_items_id).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product = product,user=request.user,id=cart_items_id)
   
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id present in the session by using _cart_id() method which is a private method. 
            
            cart_item = CartItem.objects.get(product = product,cart=cart,id=cart_items_id)
        cart_item.delete()

        # save item or add item to database
        return redirect('cart')
    except ObjectDoesNotExist:
        pass

@login_required(login_url='login')    
def checkout(request,total_amount=0,cart_items=None,tax=0):
    grand_total = 0
    try :
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        # print(cart)
        cart_items = CartItem.objects.filter(user=request.user,is_active = True)
        # total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.product.price * cart_item.quantity 
        tax = total_amount * 0.02
        grand_total = total_amount+tax
        
    except ObjectDoesNotExist:
        pass
    except Exception as e:
        print(e)
    
    context={
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'total_price':total_amount
    }
    return render(request,'store/checkout.html',context)