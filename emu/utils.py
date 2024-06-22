from django.shortcuts import render, redirect
from django.views import View
from .models import Item, CartItem, Order, ShippingAddress,Category, Coupon
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import CheckoutForm, CouponForm

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exist.')
        return redirect('src:checkout')