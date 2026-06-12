from rest_framework.response import Response
from rest_framework.decorators import api_view

from chatbot.services.llm import generate_response
from chatbot.prompts import (
    IDEA_GENERATOR_PROMPT,
    CRITICAL_EVALUATOR_PROMPT
)


@api_view(["GET"])
def health(request):
    return Response({
        "status": "working"
    })


@api_view(["POST"])
def chat(request):

    role = request.data.get("role")
    user_message = request.data.get("message")

    if role == "idea-generator":

        final_prompt = f"""
        {IDEA_GENERATOR_PROMPT}

        User Request:

        {user_message}
        """

    else:

        final_prompt = f"""
        {CRITICAL_EVALUATOR_PROMPT}

        User Thesis Idea:

        {user_message}
        """

    ai_response = generate_response(final_prompt)

    return Response({
        "response": ai_response
    })