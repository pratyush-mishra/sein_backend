from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Listing, Message, ListingImage
from .serializers import ListingSerializer, MessageSerializer, ListingImageSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from rest_framework import filters

# for email moderation
from django.shortcuts import render
from django.core import signing
from django.urls import reverse
from django.http import HttpResponse, Http404
from datetime import timedelta

# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        GET all listings if the user is authenticated, otherwise return only approved listings.
        """
        queryset = Listing.objects.all() if self.request.user.is_authenticated else Listing.objects.filter(is_approved=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_approved', False):
            return Response({'detail': 'Your account is not approved yet.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Handle image uploads
        images_data = request.FILES.getlist('images')
        for image_data in images_data:
            ListingImage.objects.create(listing=serializer.instance, image=image_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        """
        CREATE a new listing and associate it with the authenticated user.
        """
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) #True for PUT, False for PATCH
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Handle image additions
        images_data = request.FILES.getlist('images')
        for image_data in images_data:
            ListingImage.objects.create(listing=instance, image=image_data)

        # Handle image deletions
        images_to_delete_ids = request.data.get('images_to_delete')
        if images_to_delete_ids:
            if not isinstance(images_to_delete_ids, list):
                images_to_delete_ids = [images_to_delete_ids]
            ListingImage.objects.filter(id__in=images_to_delete_ids, listing=instance).delete()

        # Re-serialize the instance to reflect changes in images
        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        return Response(Listing.LISTING_CATEGORIES)
    
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
        if not getattr(self.request.user, 'is_approved', False):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Your account is not approved yet.')
        serializer.save(sender=self.request.user)

# new view for handling one-click moderation from email
def moderate_listing(request, token):
    """
    View to handle listing moderation (approve/reject) via email link.
    """
    signer = signing.TimestampSigner()
    
    try:
        # Unsign the token. It will raise BadSignature if tampered with or SignatureExpired if too old (set to 30 days)
        data = signer.unsign(token, max_age=timedelta(days=30))
        action, listing_id = data.split(':')

        listing = Listing.objects.get(id=listing_id)
    
    except (signing.BadSignature, signing.SignatureExpired, Listing.DoesNotExist):
        raise Http404("moderation link is invalid or expired.")

    if action == 'approve':
        listing.is_approved = True
        listing.save()
        
        # notify the listing owner
        send_mail(
            'Your listing has been approved',
            f'Your listing "{listing.title}" has been approved.',
            settings.DEFAULT_FROM_EMAIL,
            [listing.owner.email],
            fail_silently=False,
        )
        return HttpResponse(f'Listing approved successfully: {listing.title}. This window can now be closed.')
    
    elif action == 'reject':
        listing_title = listing.title
        listing_owner_email = listing.owner.email
        listing_owner_username = listing.owner.username
        listing.delete()

        # Notify the owner of the rejection
        send_mail(
            'Update on your listing submission',
            f'Hi {listing_owner_username},\n\n. Thank you for your submission. Unfortunately your listing "{listing_title}" has been rejected.',
            settings.DEFAULT_FROM_EMAIL,
            [listing_owner_email],
            fail_silently=False,
        )
        return HttpResponse(f'Listing "{listing_title}" has been rejected and deleted. This window can now be closed.')
    
    else:
        return HttpResponse("Invalid action specified in the moderation link.")