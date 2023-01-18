from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Action(models.Model):
    user = models.ForeignKey(
        UserModel,
        related_name='actions',
        db_index=True,
        on_delete=models.CASCADE,
    )
    verb = models.CharField(
        max_length=256,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        editable=True,
    )
    limit = models.Q(app_label='post', model='post') | \
        models.Q(app_label='account', model='profile') | \
        models.Q(app_label='contact', model='contact')
    target_ct = models.ForeignKey(
        ContentType,
        related_name='actions',
        on_delete=models.CASCADE,
        limit_choices_to=limit,
        blank=True,
        null=True,
    )
    target_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
    )
    target = GenericForeignKey(
        'target_ct',
        'target_id',
    )

    class Meta:
        ordering = (
            '-created',
        )

    def __str__(self) -> str:
        return f"{self.user}:{self.verb}"
