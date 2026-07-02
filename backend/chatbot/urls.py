from django.urls import path

from .views import (
    health,
    start_experiment,
    continue_experiment,
    finish_chat,
    chat,
    chat_history,
    attentionPrediction,
)

urlpatterns = [
    path("health/", health),
    path("start-experiment/", start_experiment),
    path("continue-experiment/", continue_experiment),
    path("finish-chat/", finish_chat),
    path("chat/", chat),
    path(
        "chat-history/<uuid:session_id>/",
        chat_history,
    ),
    path(
        "attentionPrediction/",
        attentionPrediction,
    ),
]
