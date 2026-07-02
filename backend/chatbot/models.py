from django.db import models
import uuid


class ExperimentCondition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Participant(models.Model):

    participant_number = models.PositiveIntegerField(
        unique=True
    )

    first_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="first_condition_participants"
    )

    second_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="second_condition_participants"
    )

    current_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="current_condition_participants"
    )

    first_chat_completed = models.BooleanField(
        default=False
    )

    second_chat_completed = models.BooleanField(
        default=False
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
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

    engagement_estimation = models.FloatField(default=0.0)
    actual_engagement = models.FloatField(default=0.0)
    predicted_engagement = models.FloatField(default=0.0)
    predicted_reading_estimation = models.FloatField(default=0.0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    response_time_ms = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"Message {self.id}"
    
   
