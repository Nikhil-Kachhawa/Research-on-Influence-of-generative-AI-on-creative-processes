from django.db import models
import uuid


class ExperimentCondition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Participant(models.Model):

    participant_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    assigned_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="participants"
    )

    pre_survey_completed = models.BooleanField(
        default=False
    )

    post_survey_completed = models.BooleanField(
        default=False
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.participant_id)

class ChatSession(models.Model):

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="sessions",
        null=True,
        blank=True
    )

    session_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE
    )

    total_messages = models.IntegerField(
        default=0
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

    role = models.CharField(
        max_length=30
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Message {self.id}"
    
   