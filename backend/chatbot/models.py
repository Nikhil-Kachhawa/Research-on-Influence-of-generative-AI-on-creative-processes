from django.db import models
import uuid


class ExperimentCondition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChatSession(models.Model):
    session_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.session_id)


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Message {self.id}"