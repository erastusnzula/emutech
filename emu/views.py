import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from .forms import CheckoutForm, CouponForm
from .models import Item, CartItem, Order, ShippingAddress
from .utils import get_coupon, complete_order, update_guest_cart
from .templatetags.cart import update_cart_items


class HomePage(View):
    def get(self, *args, **kwargs):
        update_guest_cart(self.request)
        context = {}
        return render(self.request, 'emu/home_page.html', context)


class ItemList(View):
    def get(self, *args, **kwargs):
        items = Item.objects.all()
        update_guest_cart(self.request)
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
                    messages.info(self.request, f"Successfully increased quantity to - {order_item.quantity}")
                    print("Added")
                elif action == 'remove':
                    order_item.quantity -= 1
                    messages.info(self.request, f"Successfully reduced quantity to - {order_item.quantity}")
                    print("Reduced")
                order_item.save()
                if order_item.quantity <= 0:
                    order_item.delete()
                    messages.info(self.request, "Successfully deleted")

                return JsonResponse("Added successfully", safe=False)
            else:
                order.items.add(order_item)
                messages.info(self.request, "Successfully added")
                return JsonResponse("Added successfully", safe=False)
        else:
            order_date = timezone.now()
            order = Order.objects.create(user=self.request.user)
            order.items.add(order_item)
            messages.info(self.request, f"Successfully added")
            return JsonResponse("Added successfully", safe=False)
            # return redirect('emu:cart-items')


class CartItems(View):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, is_complete=False)
                
            else:
                order = {}
                update_guest_cart(self.request)
                    

            context = {'order': order}
            
            return render(self.request, 'emu/cart_items.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('/')


class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, is_complete=False)
                context = {'form': form, 'order': order, 'couponform': CouponForm(), 'DISPLAY_COUPON_FORM': True}
                shipping_address_qs = ShippingAddress.objects.filter(
                    user=self.request.user,
                    default=True
                )
                if shipping_address_qs.exists():
                    context.update({'default_address': shipping_address_qs[0]})

                return render(self.request, 'emu/checkout.html', context)
            else:
                order = {}
                try:
                    cart = json.loads(self.request.COOKIES['cart'])
                except:
                    cart = {}
                update_cart_items.items = len(cart)
                context = {'form': form, 'order': order, 'couponform': CouponForm(), 'DISPLAY_COUPON_FORM': True}
                return render(self.request, 'emu/checkout.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order.')
            return redirect('emu:checkout')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        order = Order.objects.get(user=self.request.user, is_complete=False)
        use_default = data['shippingInfo']['useDefault']
        if use_default == True:
            address_qs = ShippingAddress.objects.filter(
                user=self.request.user,
                default=True)
            if address_qs.exists():
                shipping_address_1 = address_qs[0]
                order.shipping_address = shipping_address_1
                order.save()
            else:
                messages.info(self.request, 'No default shipping address available.')
                return redirect('emu:checkout')
        else:
            town = data['shippingInfo']['town']
            city = data['shippingInfo']['city']
            country = data['shippingInfo']['country']
            zip_code = data['shippingInfo']['zipCode']
            shipping_address = ShippingAddress()
            shipping_address.user = self.request.user
            shipping_address.town = town,
            shipping_address.city = city,
            shipping_address.zipe_code = zip_code,
            shipping_address.country = country,
            set_default = data['shippingInfo']['save']
            if set_default == True:
                shipping_address.default = True
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
            else:
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
        complete_order(self.request)
        return JsonResponse("Data received", safe=False)


class AddCoupon(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, is_complete=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                print(order.get_total())
                messages.info(self.request, 'Successfully added coupon')
                return redirect('emu:checkout')
            except:
                print("error")
                return redirect('emu:checkout')
