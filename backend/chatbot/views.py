from rest_framework.response import Response
from rest_framework.decorators import api_view

from chatbot.services.llm import generate_response
from chatbot.prompts import (
    IDEA_GENERATOR_PROMPT,
    CRITICAL_EVALUATOR_PROMPT
)

from .models import (
    ChatSession,
    ChatMessage,
    ExperimentCondition
)

@api_view(["GET"])
def health(request):
    return Response({
        "status": "working"
    })

@api_view(["GET"])
def chat_history(request, session_id):

    try:
        session = ChatSession.objects.get(
            session_id=session_id
        )

    except ChatSession.DoesNotExist:
        return Response(
            {"messages": []}
        )

    messages = ChatMessage.objects.filter(
        session=session
    ).order_by("created_at")

    data = []

    for msg in messages:

        data.append({
            "user_message": msg.user_message,
            "ai_response": msg.ai_response,
            "created_at": msg.created_at
        })

    return Response({
        "messages": data
    })

@api_view(["POST"])
def chat(request):

    role = request.data.get("role")
    user_message = request.data.get("message")
    session_id = request.data.get("session_id")

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

    condition, _ = ExperimentCondition.objects.get_or_create(
        name=role
    )

    session, _ = ChatSession.objects.get_or_create(
        session_id=session_id,
        defaults={
            "condition": condition
        }
    )

    ChatMessage.objects.create(
        session=session,
        role=role,
        user_message=user_message,
        ai_response=ai_response
    )

    return Response({
        "response": ai_response
    })