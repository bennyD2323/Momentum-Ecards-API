from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from api.models import Card
from api.serializers import CardSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #  @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    # def followed_users(self, request):
    #     followed_users = request.user.followed_users.all()
    #     serializer = CardSerializer(cards, many=True, context={'request': request})
    #     return Response(serializer.data)


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

class FollowingView(views.APIView):
    """
    Shows all users that the logged in user is following
    """
    
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user.followed_users.all(), many=True, context={'request': request})
        return Response(serializer.data) 

