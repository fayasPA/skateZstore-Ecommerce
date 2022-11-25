from django.db import models
from admn.models import *
from django.utils import timezone
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)                                      #Adding column phone no.
    address = models.CharField(max_length=100)
    pin = models.IntegerField()
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    landmark = models.CharField(max_length=20,null=True)

class Cart(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    coupon_code = models.CharField(max_length=100,blank=True)
    discounted_amnt = models.FloatField(default=0.0)
    def get_total_item_price(self):

        if self.product.product_offer_price < 1 and self.product.category_offer_price < 1:
            return self.quantity * self.product.product_price
        elif self.product.product_offer_price > 1 and self.product.category_offer_price is 0:
            return self.quantity * self.product.product_offer_price
        elif self.product.product_offer_price < 1 and self.product.category_offer_price > 1:
            return self.quantity * self.product.category_offer_price
        elif self.product.product_offer_price < self.product.category_offer_price and self.product.category_offer_price > 1:
            return self.quantity * self.product.category_offer_price
        elif self.product.category_offer_price < self.product.product_offer_price and self.product.product_offer_price > 1:
            return self.quantity * self.product.product_offer_price
        elif self.product.product_offer_price == self.product.category_offer_price and self.product.product_offer_price > 1 and self.product.category_offer_price > 1:
            return self.quantity * self.product.category_offer_price
        

        # return self.quantity * self.product.product_price

    def get_final_price(self):
        return self.get_total_item_price()

choices = (('Order Placed', 'Order Placed'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'), 
        ('Delivered','Delivered'),
        ('Cancel', 'Cancel'), 
        )

class HistoryOrder(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100,default='COD')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.FloatField(default=0)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING,default='')
    status = models.CharField(max_length=100, choices = choices, default="Order Placed",blank=True,null=True)
    updated_date =models.DateTimeField(auto_now=True)
    coupon_code = models.CharField(max_length=100,blank=True)

    def get_order_id(self):                                                             #   strftime converts date to string
        order_id_no = self.ordered_date.strftime('PAYTOME%Y%m%dODR') + str(self.id)
        return order_id_no

    def get_total_item_price(self):
        return self.quantity * self.product.product_price

    def get_final_price(self):
        return self.get_total_item_price()

