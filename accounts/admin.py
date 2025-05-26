from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ['email','first_name','last_name','username']
    
    list_display_links = ['email','first_name','username']
    
    readonly_fields=['last_login']
    # will not be able to edit it (not by the normal user nor by the superuser or admin)
    
    ordering = ['-created_at']
    
    list_filter = ()
    # list filter is used to define the filters through which we can filter data in our admin pannel and see the data after applying the filter
    
    filter_horizontal = ()
    fieldsets = ()
    # Here fieldsets will have a field name(category name) and inside and that different model fields will be there. It also helps in hiding the passwords and other confidencial details.
    # Syntax : 
        # fieldsets = (
            # ('field_name', {
            #     "fields": ['list of fields will be here'], or any iterable sequence in place of list
            # }),
        # )
        # Here 'fields': will not change or we can not use any other name , here 'fields' is a key in which different fields will be given as values.
        


admin.site.register(User,UserAdmin)