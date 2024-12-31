from django.db import models
from django.contrib.auth.models import User


class TranslateHistory(models.Model):
    origin = models.TextField(max_length=2000)
    corresponding = models.TextField(max_length=2000)
    create_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="TranslateHistory"
    )

    def __str__(self) -> str:
        return self.corresponding


class FeedbackModel(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(max_length=10000)
    create_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="FeedbackModel"
    )

    def __str__(self) -> str:
        return self.title


class IssueModel(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(max_length=10000)
    create_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="IssueModel")
    resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
