from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jalali_models


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Email'),
        unique=True,
    )
    following = models.ManyToManyField(
        'self',
        through='contact.Contact',
        related_name='followers',
        symmetrical=False,
    )

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

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f'{self.user.username}\'s profile'
