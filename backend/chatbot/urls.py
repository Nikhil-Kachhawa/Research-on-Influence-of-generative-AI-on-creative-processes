from django.urls import path
from .views import health, test_connection

urlpatterns = [
    path("health/", health),
    path("test/", test_connection),
]