from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from rest_framework.authtoken.models import Token

from django.db.models import Q



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Overrides the default Create process. Assigns an authorization token to a User when they are created.
    """
    if created:
        Token.objects.create(user=instance)

class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="cards", null=True, blank=True)
    
    COLOR_CHOICES = (
        ('green', 'green'),
        ('yellow', 'yellow'),
        ('pink', 'pink'),
    )  
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, null=True, blank=True)

    FONT_CHOICES = (  
            ('montserratSubrayada', 'montserratSubrayada'),
            ('greatVibes', 'greatVibes'),
            ('bebasNeue', 'bebasNeue'),
        )
    font = models.CharField(max_length=50, choices=FONT_CHOICES, null=True, blank=True) 

    BORDER_CHOICES = (  
            ('solid', 'solid'),
            ('double', 'double'),
            ('dotted', 'dotted'),
        )
    border_style = models.CharField(max_length=50, choices=BORDER_CHOICES, null=True, blank=True) 
    card_name = models.CharField(max_length=50, null=True, blank=True)
    card_text = models.CharField(max_length=1000, null=True, blank=True)  