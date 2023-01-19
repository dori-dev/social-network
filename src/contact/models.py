from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name='following_set',
        on_delete=models.CASCADE,
        verbose_name=_('User from'),
    )
    user_to = models.ForeignKey(
        User,
        related_name='followers_set',
        on_delete=models.CASCADE,
        verbose_name=_('User to'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        editable=True,
        verbose_name=_('Created'),
    )

    class Meta:
        ordering = (
            '-created',
        )
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return f"{self.user_from} followed {self.user_to}"
