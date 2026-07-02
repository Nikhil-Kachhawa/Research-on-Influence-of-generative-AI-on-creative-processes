import logging
import random
import time

from django.db.models import Max
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from chatbot.prompts import (
    IDEA_GENERATOR_PROMPT,
    CRITICAL_EVALUATOR_PROMPT,
)
from chatbot.services.knowledge import get_context
from chatbot.services.llm import generate_response

from .models import (
    ChatMessage,
    ChatSession,
    ExperimentCondition,
    Participant,
)

logger = logging.getLogger(__name__)


@api_view(["GET"])
def health(request):
    return Response({"status": "working"})


@api_view(["POST"])
def start_experiment(request):

    next_number = (
        Participant.objects.aggregate(Max("participant_number"))[
            "participant_number__max"
        ]
        or 0
    ) + 1

    idea_generator, _ = ExperimentCondition.objects.get_or_create(name="idea-generator")

    critical_evaluator, _ = ExperimentCondition.objects.get_or_create(
        name="critical-evaluator"
    )

    if random.choice([True, False]):
        first_condition = idea_generator
        second_condition = critical_evaluator
    else:
        first_condition = critical_evaluator
        second_condition = idea_generator

    participant = Participant.objects.create(
        participant_number=next_number,
        first_condition=first_condition,
        second_condition=second_condition,
        current_condition=first_condition,
        experiment_phase="chat_1",
    )

    session = ChatSession.objects.create(
        participant=participant,
        condition=participant.current_condition,
    )

    return Response(
        {
            "participant_id": str(participant.participant_id),
            "participant_number": f"{participant.participant_number:03d}",
            "current_role": participant.current_condition.name,
            "session_id": str(session.session_id),
            "experiment_phase": participant.experiment_phase,
        }
    )


@api_view(["POST"])
def continue_experiment(request):

    participant_id = request.data.get("participant_id")

    if not participant_id:
        return Response(
            {"error": "Participant ID is required."},
            status=400,
        )

    try:
        participant = Participant.objects.get(participant_id=participant_id)

    except Participant.DoesNotExist:
        return Response(
            {"error": "Participant not found."},
            status=404,
        )

    # -----------------------------
    # Survey 1 -> Chat 2
    # -----------------------------
    if participant.experiment_phase == "survey_1":

        participant.current_condition = participant.second_condition
        participant.experiment_phase = "chat_2"
        participant.save()
        session = ChatSession.objects.create(
            participant=participant,
            condition=participant.current_condition,
        )
        return Response(
            {
                "participant_number": f"{participant.participant_number:03d}",
                "current_role": participant.current_condition.name,
                "session_id": str(session.session_id),
                "experiment_phase": participant.experiment_phase,
            }
        )

    # -----------------------------
    # Already moved to Chat 2
    # (duplicate request)
    # -----------------------------
    if participant.experiment_phase == "chat_2":

        return Response(
            {
                "participant_number": f"{participant.participant_number:03d}",
                "current_role": participant.current_condition.name,
                "experiment_phase": participant.experiment_phase,
            }
        )

    # -----------------------------
    # Survey 2 -> Completed
    # -----------------------------
    if participant.experiment_phase == "survey_2":

        participant.experiment_phase = "completed"
        participant.finished_at = timezone.now()
        participant.save()

        return Response({"status": "completed"})

    # -----------------------------
    # Already completed
    # -----------------------------
    if participant.experiment_phase == "completed":

        return Response({"status": "completed"})

    return Response(
        {"error": "Invalid experiment state."},
        status=400,
    )


@api_view(["GET"])
def chat_history(request, session_id):

    try:
        session = ChatSession.objects.get(session_id=session_id)

    except ChatSession.DoesNotExist:
        return Response({"messages": []})

    messages = ChatMessage.objects.filter(session=session).order_by("created_at")

    data = []

    for msg in messages:

        data.append(
            {
                "id": msg.id,
                "user_message": msg.user_message,
                "ai_response": msg.ai_response,
                "created_at": msg.created_at,
            }
        )

    return Response({"messages": data})


