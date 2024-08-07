from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('sign up/', views.Register.as_view(), name='register'),
    path('sign in/', views.Login.as_view(), name='login'),
    path('sign out/', views.LogoutUser.as_view(), name='logout'),
]
