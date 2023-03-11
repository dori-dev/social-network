from django.db.models.signals import m2m_changed, post_save, post_delete
from django.db.models import F
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


@receiver(post_delete, sender=models.Post)
def decrease_posts_count(instance: models.Post, **kwargs):
    instance.user.posts_count = F('posts_count') - 1
    instance.user.save()


@receiver(post_save, sender=models.Post)
def increase_posts_count(instance: models.Post, created, **kwargs):
    if created:
        instance.user.posts_count = F('posts_count') + 1
        instance.user.save()
