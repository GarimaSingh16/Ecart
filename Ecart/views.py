from django.shortcuts import render
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available = True)[0:12]

    return render(request,'home.html',{'products':products})