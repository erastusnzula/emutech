from django.contrib import admin
from .models import Item, Category, Order, CartItem, ShippingAddress, Coupon

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Coupon)
