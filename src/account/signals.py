from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from . import models

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)
