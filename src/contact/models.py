from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jalali_models


class Contact(models.Model):
    user_from = models.ForeignKey(
        "account.CustomUser",
        related_name='following_set',
        on_delete=models.CASCADE,
        verbose_name=_('User from'),
    )
    user_to = models.ForeignKey(
        "account.CustomUser",
        related_name='followers_set',
        on_delete=models.CASCADE,
        verbose_name=_('User to'),
    )
    created = jalali_models.jDateField(
        _('Created'),
        auto_now_add=True,
        db_index=True,
        editable=True,
    )

    class Meta:
        ordering = (
            '-created',
        )
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return f"{self.user_from} followed {self.user_to}"
