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
        "role",
        "short_user_message",
        "created_at",
        "ai_response",
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
        return obj.user_message[:80]

    short_user_message.short_description = "User Message"