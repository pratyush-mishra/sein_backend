from rest_framework import serializers
from .models import Listing, Message
from users.serializers import MemberSerializer

class ListingSerializer(serializers.ModelSerializer):
    owner = MemberSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'owner', 'title', 'description', 'image', 'contact_details','is_approved', 'created_at', 'updated_at']
        read_only_fields = ['is_approved', 'owner']

class MessageSerializer(serializers.ModelSerializer):
    sender = MemberSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'listing', 'sender', 'recipient', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']