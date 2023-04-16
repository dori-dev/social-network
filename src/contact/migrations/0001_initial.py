# Generated by Django 4.1.5 on 2023-03-24 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateField(auto_now_add=True, db_index=True, verbose_name='Created')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_set', to=settings.AUTH_USER_MODEL, verbose_name='User from')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers_set', to=settings.AUTH_USER_MODEL, verbose_name='User to')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ('-created',),
            },
        ),
    ]