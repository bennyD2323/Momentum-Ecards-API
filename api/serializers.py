from rest_framework import serializers
from users.models import User
from api.models import Card


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]

class CardSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    class Meta:
        model = Card
        fields = [
            'url',
            'user',
            'color',
            'border_style',
            'font',
            'card_name',
            'card_text',
        ]