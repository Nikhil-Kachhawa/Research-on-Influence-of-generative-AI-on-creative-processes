from django.urls import path
from .views import health, test_connection, chat
urlpatterns = [
    path("health/", health),
    path("test/", test_connection),
    path("chat/", chat),
]