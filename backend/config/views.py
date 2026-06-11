from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def api_home(request):
    return Response({
        "project": "Research Lab AI",
        "version": "1.0",
        "status": "running"
    })