@api_view(["POST"])
def attentionPrediction(request):
    try:
        message = ChatMessage.objects.get(id=request.data.get("response_id"))
        logger.info("Chat message accessed: %s", message.id)
    except ChatMessage.DoesNotExist:
        logger.error("Error accessing chatmessage: %s", request.data.get("response_id"))
        return Response({"error": "Participant not found"}, status=404)

    word_count = len(message.ai_response.split())
    avg_reading_speed = 200
    message.actual_engagement = request.data.get("actual_engagement")
    message.engagement_estimation = (word_count / avg_reading_speed) * 60
    message.predicted_engagement = request.data.get("predicted_engagement")
    message.predicted_reading_estimation = (
        request.data.get("predicted_engagement") / message.engagement_estimation
    )

    message.save()
    logger.info("chat message analytics updated: %s", message.id)
    return Response({"success": True})


@api_view(["POST"])
def chat(request):

    start_time = time.time()

    user_message = request.data.get("message")
    session_id = request.data.get("session_id")
    participant_id = request.data.get("participant_id")

    if not user_message:
        return Response({"error": "Message is required."}, status=400)

    if not participant_id:
        return Response({"error": "Participant ID is required."}, status=400)

    if not session_id:
        return Response({"error": "Session ID is required."}, status=400)

    try:
        participant = Participant.objects.get(participant_id=participant_id)

    except Participant.DoesNotExist:
        return Response({"error": "Participant not found"}, status=404)

    if participant.experiment_phase not in ("chat_1", "chat_2"):
        return Response(
            {"error": "Chat is not available in the current experiment phase."},
            status=403,
        )

    role = participant.current_condition.name

    session, _ = ChatSession.objects.get_or_create(
        session_id=session_id,
        defaults={
            "condition": participant.current_condition,
            "participant": participant,
        },
    )

    previous_messages = ChatMessage.objects.filter(session=session).order_by(
        "created_at"
    )

    context = get_context(user_message)

    base_prompt = (
        IDEA_GENERATOR_PROMPT if role == "idea-generator" else CRITICAL_EVALUATOR_PROMPT
    )

    if context:
        system_content = (
            f"{base_prompt}\n\n"
            f"=== University of Koblenz — FB4 Research Context ===\n"
            f"The following is real information about faculty, research projects, "
            f"and thesis topics at the University of Koblenz Computer Science "
            f"department. Use it to ground your suggestions in the department's "
            f"actual research areas:\n\n"
            f"{context}\n"
            f"====================================================="
        )
    else:
        system_content = base_prompt

    messages = [{"role": "system", "content": system_content}]

    for msg in previous_messages:

        messages.append({"role": "user", "content": msg.user_message})

        messages.append({"role": "assistant", "content": msg.ai_response})

    messages.append({"role": "user", "content": user_message})

    ai_response = generate_response(messages)

    response_time_ms = int((time.time() - start_time) * 1000)

    saved_message = ChatMessage.objects.create(
        session=session,
        role=role,
        user_message=user_message,
        ai_response=ai_response,
        response_time_ms=response_time_ms,
    )

    session.total_messages += 1
    session.save(update_fields=["total_messages"])

    return Response(
        {
            "response": ai_response,
            "response_id": saved_message.id,
        }
    )


@api_view(["POST"])
def finish_chat(request):

    participant_id = request.data.get("participant_id")

    if not participant_id:
        return Response(
            {"error": "Participant ID is required."},
            status=400,
        )

    try:
        participant = Participant.objects.get(participant_id=participant_id)

    except Participant.DoesNotExist:
        return Response(
            {"error": "Participant not found."},
            status=404,
        )

    if participant.experiment_phase == "chat_1":

        participant.experiment_phase = "survey_1"
        participant.save()

        return Response(
            {
                "next_step": "survey_1",
                "participant_number": f"{participant.participant_number:03d}",
                "role": participant.current_condition.name,
            }
        )

    elif participant.experiment_phase == "chat_2":

        participant.experiment_phase = "survey_2"
        participant.save()

        return Response(
            {
                "next_step": "survey_2",
                "participant_number": f"{participant.participant_number:03d}",
                "role": participant.current_condition.name,
            }
        )

    return Response(
        {"error": "Invalid experiment state."},
        status=400,
    )
