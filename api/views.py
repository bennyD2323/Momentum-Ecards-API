from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from api.models import Card
from api.serializers import CardSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View set representing the User model. It has default methods for GET, POST, PUT, DELETE requests, but its 'Read-Only' status prohibits POST, PUT, and DELETE for User data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def info(self, request):
        """
        This returns User model data for the User who is currently logged-in and making the GET request.
        """
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class CardViewSet(viewsets.ModelViewSet):
    """
    Viewset representing the Card model.
    """
    # queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Sets the queryset to the cards belonging to the logged-in User.
        """
        cards = self.request.user.cards.all()
        return cards

    def perform_create(self, serializer):
        """
        Ensures that the logged-in User who is creating a card is set as that card's owner.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def all(self, request):
        cards= Card.objects.all()
        page= self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def own(self, request):
        """
        Returns a list of cards belonging to the logged-in User.
        """
        cards = request.user.cards.all()
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    # """
    # """
    def follower_cards(self, request):
        cards = Card.objects.filter(user__users=request.user)
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    
# class CardDetailView(views.APIView):
# queryset = Card.objects.all()
# # ADD PERMISSIONS
#     def get(self, request, id):
#         """
#         GET request to /cards/<cardID#> should give you the card with that ID
#         """
#         card = get_object_or_404(Card, id=card.id)
#         return Response()


class UserCardsView(views.APIView):
    # ADD PERMISSIONS
    """
    GET request to api/user_cards/<username>/ will return all of the user's cards
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = CardSerializer(user.cards.all(), many=True, context={'request': request})
        return Response(serializer.data)

class FollowingView(views.APIView):
    # ADD PERMISSIONS
    """
    Shows all users that the logged-in user is following
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user.followed_users.all(), many=True, context={'request': request})
        return Response(serializer.data) 
    
    def post(self, request, format=None):
        """
        POST request with friend username adds that user to the Logged-In User's following list.
        """
        username = request.data.get("user")
        user = get_object_or_404(User, username=username)
        request.user.followed_users.add(user)
        return Response({"user": username}, status=201) 

class RemoveFollowView(views.APIView):
    # """
    # """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, username, format=None):
        """
        DELETE request to /following/<username>/ should delete remove that user from your friends list.
        """
        user = get_object_or_404(User, username=username)
        request.user.followed_users.remove(user)
        return Response()
