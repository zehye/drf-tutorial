from django.contrib.auth import get_user_model
from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from .users import UserListSerializer
from ..models import Snippet


__all__ = (
    'SnippetListSerializer',
    'SnippetDetailSerializer',
)


class SnippetBaseSerializer(serializers.ModelSerializer):
    owner = UserListSerializer()

    class Meta:
        model = Snippet
        fields = (
            'pk',
            'title',
            'linenos',
            'language',
            'style',
            'owner',
        )
        # 읽기전용으로 처리가 된다.
        read_only_fields = (
            'owner',
        )

class SnippetListSerializer(SnippetBaseSerializer):
    pass


class SnippetDetailSerializer(SnippetBaseSerializer):
    class Mata(SnippetBaseSerializer.Meta):
        fields = SnippetBaseSerializer.Meta.fields + ('code',)
