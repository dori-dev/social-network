from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control mt-2 direction-change",
                "placeholder": "نام کاربری ات رو وارد کن...",
            }
        )
    )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control mt-2 mb-2 direction-change",
                "placeholder": "رمز عبور ات رو وارد کن...",
            }
        ),
    )

    error_messages = {
        "invalid_login": "لطفا نام کاربری یا رمز عبور صحیح را وارد کن!",
        "inactive": "این حساب کاربری غیر فعال شده.",
    }
