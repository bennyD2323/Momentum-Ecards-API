from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from users.models import User
from api.models import Card
from api.serializers import CardSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def own(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

class UserCardsView(views.APIView):
    """
    Shows all cards for a specific user, checking by username
    """
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = CardSerializer(user.cards.all(), many=True, context={'request': request})
        return Response(serializer.data)