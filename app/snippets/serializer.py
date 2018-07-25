from django.contrib.auth import get_user_model
from django.forms import widgets
from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User

__all__ = (
    'UserSerializer',
    'SnippetSerializer',
)


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = (
            'pk',
            'title',
            'code',
            'linenos',
            'language',
            'style',
            'owner',
        )
        # 읽기전용으로 처리가 된다.
        read_only_fields = (
            'owner',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'snippets',
        )


# class SnippetSerializer2:
#     pk = None
#     title = None
#     code = None
#
#     def __init__(self, instance):
#         if hasattr(instance, 'pk'):
#             self.pk = instance.pk
#         if hasattr(instance, 'title'):
#             self.title = instance.title
#         if hasattr(instance, 'code'):
#             self.code = instance.code
#
#     @property
#     def data(self):
#         return {
#             'pk': self.pk,
#             'title': self.title,
#             'code': self.code
#         }
