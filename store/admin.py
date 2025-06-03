from django.contrib import admin
from .models import Product,Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price','stock','category','modified_date','is_available']
    prepopulated_fields = {'slug':['product_name']}
    
admin.site.register(Product,ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product','variation_category','variation_value','is_active','created_date']
    # c:\Users\garim\AppData\Local\Packages\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\TempState\ScreenClip\{7A508B00-2966-4EFD-AE70-98EE2D30B86D}.png
    
    list_editable = ['is_active']
    # we can edit this value without entering into full details , just ve seeing outside
    # c:\Users\garim\AppData\Local\Packages\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\TempState\ScreenClip\{12ED2705-4CAB-4C33-B5A9-1E1EE1F6C738}.png
    
    list_filter  = ['product','variation_category','variation_value']
    # c:\Users\garim\AppData\Local\Packages\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\TempState\ScreenClip\{781D4437-24CB-473C-8509-10725D59DF3E}.png
    


    

admin.site.register(Variation,VariationAdmin)