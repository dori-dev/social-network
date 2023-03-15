from django.db.models.signals import m2m_changed, post_save, post_delete
from django.db.models import F, Count
from django.db import transaction
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


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


@receiver(post_save, sender=models.Post)
@on_transaction_commit
def set_related_posts(instance: models.Post, **kwargs):
    tags = instance.tags.values_list(
        'id',
        flat=True,
    )
    # Related posts
    related_posts = list(
        models.Post.objects
        .filter(tags__in=tags)
        .distinct()
        .exclude(id=instance.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-created')
        .values_list('id', flat=True)[:12]
    )
    # User other posts
    diff = 12 - len(related_posts)
    if diff > 0:
        other = instance.user.posts.exclude(
            id=instance.id
        ).values_list('id', flat=True)[:diff]
        related_posts.extend(list(other))
        # Latest posts
        diff = 12 - len(related_posts)
        if diff > 0:
            latest = models.Post.objects.exclude(
                id__in=related_posts,
            ).values_list('id', flat=True)[:diff]
            related_posts.extend(list(latest))
    instance.related_posts.clear()
    instance.related_posts.add(*related_posts)
