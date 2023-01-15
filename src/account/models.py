from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    following = models.ManyToManyField(
        'self',
        through='Contact',
        related_name='followers',
        symmetrical=False,
    )


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
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        validators=[
            check_image,
        ],
        default='profile.png',
    )

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f'{self.user.username}\'s profile'


class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='following_set',
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        User,
        related_name='followers_set',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        editable=True,
    )

    class Meta:
        ordering = (
            '-created',
        )

    def __str__(self):
        return f"{self.user_from} followed {self.user_to}"
