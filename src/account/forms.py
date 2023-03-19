from io import BytesIO
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Profile, OTP


User = get_user_model()
User._meta.get_field('first_name').validators[0].limit_value = 30
error_message = (
    'طول اسم باید کمتر از 30 کاراکتر باشد'
    ' اما تو %(show_value)s کاراکتر وارد کردی!'
)
User._meta.get_field('first_name').validators[0].message = error_message


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


class BaseRegisterForm(auth_forms.UserCreationForm):
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
        )
        field_classes = {
            'username': auth_forms.UsernameField
        }
        labels = {
            'username': 'نام کاربری',
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


class RegisterForm(BaseRegisterForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        field_classes = {
            'username': auth_forms.UsernameField
        }
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('هم اکنون کاربری با این ایمیل وجود دارد.')
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
        )
        field_classes = {
            'username': auth_forms.UsernameField
        }
        labels = {
            'username': 'نام کاربری',
            'first_name': 'اسم',
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
        username.required = True
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
        # first_name
        first_name = self.fields['first_name']
        first_name.widget.attrs['class'] = 'form-control mt-2 mb-2'
        first_name.widget.attrs[
            'placeholder'
        ] = 'اسمتو بهم بگو تا بدونم چی صدات کنم!'


class ImageField(forms.FileField):
    default_error_messages = {
        "invalid_image": (
            "لطفا یک عکس آپولود کن."
        ),
    }

    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        from PIL import Image

        if hasattr(data, "temporary_file_path"):
            file = data.temporary_file_path()
        else:
            if hasattr(data, "read"):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data["content"])

        try:
            image = Image.open(file)
            image.verify()
            f.image = image
            f.content_type = Image.MIME.get(image.format)
        except Exception as exc:
            raise ValidationError(
                self.default_error_messages["invalid_image"],
                code="invalid_image",
            ) from exc
        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)
        return f

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, forms.FileInput) and \
                "accept" not in widget.attrs:
            attrs.setdefault("accept", "image/*")
        return attrs


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'bio',
            'date_of_birth',
            'photo',
        )
        widgets = {
            'date_of_birth': AdminJalaliDateWidget,
        }
        field_classes = {
            'photo': ImageField,
            'date_of_birth': JalaliDateField,
        }
        labels = {
            'bio': 'بیو',
            'date_of_birth': 'تاریخ تولد',
            'photo': 'عکس پروفایل',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        date_of_birth = self.fields['date_of_birth']
        date_of_birth.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 ltr jalali_date-date'
        date_of_birth.widget.attrs[
            'placeholder'
        ] = '1370-11-24'
        date_of_birth.widget.attrs[
            'autocomplete'
        ] = 'off'
        # photo
        photo = self.fields['photo']
        photo.widget.attrs['class'] = 'form-control mt-2 mb-2'
        photo.widget.attrs[
            'placeholder'
        ] = 'عکس پروفایل ات رو آپلود کن...'
        # bio
        bio = self.fields['bio']
        bio.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 rtl'
        bio.widget.attrs['dir'] = 'auto'
        bio.widget.attrs[
            'placeholder'
        ] = 'توضیحی در مورد خودت بنویس...'
        bio.error_messages = {
            'max_length': 'توضیحات ات خیلی زیاد شد!',
        }


class OtpForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = (
            'phone',
        )
        labels = {
            'phone': 'شماره تلفن',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        phone = self.fields['phone']
        phone.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 ltr'
        phone.widget.attrs[
            'placeholder'
        ] = 'مثال: 09133352042'
        phone.error_messages = {
            'max_length': 'طول شماره تلفن ات بیش از حد مجازه.',
        }

    def clean_phone(self):
        phone: str = self.cleaned_data['phone']
        if not phone.isdigit():
            raise ValidationError('شماره تلفنی که وارد کردی اشتباهه.')
        return phone


class OtpLoginForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = (
            'otp',
        )
        labels = {
            'otp': 'کد تایید',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': 'پر کردن این فیلد ضروری است!',
                'invalid': 'این فیلد رو به درستی وارد کن!',
            }
        otp = self.fields['otp']
        otp.widget.attrs[
            'class'
        ] = 'form-control mt-2 mb-2 direction-change rtl'
        otp.widget.attrs[
            'placeholder'
        ] = 'کد تاییدی که به تلفنت پیامک شد رو وارد کن...'
        otp.error_messages = {
            'max_length': 'طول کد تایید بیش از حد مجازه.',
        }

    def clean_otp(self):
        otp: str = self.cleaned_data['otp']
        if isinstance(otp, str):
            raise ValidationError('کد تایید باید فقط شامل عدد باشه.')
        return otp


class OtpRegisterForm(BaseRegisterForm):
    otp = forms.IntegerField(
        label='کد تایید',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'autocomplete': 'off',
                'class': 'form-control mt-2 mb-2 direction-change rtl',
                'placeholder': 'کد تاییدی که به تلفنت پیامک شد رو وارد کن...',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields([
            'username',
            'otp',
            'password1',
            'password2',
        ])
        # otp
        otp = self.fields['otp']
        otp.error_messages = {
            'max_length': 'طول کد تایید بیش از حد مجازه.',
        }

    def clean_otp(self):
        otp: str = self.cleaned_data['otp']
        if isinstance(otp, str):
            raise ValidationError('کد تایید باید فقط شامل عدد باشه.')
        return otp
