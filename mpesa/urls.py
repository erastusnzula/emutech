from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import STKPush, CallBack

app_name = 'mpesa'
urlpatterns = [
    path('stk_push/', csrf_exempt(STKPush.as_view()), name='stk-push'),
    path('call_back/', csrf_exempt(CallBack.as_view()), name='call-back'),
]
