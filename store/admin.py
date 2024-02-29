from django.contrib import admin
from .models import Category, Product,Customer,Order,Profile,OrderItem
# Register your models here.

admin.site.register([Order, Customer, Product, Category,Profile,OrderItem])