from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('edit/', views.Edit.as_view(), name='edit'),
    # Change password
    path(
        'change-password/',
        views.ChangePassword.as_view(),
        name='change_password'
    ),
    # Reset password
    path(
        'reset-password/',
        views.ResetPassword.as_view(),
        name='reset_password'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.ResetPasswordConfirm.as_view(),
        name='reset_password_confirm'
    ),
    # OTP
    path('otp/auth/', views.OtpAuth.as_view(), name='otp_auth'),
    path('otp/login/', views.OtpLogin.as_view(), name='otp_login'),
]
