from django.urls import path
from .views import CreateGeminiRequest, DeleteGeminiRequest

urlpatterns = [
    path("request/", CreateGeminiRequest.as_view()),
    path(
        "request/delete/<int:pk>/",
        DeleteGeminiRequest.as_view(),
    ),
]
