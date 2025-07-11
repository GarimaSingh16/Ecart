from tkinter import CASCADE
from django.db import models
from accounts.models import User
from store.models import Product,Variation

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    # This is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
    
    
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    )
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=70)
    address_line_2 = models.CharField(max_length=70,blank=True)
    country = models.CharField(max_length=50) 
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    order_note = models.CharField(max_length=150,blank = True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10,choices = STATUS , default='New')
    ip = models.CharField(blank=True , max_length=20)
    is_ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name}  {self.last_name}'
    
    def sub_total(self):
        return self.order_total - self.tax
    
    def trans_id(self):
        return str(self.payment)[-4:-1:-1]
    
    def __str__(self):
        return self.first_name
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    variation = models.ManyToManyField(Variation,blank=True)
    # we can't use on_delete here
    
    quantity = models.PositiveIntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
    
    
    