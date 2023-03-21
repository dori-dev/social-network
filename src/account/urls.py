from django.urls import path
from account.views import edit, login, otp, password, register

app_name = 'account'

urlpatterns = [
    # Login
    path('login/', login.UserLogin.as_view(), name='login'),
    path('logout/', login.UserLogout.as_view(), name='logout'),
    # Register
    path('register/', register.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', register.activate, name='activate'),
    # Edit
    path('edit/', edit.Edit.as_view(), name='edit'),
    # OTP
    path('otp/auth/', otp.OtpAuth.as_view(), name='otp_auth'),
    path('otp/login/', otp.OtpLogin.as_view(), name='otp_login'),
    path('otp/register/', otp.OtpRegister.as_view(), name='otp_register'),
    # Change password
    path(
        'change-password/',
        password.ChangePassword.as_view(),
        name='change_password'
    ),
    # Reset password
    path(
        'reset-password/',
        password.ResetPassword.as_view(),
        name='reset_password'
    ),
    path(
        'reset/<uidb64>/<token>/',
        password.ResetPasswordConfirm.as_view(),
        name='reset_password_confirm'
    ),
]
