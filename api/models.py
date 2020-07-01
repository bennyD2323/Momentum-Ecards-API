from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from rest_framework.authtoken.models import Token

from django.db.models import Q





# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)



class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="cards", null=True, blank=True),

    color = models.CharField(max_length=20, null=True, blank=True),
    font = models.CharField(max_length=20, null=True, blank=True),
    border_style = models.CharField(max_length=20, null=True, blank=True),
    # favorited_by = models.ManyToManyField(to=User, related_name="favorite_cards")
    card_name = models.CharField(max_length=50, null=True, blank=True),
    card_text = models.CharField(max_length=250, null=True, blank=True),