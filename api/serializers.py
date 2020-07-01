from rest_framework import serializers
from users.models import User
from api.models import Card


class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = [
            'id',
            'url',
            'color',
            'border_style',
            'font',
            'card_name',
            'card_text',
        ]