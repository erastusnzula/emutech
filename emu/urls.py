from django.urls import path
from . import views

app_name = 'emu'
urlpatterns = [
    path('', views.HomePage.as_view(), name='home-page'),
    path('item_list/', views.ItemList.as_view(), name='item-list'),
    path('<int:id>/', views.ItemView.as_view(), name='item-view'),
    path('add_to_cart/', views.AddItemToCart.as_view(), name='add-to-cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('cart_items/', views.CartItems.as_view(), name='cart-items'),
    path('add-coupon/', views.AddCoupon.as_view(), name='add-coupon'),
    path('paypal/', views.PaypalPayment.as_view(), name="paypal"),
    path('stripe/', views.StripePayment.as_view(), name='stripe'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('about/', views.About.as_view(), name='about'),
]
