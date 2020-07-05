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

    @action(detail=False, methods=['GET'])
    def info(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

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

    # @action(detail=False, methods=['GET'])
    # def follower_cards(self, request):
    #     queryset = request.user.followed_users.cards.all()
    #     user = request.user
    #     serializer = CardSerializer(user.followed_users.cards.all(), many=True, context={'request': request})
    #     return Response(serializer.data)

    
    #  def cardsbyid():
    #     """
    #     GET request to /cards/<cardID#> should give you the card with that ID
    #     """
    #     pass

    # def cardsupdate():
    #     """
    #     PATCH request to cards/<cardID#> should update that card with new info! Should only work with logged-in user cards
    #     """
    #     pass

    # def cardDeleter():
    #     """
    #     DELETE request to cards/<cardID#> should DELETE THAT CARD. Should only work with loged-in user cards
    #     """

class UserCardsView(views.APIView):
    """
    GET request to api/user_cards/<username>/ will return all of the user's cards
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
    

    

    # def postnewFriend():
    #     """
    #     POST request with friend username should add that user to the Logged-In User's following list
    #     """
    #     pass

    # def friendDeleter():
    #     """
    #     DELETE request to /following/<userID#>/ should delete remove that user from your friends list
    #     """
