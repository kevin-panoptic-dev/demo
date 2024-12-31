from django.db import models
from django.contrib.auth.models import User


class GeminiModel(models.Model):
    message = models.TextField(max_length=5000)
    prompt = models.TextField()
    language_message = models.TextField(max_length=100)
    type = models.CharField(
        choices=[("validate", ""), ("translate", "")], max_length=10
    )
    response_data = models.JSONField(blank=True, null=True)
    error = models.CharField(max_length=1, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="GeminiModel")
