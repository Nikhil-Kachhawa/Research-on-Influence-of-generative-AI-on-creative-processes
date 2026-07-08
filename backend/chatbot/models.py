from django.db import models
import uuid


class ExperimentCondition(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Participant(models.Model):

    PHASE_CHOICES = [
        ("chat_1", "Chat 1"),
        ("survey_1", "Survey 1"),
        ("chat_2", "Chat 2"),
        ("survey_2", "Survey 2"),
        ("completed", "Completed"),
    ]

    chat_1_started_at = models.DateTimeField(null=True, blank=True)
    chat_1_finished_at = models.DateTimeField(null=True, blank=True)

    survey_1_started_at = models.DateTimeField(null=True, blank=True)
    survey_1_finished_at = models.DateTimeField(null=True, blank=True)

    chat_2_started_at = models.DateTimeField(null=True, blank=True)
    chat_2_finished_at = models.DateTimeField(null=True, blank=True)

    survey_2_started_at = models.DateTimeField(null=True, blank=True)
    survey_2_finished_at = models.DateTimeField(null=True, blank=True)

    participant_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    participant_number = models.PositiveIntegerField(
        unique=True,
        db_index=True,
    )

    first_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="first_condition_participants",
    )

    second_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="second_condition_participants",
    )

    current_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
        related_name="current_condition_participants",
    )

    experiment_phase = models.CharField(
        max_length=20,
        choices=PHASE_CHOICES,
        default="chat_1",
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["participant_number"]

    def __str__(self):
        return f"P{self.participant_number:03d}"


class ChatSession(models.Model):

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="sessions",
        null=True,
        blank=True,
    )

    session_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
    )

    total_messages = models.IntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return str(self.session_id)


class ChatMessage(models.Model):

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    role = models.CharField(
        max_length=30,
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    engagement_estimation = models.FloatField(default=0.0)

    actual_engagement = models.FloatField(default=0.0)

    predicted_engagement = models.FloatField(default=0.0)

    predicted_reading_estimation = models.FloatField(default=0.0)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    response_time_ms = models.IntegerField(
        default=0,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.id}"


class ConversationAnalysis(models.Model):

    session = models.OneToOneField(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="analysis",
    )

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )

    agent_condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE,
    )

    role = models.CharField(
    max_length=50,
    )

    interaction_order = models.IntegerField()

    final_research_question = models.TextField()

    cluster_count = models.IntegerField(default=0)

    mean_ideas_per_cluster = models.FloatField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"P{self.participant.participant_number:03d} - "
            f"{self.agent_condition.name}"
        )
    

class IdeaCluster(models.Model):

    analysis = models.ForeignKey(
        ConversationAnalysis,
        on_delete=models.CASCADE,
        related_name="clusters"
    )

    cluster_number = models.IntegerField()

    cluster_name = models.CharField(max_length=255)

    idea_count = models.IntegerField()


class ClusterIdea(models.Model):

    cluster = models.ForeignKey(
        IdeaCluster,
        on_delete=models.CASCADE,
        related_name="ideas"
    )

    idea_text = models.TextField()
