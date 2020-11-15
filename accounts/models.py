from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=25,null=True)
    email=models.CharField(max_length=25,null=True)
    phone=models.CharField(max_length=12,null=True)
    profile_pic=models.ImageField(default="dpdefault.png",null=True,blank=True)
    
    date=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
       return self.name

class Tags(models.Model):
    name=models.CharField(max_length=25,null=True)
    
    def __str__(self):
       return self.name
class Products(models.Model):
    CATEGORY=(
        ('INDOOR','INDOOR'),
        ('OUTDOOR','OUTDOOR')
    )
    name=models.CharField(max_length=25,null=True)
    price=models.FloatField()
    category=models.CharField(max_length=100,null=True,choices=CATEGORY)
    description=models.CharField(max_length=250,null=True)
    date=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tags)
    def __str__(self):
       return self.name




class Order(models.Model):
    STATUS=(
        ('pending','pending'),
        ('Out for delievery','Out for delievery'),
        ('Delievered','Delievered')
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Products,null=True,on_delete=models.SET_NULL)
    date=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=100,null=True,choices=STATUS)
    note=models.CharField(max_length=1000,null=True)
    def __str__(self):
       return self.product.name
    
