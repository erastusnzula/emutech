from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
    )

from . import views

app_name = 'users'
urlpatterns = [
    path('sign up/', views.Register.as_view(), name='register'),
    path('sign in/', views.Login.as_view(), name='login'),
    path('sign out/', views.LogoutUser.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html', success_url='/users/password_reset_done/',email_template_name='users/password_reset_email.html', subject_template_name='users/password_reset_subject.txt'), name='password-reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url = '/password_reset_complete/'), name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('change_password/', views.ChangePassword.as_view(), name='change-password'),
    path('change_password_done/', views.ChangePasswordDone.as_view(), name='change-password-done'),
]
