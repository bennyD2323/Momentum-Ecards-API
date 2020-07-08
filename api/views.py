from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from api.models import Card
from api.serializers import CardSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# ADD PERMISSIONS
    @action(detail=False, methods=['GET'])
    # """
    # """
    def info(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class CardViewSet(viewsets.ModelViewSet):
    # """
    # """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
# ADD PERMISSIONS
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=False, methods=['GET'])
    # """
    # """
    def own(self, request):
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    # """
    # """
    def follower_cards(self, request):
        cards = Card.objects.filter(user__users=request.user)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    

class UserCardsView(views.APIView):
    # ADD PERMISSIONS
    """
    GET request to api/user_cards/<username>/ will return all of the user's cards
    """
    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = CardSerializer(user.cards.all(), many=True, context={'request': request})
        return Response(serializer.data)

class FollowingView(views.APIView):
    # ADD PERMISSIONS
    """
    Shows all users that the logged-in user is following.
    """
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user.followed_users.all(), many=True, context={'request': request})
        return Response(serializer.data) 
    
    def post(self, request, format=None):
        """
        POST request with friend username should add that user to the Logged-In User's following list.
        """
        username = request.data.get("user")
        user = get_object_or_404(User, username=username)
        request.user.followed_users.add(user)
        return Response({"user": username}, status=201)

class RemoveFollowView(views.APIView):
    # ADD PERMISSIONS
    def delete(self, request, username, format=None):
        """
        DELETE request to /following/<username/ should delete remove that user from your friends list.
        """
        user = get_object_or_404(User, username=username)
        request.user.followed_users.remove(user)
        return Response()
