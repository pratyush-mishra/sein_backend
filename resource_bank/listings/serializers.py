from rest_framework import serializers
from .models import Listing, Message, ListingImage
from users.serializers import MemberSerializer
from django.contrib.auth import get_user_model


class ListingImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ListingImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

class ListingSerializer(serializers.ModelSerializer):
    owner = MemberSerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'description', 'category', 'qty', 'is_fee', 'fee',
            'dimensions', 'availability', 'condition', 'comment', 'images', 'contact_details',
            'is_approved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_approved', 'owner', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = MemberSerializer(read_only=True)
    User = get_user_model()
    recipient = MemberSerializer(read_only=True)  # For output
    recipient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='recipient'
    )
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), source='listing', write_only=True
    )

    class Meta:
        model = Message
        fields = ['id', 'listing', 'listing_id', 'sender', 'recipient', 'recipient_id', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']