from random import choices
from string import ascii_letters

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse


UserModel = get_user_model()


def check_image(image: ImageFieldFile):
    if image.size > 50_000_000:
        raise ValidationError(
            "حجم عکس ات بیشتر از 50 مگابایت است!"
        )


class Post(models.Model):
    user = models.ForeignKey(
        UserModel,
        related_name='images',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=8,
        editable=True,
        unique=False,
        db_index=True,
        blank=True,
    )
    url = models.URLField(
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        validators=[
            check_image,
        ],
    )
    description = models.TextField(
        blank=True,
    )
    created = models.DateField(
        auto_now_add=True,
        db_index=True,
    )
    users_like = models.ManyToManyField(
        UserModel,
        related_name='images_liked',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self._random_slug(8)
            while Post.objects.filter(slug=slug).exists():
                slug = self._random_slug(8)
            self.slug = slug
        return super().save(*args, **kwargs)

    @staticmethod
    def _random_slug(length: int) -> str:
        return "".join(choices(ascii_letters, k=length))

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'slug',
                ],
                name='slug_idx',
            ),
            models.Index(
                fields=[
                    'created',
                ],
                name='created_idx',
            ),
        ]
        ordering = (
            '-created',
        )
