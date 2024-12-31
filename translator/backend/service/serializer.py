from rest_framework import serializers
from .models import GeminiModel


class GeminiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiModel
        fields = [
            "id",
            "message",
            "prompt",
            "language_message",
            "type",
            "response_data",
            "error",
            "error_message",
            "user",
        ]
        extra_kwargs = {
            "response_data": {"read_only": True},
            "error": {"read_only": True},
            "error_message": {"read_only": True},
        }
