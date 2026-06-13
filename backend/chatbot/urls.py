from django.urls import path

from .views import (
    health,
    chat,
    chat_history
)

urlpatterns = [
    path("health/", health),
    path("chat/", chat),
    path("chat-history/<uuid:session_id>/", chat_history),
]