from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import STKPush, CallBack, TransactionSuccess, FailedTransaction

app_name = 'mpesa'
urlpatterns = [
    path('stk_push/', csrf_exempt(STKPush.as_view()), name='stk-push'),
    path('call_back/', csrf_exempt(CallBack.as_view()), name='call-back'),
    path('success/', TransactionSuccess.as_view(), name='sucess'),
    path('failed/', FailedTransaction.as_view(), name='failed'),
]
