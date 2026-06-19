from django.urls import path

from .views import (
    health,
    chat,
    chat_history,
    start_experiment,
    complete_survey,
    experiment_export,
    experiment_stats,
    chat_export
)

urlpatterns = [
    path("health/", health),
    path("chat/", chat),
    path("chat-history/<uuid:session_id>/", chat_history),
    path("start-experiment/", start_experiment),
    path("complete-survey/", complete_survey),
    path("experiment-export/", experiment_export),
    path("experiment-stats/", experiment_stats),
    path("chat-export/", chat_export),
]