from django.contrib import admin
from .models import Dish, Category, Order, OrderItem, Review

admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)


# Register your models here.
