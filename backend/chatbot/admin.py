from django.contrib import admin
from django.db.models import Count

from .models import (
    Participant,
    ExperimentCondition,
    ChatSession,
    ChatMessage,
    ConversationAnalysis,
    IdeaCluster,
    ClusterIdea,
)


# =====================================================
# CHAT MESSAGE INLINE
# =====================================================

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0

    can_delete = False

    readonly_fields = (
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

    fields = (
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

    show_change_link = True


# =====================================================
# CHAT SESSION INLINE
# =====================================================

class ChatSessionInline(admin.TabularInline):
    model = ChatSession

    extra = 0

    can_delete = False

    show_change_link = True

    readonly_fields = (
        "session_id",
        "condition",
        "total_messages",
        "created_at",
    )

    fields = (
        "session_id",
        "condition",
        "total_messages",
        "created_at",
    )


# =====================================================
# PARTICIPANT
# =====================================================

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    inlines = [
        ChatSessionInline,
    ]

    list_display = (
        "id",
        "participant_number",
        "participant_id",

        "first_condition",
        "second_condition",
        "current_condition",

        "experiment_phase",

        "chat_1_started_at",
        "chat_1_finished_at",

        "survey_1_started_at",
        "survey_1_finished_at",

        "chat_2_started_at",
        "chat_2_finished_at",

        "survey_2_started_at",
        "survey_2_finished_at",

        "chat_session_count",
        "message_count",

        "started_at",
        "finished_at",

        "duration",
    )

    readonly_fields = (

        "participant_number",
        "participant_id",

        "first_condition",
        "second_condition",
        "current_condition",

        "experiment_phase",

        "chat_1_started_at",
        "chat_1_finished_at",

        "survey_1_started_at",
        "survey_1_finished_at",

        "chat_2_started_at",
        "chat_2_finished_at",

        "survey_2_started_at",
        "survey_2_finished_at",

        "started_at",
        "finished_at",

        "chat_session_count",
        "message_count",

        "duration",
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

    fieldsets = (

        (
            "Participant Information",
            {
                "fields": (
                    "participant_number",
                    "participant_id",
                )
            },
        ),

        (
            "Experiment Configuration",
            {
                "fields": (
                    "first_condition",
                    "second_condition",
                    "current_condition",
                    "experiment_phase",
                )
            },
        ),
                (
            "Chat 1",
            {
                "fields": (
                    "chat_1_started_at",
                    "chat_1_finished_at",
                )
            },
        ),

        (
            "Survey 1",
            {
                "fields": (
                    "survey_1_started_at",
                    "survey_1_finished_at",
                )
            },
        ),

        (
            "Chat 2",
            {
                "fields": (
                    "chat_2_started_at",
                    "chat_2_finished_at",
                )
            },
        ),

        (
            "Survey 2",
            {
                "fields": (
                    "survey_2_started_at",
                    "survey_2_finished_at",
                )
            },
        ),

        (
            "Experiment Summary",
            {
                "fields": (
                    "started_at",
                    "finished_at",
                    "chat_session_count",
                    "message_count",
                    "duration",
                )
            },
        ),

    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(
            session_count=Count(
                "sessions",
                distinct=True,
            ),
            total_messages=Count(
                "sessions__messages",
                distinct=True,
            ),
        )

    @admin.display(
        description="Sessions",
        ordering="session_count",
    )
    def chat_session_count(self, obj):
        return obj.session_count

    @admin.display(
        description="Messages",
        ordering="total_messages",
    )
    def message_count(self, obj):
        return obj.total_messages

    @admin.display(description="Duration")
    def duration(self, obj):

        if obj.started_at and obj.finished_at:

            delta = obj.finished_at - obj.started_at

            return str(delta).split(".")[0]

        return "-"

# =====================================================
# EXPERIMENT CONDITION
# =====================================================

@admin.register(ExperimentCondition)
class ExperimentConditionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    readonly_fields = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "id",
    )

# =====================================================
# CHAT SESSION
# =====================================================

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    inlines = [
        ChatMessageInline,
    ]

    list_display = (
        "id",
        "participant_number",
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
        "participant__participant_id",
        "session_id",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Participant",
            {
                "fields": (
                    "participant",
                )
            },
        ),

        (
            "Session Information",
            {
                "fields": (
                    "session_id",
                    "condition",
                    "total_messages",
                )
            },
        ),

        (
            "Timestamp",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    @admin.display(description="Participant Number")
    def participant_number(self, obj):

        if obj.participant:
            return obj.participant.participant_number

        return "-"

# =====================================================
# CHAT MESSAGE
# =====================================================

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "participant_number",
        "condition",
        "session_id_short",
        "role",
        "short_user_message",
        "short_ai_response",
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
        "session__participant__participant_id",
        "user_message",
        "ai_response",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Participant Information",
            {
                "fields": (
                    "session",
                    "role",
                )
            },
        ),

        (
            "Conversation",
            {
                "fields": (
                    "user_message",
                    "ai_response",
                )
            },
        ),

        (
            "Engagement Analytics",
            {
                "fields": (
                    "engagement_estimation",
                    "actual_engagement",
                    "predicted_engagement",
                    "predicted_reading_estimation",
                )
            },
        ),

        (
            "Performance",
            {
                "fields": (
                    "response_time_ms",
                    "created_at",
                )
            },
        ),

    )

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
    def session_id_short(self, obj):

        if obj.session:
            return str(obj.session.session_id)[:8]

        return "-"

    @admin.display(description="User Message")
    def short_user_message(self, obj):

        if not obj.user_message:
            return "-"

        if len(obj.user_message) > 100:
            return obj.user_message[:100] + "..."

        return obj.user_message

    @admin.display(description="AI Response")
    def short_ai_response(self, obj):

        if not obj.ai_response:
            return "-"

        if len(obj.ai_response) > 100:
            return obj.ai_response[:100] + "..."

        return obj.ai_response
            
# =====================================================
# CLUSTER IDEA INLINE
# =====================================================

class ClusterIdeaInline(admin.TabularInline):

    model = ClusterIdea

    extra = 0

    can_delete = False

    show_change_link = True

    readonly_fields = (
        "idea_text",
    )

    fields = (
        "idea_text",
    )            


    # =====================================================
# IDEA CLUSTER INLINE
# =====================================================

class IdeaClusterInline(admin.TabularInline):

    model = IdeaCluster

    extra = 0

    can_delete = False

    show_change_link = True

    readonly_fields = (
        "cluster_number",
        "cluster_name",
        "idea_count",
    )

    fields = (
        "cluster_number",
        "cluster_name",
        "idea_count",
    )

    # =====================================================
# CONVERSATION ANALYSIS
# =====================================================

@admin.register(ConversationAnalysis)
class ConversationAnalysisAdmin(admin.ModelAdmin):

    inlines = [
        IdeaClusterInline,
    ]

    list_display = (
        "id",
        "participant",
        "session",
        "agent_condition",
        "role",
        "interaction_order",
        "cluster_count",
        "mean_ideas_per_cluster",
        "created_at",
    )

    readonly_fields = (
        "participant",
        "session",
        "agent_condition",
        "role",
        "interaction_order",
        "final_research_question",
        "cluster_count",
        "mean_ideas_per_cluster",
        "created_at",
    )

    list_filter = (
        "agent_condition",
        "role",
        "created_at",
    )

    search_fields = (
        "participant__participant_number",
        "final_research_question",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Participant",
            {
                "fields": (
                    "participant",
                    "session",
                )
            },
        ),

        (
            "Agent",
            {
                "fields": (
                    "agent_condition",
                    "role",
                    "interaction_order",
                )
            },
        ),

        (
            "Research Output",
            {
                "fields": (
                    "final_research_question",
                )
            },
        ),

        (
            "Statistics",
            {
                "fields": (
                    "cluster_count",
                    "mean_ideas_per_cluster",
                )
            },
        ),

        (
            "Timestamp",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    # =====================================================
# IDEA CLUSTER
# =====================================================

@admin.register(IdeaCluster)
class IdeaClusterAdmin(admin.ModelAdmin):

    inlines = [
        ClusterIdeaInline,
    ]

    list_display = (
        "id",
        "analysis",
        "cluster_number",
        "cluster_name",
        "idea_count",
    )

    readonly_fields = (
        "analysis",
        "cluster_number",
        "cluster_name",
        "idea_count",
    )

    search_fields = (
        "cluster_name",
    )

    ordering = (
        "cluster_number",
    )

    fieldsets = (

        (
            "Cluster",
            {
                "fields": (
                    "analysis",
                    "cluster_number",
                    "cluster_name",
                    "idea_count",
                )
            },
        ),

    )


    # =====================================================
# CLUSTER IDEA
# =====================================================

@admin.register(ClusterIdea)
class ClusterIdeaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cluster",
        "idea_text",
    )

    readonly_fields = (
        "cluster",
        "idea_text",
    )

    search_fields = (
        "idea_text",
    )

    ordering = (
        "id",
    )

    fieldsets = (

        (
            "Idea",
            {
                "fields": (
                    "cluster",
                    "idea_text",
                )
            },
        ),

    )