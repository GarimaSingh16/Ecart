from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60,unique=True)
    # slug is nothing but the url for the category
    
    description = models.TextField(max_length=100,blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    # blank=True means can be leaved as blank
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    # get_url function is used to return the url containing the slug , so that when we click on any category then the url gets generated for that category. 
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
        # it will return an url containing slug in it .
    
    def __str__(self):
        return self.category_name
    