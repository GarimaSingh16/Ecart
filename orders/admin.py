from django.contrib import admin
from .models import Payment,OrderProduct,Order


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    # by default django provide some extra 3 fields with blank data and if we delete it manually after refreshing we will get them again . so, this will stop generating extra fields
    
    readonly_fields = ['payment','user','product','quantity','product_price','ordered']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','user','full_name','phone','email','city','order_total','status','is_ordered','created_at','updated_at']
    
    list_filter = ['status','is_ordered','updated_at']
    
    search_fields = ['order_number','first_name','last_name','phone','email','user']
    
    inlines=[OrderProductInline]
    # this will add/append orderproduct model in order model

# Register your models here.
admin.site.register([Payment,OrderProduct])
admin.site.register(Order,OrderAdmin)