from rest_framework.response import Response
from rest_framework.decorators import api_view

from chatbot.services.llm import generate_response


@api_view(["GET"])
def health(request):
    return Response({"status": "working"})


@api_view(["GET"])
def test_connection(request):
    return Response({
        "message": "Hello from Django Backend!"
    })


@api_view(["POST"])
def chat(request):

    user_message = request.data.get("message")

    return Response({
        "response": f"You said: {user_message}"
    })


@api_view(["GET"])
def test_llm(request):

    try:

        response = generate_response(
            "Say hello in one short sentence."
        )

        return Response({
            "success": True,
            "response": response
        })

    except Exception as e:

        return Response({
            "success": False,
            "error": str(e)
        })