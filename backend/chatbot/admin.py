from django.contrib import admin
from django.db.models import Count

from .models import (
    Participant,
    ExperimentCondition,
    ChatSession,
    ChatMessage,
)

# -------------------------------------------------------
# Participant
# -------------------------------------------------------


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "participant_number",
        "participant_id",
        "first_condition",
        "second_condition",
        "current_condition",
        "experiment_phase",
        "started_at",
        "finished_at",
    )

    readonly_fields = (
        "participant_id",
        "participant_number",
        "first_condition",
        "second_condition",
        "current_condition",
        "experiment_phase",
        "started_at",
        "finished_at",
    )

    list_filter = (
        "experiment_phase",
        "first_condition",
        "second_condition",
        "current_condition",
    )

    search_fields = (
        "participant_number",
        "participant_id",
    )

    ordering = ("-participant_number",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            session_count=Count("sessions", distinct=True),
            total_messages=Count("sessions__messages", distinct=True),
        )

    @admin.display(description="Sessions", ordering="session_count")
    def chat_session_count(self, obj):
        return obj.session_count

    @admin.display(description="Messages", ordering="total_messages")
    def message_count(self, obj):
        return obj.total_messages

    @admin.display(description="Duration")
    def duration(self, obj):
        if obj.started_at and obj.finished_at:
            delta = obj.finished_at - obj.started_at
            return str(delta).split(".")[0]
        return "-"


# -------------------------------------------------------
# Experiment Condition
# -------------------------------------------------------


@admin.register(ExperimentCondition)
class ExperimentConditionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = ("name",)


# -------------------------------------------------------
# Chat Session
# -------------------------------------------------------


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "participant",
        "session_id",
        "condition",
        "total_messages",
        "created_at",
    )

    readonly_fields = (
        "participant",
        "session_id",
        "condition",
        "total_messages",
        "created_at",
    )

    list_filter = (
        "condition",
        "created_at",
    )

    search_fields = (
        "participant__participant_number",
        "session_id",
    )

    ordering = ("-created_at",)

    @admin.display(description="Participant")
    def participant_number(self, obj):
        return obj.participant.participant_number


# -------------------------------------------------------
# Chat Message
# -------------------------------------------------------

@admin.display(description="Participant")
def participant_number(self, obj):
    if obj.session and obj.session.participant:
        return obj.session.participant.participant_number
    return "-"


@admin.display(description="Condition")
def condition(self, obj):
    if obj.session:
        return obj.session.condition
    return "-"


@admin.display(description="Session ID")
def session_id(self, obj):
    if obj.session:
        return obj.session.session_id
    return "-"

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "participant_number",
        "session",
        "role",
        "user_message",
        "ai_response",
        "engagement_estimation",
        "actual_engagement",
        "predicted_engagement",
        "predicted_reading_estimation",
        "response_time_ms",
        "created_at",
    )

    readonly_fields = (
        "session",
        "role",
        "user_message",
        "ai_response",
        "engagement_estimation",
        "actual_engagement",
        "predicted_engagement",
        "predicted_reading_estimation",
        "response_time_ms",
        "created_at",
    )

    list_filter = (
        "role",
        "session__condition",
        "created_at",
    )

    search_fields = (
        "session__participant__participant_number",
        "user_message",
        "ai_response",
    )

    ordering = ("-created_at",)

    @admin.display(description="Participant")
    def participant_number(self, obj):
        return obj.session.participant.participant_number

    @admin.display(description="Condition")
    def condition(self, obj):
        return obj.session.condition

    @admin.display(description="User Message")
    def short_user_message(self, obj):
        if not obj.user_message:
            return "-"
        return (
            obj.user_message[:80] + "..."
            if len(obj.user_message) > 80
            else obj.user_message
        )
