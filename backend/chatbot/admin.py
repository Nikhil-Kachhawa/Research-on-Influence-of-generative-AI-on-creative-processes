from django.contrib import admin

from .models import (
    Participant,
    ExperimentCondition,
    ChatSession,
    ChatMessage,
)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = (
        "participant_number",
        "participant_id",
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

    ordering = (
        "-participant_number",
    )


@admin.register(ExperimentCondition)
class ExperimentConditionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "session_id",
        "participant",
        "condition",
        "total_messages",
        "created_at",
    )

    list_filter = (
        "condition",
        "created_at",
    )

    search_fields = (
        "session_id",
    )

    ordering = (
        "-created_at",
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "session",
        "role",
        "short_user_message",
        "response_time_ms",
        "created_at",
    )

    list_filter = (
        "role",
        "created_at",
    )

    search_fields = (
        "user_message",
        "ai_response",
    )

    ordering = (
        "-created_at",
    )

    def short_user_message(self, obj):
        return (
            obj.user_message[:80] + "..."
            if len(obj.user_message) > 80
            else obj.user_message
        )

    short_user_message.short_description = "User Message"