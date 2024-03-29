from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jalali_models


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Email'),
        null=True,
        blank=True,
    )
    following = models.ManyToManyField(
        'self',
        through='contact.Contact',
        related_name='followers',
        symmetrical=False,
    )
    posts_count = models.IntegerField(
        _('Posts Count'),
        db_index=True,
        default=0,
    )

    class Meta:
        ordering = (
            '-posts_count',
        )
        verbose_name = _('Custom user')
        verbose_name_plural = _('Custom users')

    def get_absolute_url(self):
        return reverse('user:detail', args=(self.username,))


User = get_user_model()


def check_image(image: ImageFieldFile):
    if image.size > 2_000_000:
        raise ValidationError(
            "حجم عکس ات بیشتر از 2 مگابایت است!"
        )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    date_of_birth = jalali_models.jDateField(
        _('Date of birth'),
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        _('Photo'),
        upload_to='users/%Y/%m/%d/',
        blank=True,
        validators=[
            check_image,
        ],
        default='profile.png',
    )
    bio = models.CharField(
        _('Biography'),
        max_length=128,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def save(self, *args, **kwargs):
        if not self.photo:
            self.photo = 'profile.png'
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}\'s profile'


class OTP(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    phone = models.CharField(
        _("Phone"),
        max_length=15,
    )
    otp = models.PositiveIntegerField(
        _("OTP"),
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        _("Created"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTP')

    def __str__(self):
        return f'{self.user} - {self.phone}'
