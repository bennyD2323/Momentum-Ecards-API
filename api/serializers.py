from rest_framework import serializers
from users.models import User
from api.models import Card


class UserSerializer(serializers.ModelSerializer):
    # followed_users = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'followed_users',
            'first_name',
            'last_name',
        ]


class CardSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Card
        fields = [
            'id',
            'url',
            'user',
            'color',
            'border_style',
            'font',
            'card_name',
            'card_text',
        ]