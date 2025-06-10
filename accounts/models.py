from django.db import models

# We want to use email instead of username in login field and want to define new fields also.

# 1

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# we will inherit AbstractBaseUser to create a cutom user model
# we will inherit BaseUserManager to generate a custom manager for user. 


# Custom User Manager
class UserManager(BaseUserManager):
    
    def create_user(self,first_name,last_name,email,username,password=None,password2=None):
    
        '''
        Creates and saves a User with the given email, name, tc and password.
        '''
        if not email:
            raise ValueError('User must have an email address')
        if not username :
            raise ValueError('User must have an Username')
        
        user = self.model(
            email = self.normalize_email(email),
            # Normalize the email address by lowercasing the domain part of it.
            
            first_name=first_name,
            last_name=last_name,
            username = username
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name, username, email,password=None):
        
        user = self.create_user(
            email=self.normalize_email(email) ,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            
        )
        
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True )
    
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    username = models.CharField(max_length=250,unique=True)
    phone_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # date_joined is same as created_at
    
    # objects = UserManagher()
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    # will use email instead of username
    
    REQUIRED_FIELDS = ['first_name','last_name','username']
    # will not add email because when we made or marked email as username field it automatically added to required field we don't need to explicitly add it.
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None) :
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label' ? "
        
        return True
        
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
    
    
# settings.py
    # AUTH_USER_MODEL = 'account.User'
    # NOTE : Don't run migration commands before writting this , it will cause error later.