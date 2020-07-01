from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import User, Card

admin.site.register(Card)
