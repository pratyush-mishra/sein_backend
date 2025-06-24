from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Listing, Message
from .serializers import ListingSerializer, MessageSerializer
#from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        GET all listings if the user is authenticated, otherwise return only approved listings.
        """
        if self.request.user.is_authenticated:
            return Listing.objects.all()
        else:
            return Listing.objects.filter(is_approved=True)
        
    def perform_create(self, serializer):
        """
        CREATE a new listing and associate it with the authenticated user.
        """
        serializer.save(owner=self.request.user)
    
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Members can only see messages they sent or received
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        )
    
    def perform_create(self, serializer):
        """
        CREATE a new message and associate it with the authenticated user.
        """
        serializer.save(sender=self.request.user)