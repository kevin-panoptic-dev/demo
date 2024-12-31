from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializer import (
    HistorySerializer,
    UserSerializer,
    IssueSerializer,
    FeedbackSerializer,
)
from .models import TranslateHistory, IssueModel, FeedbackModel
from library.utility import prismelt


class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


class DeleteUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return User.objects.filter(user=user)


class AppendHistory(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return TranslateHistory.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            prismelt("BackendError: Invalid History Serializer.", color=(255, 0, 0))


class DeleteHistory(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return TranslateHistory.objects.filter(user=user)


class SubmitIssue(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return IssueModel.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            prismelt("BackendError: Invalid Issue Serializer.", color=(255, 0, 0))


class DeleteIssue(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IssueSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return IssueModel.objects.filter(user=user)


class SubmitFeedback(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return FeedbackModel.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            prismelt("BackendError: Invalid Feedback Serializer.", color=(255, 0, 0))


class DeleteFeedback(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return FeedbackModel.objects.filter(user=user)
