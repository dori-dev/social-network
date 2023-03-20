from django.urls import path
from account.views import auth, edit, otp, password

app_name = 'account'

urlpatterns = [
    path('login/', auth.UserLogin.as_view(), name='login'),
    path('logout/', auth.UserLogout.as_view(), name='logout'),
    path('register/', auth.Register.as_view(), name='register'),
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
