import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_updated = models.DateField(User, auto_now=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255,unique=True,null=True)
    password = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1,related_name='products')
    description = models.TextField(default='',blank=True,null=True)
    image = models.ImageField(upload_to='images/product/')

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)


    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    @property
    def get_total_price(self):
        return self.quantity * self.price