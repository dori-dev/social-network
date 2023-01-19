from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from . import models


@receiver(m2m_changed, sender=models.Post.users_like.through)
def update_total_likes(instance: models.Post, action, **kwargs):
    if action == 'post_add':
        instance.total_likes += 1
        instance.save()
    elif action == 'post_remove':
        instance.total_likes -= 1
        instance.save()
