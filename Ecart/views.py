from django.shortcuts import render
from store.models import Product

products = Product.objects.all().filter(is_available = True)[0:12]

def home(request):
    return render(request,'home.html',{'products':products})