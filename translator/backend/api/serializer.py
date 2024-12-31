from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TranslateHistory, FeedbackModel, IssueModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateHistory
        fields = ["id", "origin", "corresponding", "create_at", "user"]
        extra_kwargs = {
            "origin": {"read_only": True},
            "corresponding": {"read_only": True},
        }


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = ["id", "title", "content", "create_at", "user"]
        extra_kwargs = {"title": {"read_only": True}, "content": {"read_only": True}}


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueModel
        fields = ["id", "title", "content", "create_at", "user", "resolved"]
        extra_kwargs = {"title": {"read_only": True}, "content": {"read_only": True}}
