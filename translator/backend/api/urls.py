from django.urls import path
from .views import AppendHistory, DeleteHistory

urlpatterns = [
    path("history/", AppendHistory.as_view()),
    path("history/delete/<int:pk>/", DeleteHistory.as_view()),
]
