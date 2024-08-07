import json
import random

from django import forms as f
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from .forms import CheckoutForm, CouponForm, SignUpForm, SignInForm, ContactForm
from .models import Item, CartItem, Order, ShippingAddress, GuestCustomer
from .utils import get_coupon, complete_order, update_guest_cart, get_next

guest_order_slug = []
guest_order_customers = []


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
        update_guest_cart(request)
        context = {'item': item}
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
            is_guest = False
            if self.request.user.is_authenticated:
                order = Order.objects.get(user=self.request.user, is_complete=False)

            else:
                is_guest = True
                guest = update_guest_cart(self.request)
                cart_items = guest['order']['get_cart_items']
                order_total = guest['order']['get_total']
                items = guest['order']['items']
                for_shipping = guest['order']['for_shipping']
                order = {"get_cart_items": cart_items, 'get_total': order_total, 'items': items,
                         'for_shipping': for_shipping}

            context = {'order': order, 'is_guest': is_guest}

            return render(self.request, 'emu/cart_items.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('/')


class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            is_guest = False
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
                is_guest = True
                guest = update_guest_cart(self.request)
                cart_items = guest['order']['get_cart_items']
                order_total = guest['order']['get_total']
                items = guest['order']['items']
                for_shipping = guest['order']['for_shipping']
                order = {"get_cart_items": cart_items, 'get_total': order_total, 'items': items,
                         'for_shipping': for_shipping}
                context = {'form': form, 'order': order, 'couponform': CouponForm(), 'DISPLAY_COUPON_FORM': True,
                           'is_guest': is_guest}
                return render(self.request, 'emu/checkout.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order.')
            return redirect('emu:checkout')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        if self.request.user.is_authenticated:

            order = Order.objects.get(user=self.request.user, is_complete=False)
            use_default = data['shippingInfo']['useDefault']
            if use_default:
                address_qs = ShippingAddress.objects.filter(
                    user=self.request.user,
                    default=True)
                if address_qs.exists():
                    shipping_address_1 = address_qs[0]
                    order.shipping_address = shipping_address_1
                    order.save()
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
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                if set_default == True:
                    shipping_address.default = True
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()

            # complete_order(self.request, self.request.user)

        else:
            print(self.request.COOKIES)
            username = data['userInfo']['name']
            email = data['userInfo']['email']
            password = f"PASSWOrdG{random.randint(0, 1000)}"
            print(f"Not logged in {username} {email}")
            customer, created = GuestCustomer.objects.get_or_create(email=email)
            customer.username = username
            customer.password = password
            customer.save()
            user, created = User.objects.get_or_create(username=username, email=email)
            user.password = password
            user.save()

            guest_order_customers.append(username)
            guest_order_customers.append(email)

            guest = update_guest_cart(self.request)
            items = guest['order']['items']
            order = Order.objects.create(user=user)

            for i in items:
                item = Item.objects.get(id=i['item']['id'])
                order_item, created = CartItem.objects.get_or_create(item=item, user=user, is_complete=False)
                order.items.add(order_item)
            use_default = data['shippingInfo']['useDefault']
            if use_default:
                address_qs = ShippingAddress.objects.filter(
                    user=user,
                    default=True)
                if address_qs.exists():
                    shipping_address_1 = address_qs[0]
                    order.shipping_address = shipping_address_1
                    order.save()
            else:
                town = data['shippingInfo']['town']
                city = data['shippingInfo']['city']
                country = data['shippingInfo']['country']
                zip_code = data['shippingInfo']['zipCode']
                shipping_address = ShippingAddress()
                shipping_address.user = user
                shipping_address.town = town,
                shipping_address.city = city,
                shipping_address.zipe_code = zip_code,
                shipping_address.country = country,
                set_default = data['shippingInfo']['save']
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                if set_default:
                    shipping_address.default = True
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()
            customer.order_slug = order.order_slug
            guest_order_slug.append(order.order_slug)
            customer.save()
            print(f"Order slug: {order.order_slug}")
            # complete_order(self.request, user)
        return JsonResponse("Order completed successfully", safe=False)


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


class PaypalPayment(View):

    def get(self, *args, **kwargs):
        paypal_client_id = settings.PAYPAL_CLIENT_ID

        if self.request.user.is_authenticated:
            order = Order.objects.get(user=self.request.user, is_complete=False)

        else:
            order = {'get_total': 0}
            guest = update_guest_cart(self.request)
            total = guest['order']['get_total']
            order['get_total'] = total

        context = {'order': order, 'paypal_client_id': paypal_client_id}
        return render(self.request, 'emu/paypal_payment.html', context)

    def post(self, *args, **kwargs):
        print('Paid with paypal')
        if self.request.user.is_authenticated:
            user = self.request.user
            complete_order(self.request, user)
        else:
            print("to be updated")
            quest_customer = GuestCustomer.objects.get(order_slug=guest_order_slug[-1],
                                                       username=guest_order_customers[0],
                                                       email=guest_order_customers[1])
            print(quest_customer)
            guest_username = quest_customer.username
            guest_email = quest_customer.email
            user = User.objects.get(username=guest_username, email=guest_email)
            complete_order(self.request, user)
            del guest_order_slug[:]
            del guest_order_customers[:]
            print(f"customer {guest_order_customers}")

        return JsonResponse("Success Paypal", safe=False)


class StripePayment(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'emu/stripe_payment.html')

class Contact(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(self.request, 'emu/contact.html', context)

    def post(self, *args, **kwargs):
        form = ContactForm(data=self.request.POST)
        error_user = ''
        if form.is_valid():
            user = form.cleaned_data.get('user')
            if self.request.user.is_authenticated:
                if user == self.request.user.username:
                    form.save()
                    return redirect('emu:contact')
                else:
                    try:
                        error_user = "Your name must match with your username"
                        raise f.ValidationError("user", "jjhj")
                        # raise ValidationError("jjhhjhj")
                    except ValidationError:
                        print(self.request.user)
                        context = {'form': form, "error_user": error_user}
                        return render(self.request, 'emu/contact.html', context)

            else:
                form.save()
                return redirect('emu:contact')
        else:
            context = {'form': form}
            return render(self.request, 'emu/contact.html', context)


class About(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'emu/about.html')
