from django.shortcuts import render, redirect
from django.views import View
from .models import Item, CartItem, Order, ShippingAddress,Category, Coupon
from django.http import JsonResponse
import json
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import CheckoutForm, CouponForm


class HomePage(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, 'emu/home_page.html', context)
    
class ItemList(View):
    def get(self, *args, **kwargs):
        items = Item.objects.all()
        context = {'items': items}
        return render(self.request, 'emu/item_list.html', context)
 
class ItemView(View):
    def get(self, request, id):
        item = Item.objects.get(id=id)
        context = {
            'item': item
        }
        return render(self.request, 'emu/item_view.html', context)
    
    
class AddItemToCart(View):
    def get(self, *args, **kwargs):
        return redirect('emu:cart-items')
    
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        print(data)
        item_id = data['item_id']
        action = data['action']
        
        item = Item.objects.get(id=item_id)
        order_item, created = CartItem.objects.get_or_create(item=item, user=self.request.user, is_complete=False)
        qs = Order.objects.filter(user=self.request.user, is_complete=False)
        if qs.exists():
            order = qs[0]
            if order.items.filter(item__id=item.id).exists():
                if action == 'add':
                    order_item.quantity += 1
                    print("Added")
                elif action == 'remove':
                    order_item.quantity -= 1
                    print("Reduced")
                order_item.save()
                if order_item.quantity <= 0:
                    order_item.delete()
                    
                return JsonResponse("Added successfully", safe=False)
            else:
                order.items.add(order_item)
                return JsonResponse("Added successfully", safe=False)
        else:
            order_date = timezone.now()
            order = Order.objects.create(user=self.request.user)
            order.items.add(order_item)
            return JsonResponse("Added successfully", safe=False)
            #return redirect('emu:cart-items')
    
    

class CartItems(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_complete=False)
            context = {'order': order}
            return render(self.request, 'emu/cart_items.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('/')
        

class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_complete=False)
            print(order.for_shipping)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'couponform': CouponForm(),
                'DISPLAY_COUPON_FORM': True
            }
            shipping_address_qs = ShippingAddress.objects.filter(
                user=self.request.user,
                default = True
            )
            if shipping_address_qs.exists():
                context.update({'default_address': shipping_address_qs[0]})

            return render(self.request, 'emu/checkout.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order.')
            return redirect('emu:checkout')