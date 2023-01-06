from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    )

    def __str__(self):
        return f'{self.user.username}\'s profile'
