from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    def __str__(self):
        return self.name
    

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(Sub_Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/images', blank=True, null=True)
    date_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_at',)

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return self.price 
    
    
class Order(models.Model):   
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    distric = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    total_cost = models.IntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_date',)
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    total_price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    

    # def get_display_price(self):
    #     return self.price 
    