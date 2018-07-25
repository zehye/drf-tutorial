from django.contrib.auth import get_user_model
from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User

__all__ = (
    'UserListSerializer',
)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
        )


class UserListSerializer(UserBaseSerializer):
    pass
