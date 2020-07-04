# Generated by Django 3.0.7 on 2020-07-04 01:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200704_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followed_users',
            field=models.ManyToManyField(blank=True, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
