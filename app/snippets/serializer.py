from django.forms import widgets
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = (
            'pk',
            'title',
            'code',
            'linenos',
            'language',
            'style',
        )
