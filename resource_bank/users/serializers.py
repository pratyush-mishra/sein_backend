from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Member

# This serializer is used for creating new users (registration)
class UserCreateSerializer(BaseUserCreateSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    is_approved = serializers.BooleanField(read_only=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = Member
        fields = ('id', 'email', 'username', 'password', 'bio', 'contact_details', 'is_approved')
        extra_kwargs = {
            'password': {'write_only': True},
            'bio': {'required': False, 'allow_blank': True},
            'contact_details': {'required': False, 'allow_blank': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_email(self, value):
        """Ensure email is unique"""
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """Ensure username is unique"""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

# This serializer is used for retrieving user details
class MemberSerializer(BaseUserSerializer):
    is_approved = serializers.BooleanField(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        model = Member
        fields = ('id', 'email', 'username', 'bio', 'contact_details', 'profile_picture', 'date_joined', 'is_active', 'is_approved')
        read_only_fields = ('id', 'date_joined', 'is_active', 'is_approved')

    def to_representation(self, instance):
        """Customize the representation of user data"""
        data = super().to_representation(instance)
        
        # Handle profile picture URL
        if instance.profile_picture:
            request = self.context.get('request')
            if request:
                data['profile_picture'] = request.build_absolute_uri(instance.profile_picture.url)
        
        return data

# Optional: Custom serializer for updating user profile
class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('username', 'bio', 'contact_details', 'profile_picture')
        extra_kwargs = {
            'bio': {'required': False, 'allow_blank': True},
            'contact_details': {'required': False, 'allow_blank': True},
        }

    def validate_username(self, value):
        """Ensure username is unique (excluding current user)"""
        if Member.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

# Optional: Minimal serializer for listing users (if needed)
class MemberListSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(read_only=True)
    class Meta:
        model = Member
        fields = ('id', 'username', 'profile_picture', 'is_approved')

    def to_representation(self, instance):
        """Customize the representation for list view"""
        data = super().to_representation(instance)
        
        # Handle profile picture URL
        if instance.profile_picture:
            request = self.context.get('request')
            if request:
                data['profile_picture'] = request.build_absolute_uri(instance.profile_picture.url)
        
        return data