from django.urls import path

from .views import (
    health,
    test_connection,
    chat,
    test_llm
)

urlpatterns = [
    path("health/", health),
    path("test/", test_connection),
    path("chat/", chat),
    path("test-llm/", test_llm),
]