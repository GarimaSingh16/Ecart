from carts.views import _cart_id
from carts.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

def total_items(request):
    
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            
            # It will show the total_number of items present in cart irrespective of their quantity
            
            if request.user.is_authenticated:
                total_items = CartItem.objects.filter(user=request.user,is_active=True)
            
            else:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                
                total_items = CartItem.objects.filter(cart=cart,is_active = True)
            
            # OR
            
            # It will show the quantity of items present in cart and the above one shows the total_number of items present in cart irrespective of their quantity
            
            # cart = Cart.objects.get(cart_id = _cart_id(request))
            # cart_items = CartItem.objects.filter(cart=cart,is_active = True)
            
            # total_items = 0
            
            # for item in cart_items:
            #     total_items += item.quantity
            
            # Just write total_items in place of total_items.count in base.html
                
            
        except Cart.DoesNotExist:
            total_items = 0
    return dict(total_items = total_items)
         
