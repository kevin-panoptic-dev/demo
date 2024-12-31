from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from .api_clients.gemini import fetch_data_from_gemini
from .serializer import GeminiModelSerializer
from .models import GeminiModel
from typing import Literal
from pymodule.utility import prismelt


class CreateGeminiRequest(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeminiModelSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return GeminiModel.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["user"] = self.request.user.id
        if serializer.is_valid():
            serializer.save()
            response_data = self.perform_create(serializer)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            prismelt(serializer.errors, color=(255, 0, 0))

    def perform_create(self, serializer):  # type: ignore
        message: str = serializer.validated_data["message"]
        prompt: str = serializer.validated_data["prompt"]
        language_message: str = serializer.validated_data["language_message"]
        type: Literal["validate", "translate"] = serializer.validated_data["type"]
        response_data = fetch_data_from_gemini(
            message=message,
            prompt=prompt,
            language_message=language_message,
            type=type,
        )
        serializer.save(
            response_data=response_data["response"],
            error=response_data["error"],
            error_message=response_data["error_message"],
        )
        return response_data


class DeleteGeminiRequest(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeminiModelSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return GeminiModel.objects.filter(user=user)
