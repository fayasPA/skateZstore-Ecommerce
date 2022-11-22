from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class myUser(AbstractUser):                                             #Editing auth_user which is built-in django user
    phone_number = models.CharField(max_length=20, unique=True)         #Adding column phone no.

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name= models.CharField(max_length=100)
    category_image= models.ImageField(upload_to='category')

# class SubCategory(models.Model):
#     subcateg_name = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_qty = models.IntegerField(null=False,blank=False)
    product_price = models.FloatField(default=0.0)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='products/',null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products/',null=True,blank=True)

class Coupon(models.Model):
    code = models.CharField(max_length=100,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    min_amnt = models.FloatField(default=0.0)
    discount_amnt = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
