import random
import string

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from .models import Order, Coupon


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exist.')
        return redirect('src:checkout')


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))


def complete_order(request):
    order = Order.objects.get(user=request.user, is_complete=False)
    order_items = order.items.all()
    order_items.update(is_complete=True)
    for item in order_items:
        item.save()
    order.is_complete = True
    order.transaction_id = create_ref_code()
    order.save()
    messages.success(request,
                     f"Order: ({create_ref_code()} ) successfully submitted. Thank you for shopping with us.")
