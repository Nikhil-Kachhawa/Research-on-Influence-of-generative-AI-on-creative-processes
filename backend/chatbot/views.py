from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def health(request):
    return Response({"status": "working"})

@api_view(["GET"])
def test_connection(request):
    return Response({
        "message": "Hello from Django Backend!"
    })