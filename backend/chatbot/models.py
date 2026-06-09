from django.db import models


class ExperimentCondition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100)

    condition = models.ForeignKey(
        ExperimentCondition,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_id


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)