from django.contrib import admin
from .models import (
    ExperimentCondition,
    ChatSession,
    ChatMessage
)

admin.site.register(ExperimentCondition)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)