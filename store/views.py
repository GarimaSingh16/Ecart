from unicodedata import category
from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404
from carts.models import CartItem
from .models import Product
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q


# Create your views here.
def store(request,category_slug=None):
    
    
    categories=None
    products = None
    
    if category_slug:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category = categories)
        
        # +++++++++++++++++++++++++++++++++++++++ Pagination  +++++++++++++++++++++++++++++++++++++++
        
        paginator=Paginator(products,6)
        # Here we have created a paginator in which we have just defined how much number of products we in need per page
        
        page=request.GET.get('page')
        # In the get request or url the page number is specified as ?page=1 , here we are storing that into the page
        
        paged_products = paginator.get_page(page)
        # Here we will get 6 products because we have defined per_page=6 in paginator ehich means 6 items per page will be there .
        
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        # Here we are getting all the poducts.
        
        # +++++++++++++++++++++++++++++++++++++++ Pagination  +++++++++++++++++++++++++++++++++++++++
        
        paginator=Paginator(products,6)
        # Here we have created a paginator in which we have just defined how much number of products we in need per page
        
        page=request.GET.get('page')
        # In the get request or url the page number is specified as ?page=1 , here we are storing that into the page
        
        paged_products = paginator.get_page(page)
        # Here we will get 6 products because we have defined per_page=6 in paginator ehich means 6 items per page will be there .
        
        product_count = products.count()
        
    
    # +++++++++++++++++  before pagination  +++++++++++++++++
    # return render(request,'store/store.html',context={'products':products})
    
    # +++++++++++++++++++++  after pagination  ++++++++++++++++
    return render(request,'store/store.html',{'products':paged_products,'product_count':product_count})

def product_detail(request,category_slug=None,product_slug=None):
    
    
    # category=None
    # product = None
    
    # if category_slug and product_slug:
    #     category = get_object_or_404(Category,slug=category_slug)
    #     product = get_object_or_404(Product,category = category,slug=product_slug)
    
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = product).exists()
        # cart__cart_id , here cart is present in CartItem model but we want to access cart_id of cart which means we want to access a property of a foreign_key that is why we have used gouble underscore('__') before the property of foreign key.
        
        # will used to check if product is already present in cart or not.
        
    except Exception as e :
        raise e
        
    return render(request,'store/product-detail.html',{'product':product,'in_cart':in_cart})


def search(request):
    if request.method == 'GET':
        
        # ?keyword=shirt  we will not get this if method='POST'
        
        # return JsonResponse({'data':request.POST.get('keyword')})
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword) )
            paginator=Paginator(products,6)
            # Here we have created a paginator in which we have just defined how much number of products we in need per page
        
            page=request.GET.get('page')
            # In the get request or url the page number is specified as ?page=1 , here we are storing that into the page
            
            paged_products = paginator.get_page(page)
            # Here we will get 6 products because we have defined per_page=6 in paginator ehich means 6 items per page will be there .
            
            product_count = products.count()
            
        return render(request,'store/store.html',{'products':paged_products,'product_count':product_count})