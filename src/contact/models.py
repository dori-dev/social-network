from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
