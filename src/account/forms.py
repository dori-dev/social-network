from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class LoginForm(auth_forms.AuthenticationForm):
    error_messages = {
        "invalid_login": "لطفا نام کاربری یا رمز عبور صحیح را وارد کن!",
        "inactive": "این حساب کاربری غیر فعال شده.",
    }

    username = auth_forms.UsernameField(
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


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_incorrect": "رمز عبور قدیمی ات رو اشتباه وارد کردی!",
        "password_mismatch":  "دو رمز عبور جدید رو مثل هم وارد نکردی.",
    }

    old_password = forms.CharField(
        label="رمز عبور قدیمی",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control mt-2 direction-change",
                "placeholder": "رمز عبور قدیمی ات رو وارد کن...",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control mt-2 mb-2 direction-change",
                "placeholder": "رمز عبور جدید ات رو وارد کن...",
            }
        ),
        strip=False,
        help_text="رمز عبور ات باید حداقل شامل ۸ کاراکتر باشد!",
    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control mt-2 mb-2 direction-change",
                "placeholder": "رمز عبور جدید ات رو دوباره وارد کن...",
            }
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]


class ResetPasswordForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label="ایمیل",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control mt-2 mb-2 rtl direction-change",
                "placeholder": "آدرس ایمیل حساب کاربری ات رو وارد کن...",
            }
        ),
    )


class SetPasswordForm(auth_forms.SetPasswordForm):
    error_messages = {
        "password_mismatch": "دو رمز عبور جدید رو مثل هم وارد نکردی.",
    }

    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control mt-2 mb-2 direction-change",
                "placeholder": "رمز عبور جدید ات رو وارد کن...",
            }
        ),
        strip=False,
        help_text="رمز عبور ات باید حداقل شامل ۸ کاراکتر باشد!",
    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control mt-2 mb-2 direction-change",
                "placeholder": "رمز عبور جدید ات رو دوباره وارد کن...",
            }
        ),
    )
