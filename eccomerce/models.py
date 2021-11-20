from django.db import models
from django.contrib import auth

# Create your models here.\

class Sellers(models.Model):
    firstname =  models.CharField(max_length=255,null=True)
    lastname = models.CharField(max_length=45,null=True)
    emailaddress = models.CharField(max_length=45,null=True,unique=True)
    password = models.CharField(max_length=250,default="",null=True)
    stateofresidence = models.CharField(max_length=250,default="",null=True)

class Buyers(models.Model):
    firstname =  models.CharField(max_length=255,null=True)
    lastname = models.CharField(max_length=45,null=True)
    emailaddress = models.CharField(max_length=45,null=True,unique=True)
    password = models.CharField(max_length=250,default="",null=True)
    location = models.CharField(max_length=250,default="",null=True)


class Products(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.CharField(max_length=500)
    price = models.DecimalField(
        default=0, max_digits=16, decimal_places=2)
    sellersID = models.ForeignKey(Sellers,on_delete=models.CASCADE,null=True)
    salestatus = models.BooleanField(default=False)

class Orders(models.Model):
    productsID = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    sellersID = models.ForeignKey(Sellers,on_delete=models.CASCADE,null=True)
    buyersID = models.ForeignKey(Buyers,on_delete=models.CASCADE,null=True)
    orderstatus = models.CharField(max_length=30, null = True)

class BuyersInterest(models.Model):
    buyersID = models.ForeignKey(Buyers,on_delete=models.CASCADE,null=True)
    productsID =  models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(
        'created_at', auto_now_add=True, null=True)


