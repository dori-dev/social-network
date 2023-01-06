from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User


class LoginForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'لطفا نام کاربری یا رمز عبور صحیح را وارد کن!',
        'inactive': 'این حساب کاربری غیر فعال شده.',
    }

    username = auth_forms.UsernameField(
        label='نام کاربری',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control mt-2 direction-change',
                'placeholder': 'نام کاربری ات رو وارد کن...',
            }
        )
    )
    password = forms.CharField(
        label='رمز عبور',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور ات رو وارد کن...',
            }
        ),
    )


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    error_messages = {
        'password_incorrect': 'رمز عبور قدیمی ات رو اشتباه وارد کردی!',
        'password_mismatch':  'دو رمز عبور جدید رو مثل هم وارد نکردی.',
    }

    old_password = forms.CharField(
        label='رمز عبور قدیمی',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'autofocus': True,
                'class': 'form-control mt-2 direction-change',
                'placeholder': 'رمز عبور قدیمی ات رو وارد کن...',
            }
        ),
    )
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور جدید ات رو وارد کن...',
            }
        ),
        strip=False,
        help_text='رمز عبور ات باید حداقل شامل ۸ کاراکتر باشد!',
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور جدید ات رو دوباره وارد کن...',
            }
        ),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']


class ResetPasswordForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label='ایمیل',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'class': 'form-control mt-2 mb-2 rtl direction-change',
                'placeholder': 'آدرس ایمیل حساب کاربری ات رو وارد کن...',
            }
        ),
    )


class SetPasswordForm(auth_forms.SetPasswordForm):
    error_messages = {
        'password_mismatch': 'دو رمز عبور جدید رو مثل هم وارد نکردی.',
    }

    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور جدید ات رو وارد کن...',
            }
        ),
        strip=False,
        help_text='رمز عبور ات باید حداقل شامل ۸ کاراکتر باشد!',
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور جدید ات رو دوباره وارد کن...',
            }
        ),
    )


class RegisterForm(auth_forms.UserCreationForm):
    error_messages = {
        'password_mismatch': 'دو رمز عبور رو مثل هم وارد نکردی.',
    }

    password1 = forms.CharField(
        label='رمز عبور',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'رمز عبور مورد نظرت...',
            }
        ),
        help_text='رمز عبور ات باید حداقل شامل ۸ کاراکتر باشد!',
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control mt-2 mb-2 direction-change',
                'placeholder': 'تکرار رمز عبور قبلی برای اطمینان...',
            }),
        strip=False,
        help_text='برای اطمینان رمز عبور ات رو دوباره اینجا وارد کن.',
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'email',
        )
        field_classes = {
            'username': auth_forms.UsernameField
        }
        labels = {
            'username': 'نام کاربری',
            'first_name': 'اسم',
            'email': 'ایمیل',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        # username
        help_text = "استفاده از حروف، اعداد و @ . + - _ مجاز است."
        username = self.fields['username']
        username.help_text = help_text
        username.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 direction-change'
        username.widget.attrs[
            'placeholder'
        ] = 'آیدی یا نام کاربری مورد نظرت...'
        username.error_messages = {
            'required': 'تعیین نام کاربری ضروری است!',
            'invalid': 'یک نام کاربری صحیح وارد کن.',
            'unique': 'هم اکنون کاربری با این آیدی وجود دارد.',
        }
        # first name
        first_name = self.fields['first_name']
        first_name.required = True
        first_name.widget.attrs['class'] = 'form-control mt-2 mb-2'
        first_name.widget.attrs['placeholder'] = 'اسم ات رو وارد کن...'
        first_name.error_messages = {
            'required': 'اسمتو بهم بگو تا بدونم چی صدات کنم!',
        }
        # email
        email = self.fields['email']
        email.required = True
        email.widget.attrs[
            'class'
        ] = 'form-control rtl mt-2 mb-2 direction-change'
        email.widget.attrs['placeholder'] = 'آدرس ایمیل ات...'
        email.error_messages = {
            'required': 'پر کردن فیلد ایمیل ضروری است!',
            'invalid': 'یک ایمیل صحیح وارد کن.',
        }
