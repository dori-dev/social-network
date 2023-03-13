from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('User'),
    )
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Post'),
    )
    reply = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True,
        verbose_name=_('Reply'),
    )
    is_reply = models.BooleanField(
        _('Is reply'),
        default=False,
    )
    body = models.TextField(
        _('Body'),
        max_length=512,
    )
    created = models.DateTimeField(
        _('Created'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = (
            '-created',
        )

    def __str__(self):
        return f'{self.user} - {self.post}'
