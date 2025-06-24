from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Member

# This serializer is used for creating new users (registration)
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = Member
        fields = ('id', 'email', 'username', 'password', 'bio', 'contact_details')
        extra_kwargs = {
            'password': {'write_only': True},
            'bio': {'required': False, 'allow_blank': True},
            'contact_details': {'required': False, 'allow_blank': True},
        }

# This serializer is used for retrieving user details
class MemberSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Member
        fields = ('id', 'email', 'username', 'bio', 'contact_details', 'profile_picture')