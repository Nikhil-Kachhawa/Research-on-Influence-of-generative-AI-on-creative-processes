from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone

from chatbot.services.llm import generate_response
from chatbot.prompts import (
    IDEA_GENERATOR_PROMPT,
    CRITICAL_EVALUATOR_PROMPT
)

from .models import (
    Participant,
    ChatSession,
    ChatMessage,
    ExperimentCondition
)

@api_view(["GET"])
def health(request):
    return Response({
        "status": "working"
    })

@api_view(["POST"])
def start_experiment(request):

    idea_count = Participant.objects.filter(
        assigned_condition__name="idea-generator"
    ).count()

    critical_count = Participant.objects.filter(
        assigned_condition__name="critical-evaluator"
    ).count()

    if idea_count <= critical_count:
        condition_name = "idea-generator"
    else:
        condition_name = "critical-evaluator"

    condition = ExperimentCondition.objects.get(
        name=condition_name
    )

    participant = Participant.objects.create(
        assigned_condition=condition
    )

    return Response({
        "participant_id":
            str(participant.participant_id),

        "condition":
            condition_name
    })

@api_view(["POST"])
def complete_survey(request):

    participant_id = request.data.get(
        "participant_id"
    )

    survey_type = request.data.get(
        "survey_type"
    )

    try:

        participant = Participant.objects.get(
            participant_id=participant_id
        )

    except Participant.DoesNotExist:

        return Response(
            {
                "error":
                "Participant not found"
            },
            status=404
        )

    if survey_type == "pre":

        participant.pre_survey_completed = True

    elif survey_type == "post":

        participant.post_survey_completed = True

        participant.finished_at = (
            timezone.now()
        )

    participant.save()

    return Response({
        "success": True
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

    participant_id = request.data.get(
        "participant_id"
    )

    participant = Participant.objects.get(
        participant_id=participant_id
    )

    if not participant.pre_survey_completed:

        return Response(
        {
            "error":
            "Complete survey first"
        },
        status=403
    )

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
            "condition": condition,
            "participant": participant
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

@api_view(["GET"])
def experiment_stats(request):

    return Response({

        "participants":
            Participant.objects.count(),

        "idea_generator":
            Participant.objects.filter(
                assigned_condition__name=
                "idea-generator"
            ).count(),

        "critical_evaluator":
            Participant.objects.filter(
                assigned_condition__name=
                "critical-evaluator"
            ).count(),

        "completed":
            Participant.objects.filter(
                post_survey_completed=True
            ).count()
    })

@api_view(["GET"])
def experiment_export(request):

    participants = Participant.objects.all()

    data = []

    for p in participants:

        data.append({

            "participant_id":
                str(p.participant_id),

            "condition":
                p.assigned_condition.name,

            "pre_completed":
                p.pre_survey_completed,

            "post_completed":
                p.post_survey_completed,

            "started_at":
                p.started_at,

            "finished_at":
                p.finished_at
        })

    return Response(data)