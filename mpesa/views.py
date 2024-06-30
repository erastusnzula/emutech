import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from emu.models import Order
from .models import STKPushTransaction
from .utils import initiate_stk_push, get_conversion_rate


class STKPush(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            order = Order.objects.get(user=self.request.user, is_complete=False)
            order_total = int(order.get_total())
            order_total = str(get_conversion_rate(order_total))
            return render(self.request, 'mpesa/stk_push.html', {'order_total': order_total})

    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        mobile_number = data['mobile_number']
        if self.request.user.is_authenticated:
            order = Order.objects.get(user=self.request.user, is_complete=False)
            order_total = int(order.get_total())
            amount = get_conversion_rate(order_total)
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
