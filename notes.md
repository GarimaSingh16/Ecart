## Custom User Model
- if you have created any custom user model then it is mandatory to specify the models and its location in the settings.py .
- #### AUTH_USER_MODEL = 'accounts.User'
- ### ` It is important to write this before making any migrations or it might create a problem `

## No Custom User Model
- if we want to change the defalut look or listing for the field in default user model then we can specify that in the admin.py in main project(may be) and for any model we can write it in the admin.py file where the models.py for that model is present.

``` 
class UserAdmin(UserAdmin):
    list_display = ('email','first_name',...)
    
admin.site.register(UserAdmin)
```
- #### name should be like : model_name + 'Admin'
    
