from django.contrib import admin

from .models import (
    ExperimentCondition,
    ChatSession,
    ChatMessage
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
        "condition",
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