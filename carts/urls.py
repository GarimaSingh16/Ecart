from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart,name='add_cart'),
    path('subt_cart/<int:product_id>/<cart_item_id>/', views.subt_cart,name='subt_cart'),
    path('remove_cart/<int:product_id>/<int:cart_items_id>/', views.remove_cart,name='remove_cart'),
    
]
