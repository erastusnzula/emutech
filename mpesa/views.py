import json

from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib import messages

from emu.models import Order
from .models import STKPushTransaction
from .utils import initiate_stk_push, get_conversion_rate
from emu.utils import update_guest_cart


class STKPush(View):
    def get(self, request, *args, **kwargs):
        no_order=False
        if self.request.user.is_authenticated:
            try:
                no_order=False
                order = Order.objects.get(user=self.request.user, is_complete=False)
                order_total = int(order.get_total())
                order_total = str(get_conversion_rate(order_total))
            except ObjectDoesNotExist:
                no_order = True
                messages.info(self.request, "You do not have an active order to pay")
              
        else:
            order = {'get_total': 0}
            guest = update_guest_cart(self.request)  
            total = guest['order']['get_total']
            order['get_total']= total
            order_total = get_conversion_rate(total)
        context = {'order_total': order_total, 'no_order': no_order}
        
        return render(self.request, 'mpesa/stk_push.html', context)

    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        mobile_number = data['mobile_number']
        if self.request.user.is_authenticated:
            order = Order.objects.get(user=self.request.user, is_complete=False)
            order_total = int(order.get_total())
            amount = get_conversion_rate(order_total)
        else:
            order = {'get_total': 0}
            guest = update_guest_cart(self.request)  
            total = guest['order']['get_total']
            order['get_total']= total
            amount = get_conversion_rate(total)

        response = initiate_stk_push(mobile_number=int(mobile_number), amount=int(amount))
        return JsonResponse(response)


class CallBack(View):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        stk_push_transaction = STKPushTransaction()
        stk_push_transaction.merchant_id = data['Body']['stkCallback']['MerchantRequestID'],
        stk_push_transaction.checkout_id = data['Body']['stkCallback']['CheckoutRequestID'],
        stk_push_transaction.transaction_date = data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
        stk_push_transaction.reference = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
        stk_push_transaction.result_code = data['Body']['stkCallback']['ResultCode'],
        stk_push_transaction.result_description = data['Body']['stkCallback']['ResultDesc'],
        stk_push_transaction.mobile_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        stk_push_transaction.amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
        stk_push_transaction.balance = data['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value'],
        stk_push_transaction.save()
        print(data)
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
