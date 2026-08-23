from collections import defaultdict

import numpy as np

from django.core.management.base import BaseCommand
from django.db import transaction

from chatbot.models import (
    ChatSession,
    ClusterIdea,
    ConversationAnalysis,
    ExtractedIdea,
    IdeaCluster,
)

from chatbot.services.cluster_interpretation import (
    build_cluster_reason,
    calculate_cluster_evidence,
    generate_local_cluster_name,
)

from chatbot.services.idea_clustering import (
    cluster_ideas,
)

from chatbot.services.idea_embeddings import (
    create_idea_embeddings,
)


def get_interaction_order(session):
    participant_sessions = (
        ChatSession.objects
        .filter(participant=session.participant)
        .order_by("created_at", "id")
    )

    for index, participant_session in enumerate(
        participant_sessions,
        start=1,
    ):
        if participant_session.id == session.id:
            return index

    return 1


class Command(BaseCommand):

    help = (
        "Cluster previously extracted accepted ideas and save "
        "participant-session analysis results."
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--session-id",
            type=str,
            help="Process one ChatSession UUID only.",
        )

        parser.add_argument(
            "--limit",
            type=int,
            help="Maximum number of sessions to process.",
        )

        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete and regenerate existing clusters.",
        )

    def handle(self, *args, **options):

        session_uuid = options.get("session_id")
        limit = options.get("limit")
        force = options.get("force", False)

        sessions = (
            ChatSession.objects
            .select_related(
                "participant",
                "condition",
            )
            .filter(
                extracted_ideas__isnull=False,
            )
            .distinct()
            .order_by("participant_id", "created_at", "id")
        )

        if session_uuid:
            sessions = sessions.filter(
                session_id=session_uuid,
            )

        if limit:
            sessions = sessions[:limit]

        total_sessions = len(sessions)

        processed = 0
        skipped = 0
        failed = 0

        self.stdout.write(
            f"\nSessions selected: {total_sessions}\n"
        )

        for position, session in enumerate(
            sessions,
            start=1,
        ):

            self.stdout.write(
                (
                    f"[{position}/{total_sessions}] "
                    f"Participant "
                    f"P{session.participant.participant_number:03d} | "
                    f"Session {session.session_id} | "
                    f"Condition {session.condition.name}"
                )
            )

            try:
                analysis, _ = (
                    ConversationAnalysis.objects.get_or_create(
                        session=session,
                        defaults={
                            "participant": session.participant,
                            "agent_condition": session.condition,
                            "role": session.condition.name,
                            "interaction_order": (
                                get_interaction_order(session)
                            ),
                            "final_research_question": "",
                            "cluster_count": 0,
                            "mean_ideas_per_cluster": 0,
                        },
                    )
                )

                if analysis.clusters.exists() and not force:
                    skipped += 1

                    self.stdout.write(
                        self.style.WARNING(
                            "  Existing clusters found; skipped."
                        )
                    )

                    continue

                idea_rows = list(
                    ExtractedIdea.objects
                    .filter(session=session)
                    .order_by("id")
                )

                idea_texts = [
                    idea.idea_text.strip()
                    for idea in idea_rows
                    if idea.idea_text.strip()
                ]

                if not idea_texts:
                    skipped += 1

                    self.stdout.write(
                        self.style.WARNING(
                            "  No accepted ideas; skipped."
                        )
                    )

                    continue

                embeddings = create_idea_embeddings(
                    idea_texts
                )

                result = cluster_ideas(
                    embeddings
                )

                grouped_indexes = defaultdict(list)

                for idea_index, label in enumerate(
                    result.labels
                ):
                    grouped_indexes[int(label)].append(
                        idea_index
                    )

                # Give clusters a stable order.
                ordered_groups = sorted(
                    grouped_indexes.values(),
                    key=lambda indexes: min(indexes),
                )

                total_ideas = len(idea_texts)
                cluster_count = len(ordered_groups)

                mean_ideas = (
                    total_ideas / cluster_count
                    if cluster_count
                    else 0
                )

                with transaction.atomic():

                    # Delete previous clusters and their ideas when
                    # --force is supplied.
                    analysis.clusters.all().delete()

                    analysis.participant = session.participant
                    analysis.agent_condition = session.condition
                    analysis.role = session.condition.name
                    analysis.interaction_order = (
                        get_interaction_order(session)
                    )
                    analysis.cluster_count = cluster_count
                    analysis.mean_ideas_per_cluster = (
                        mean_ideas
                    )

                    analysis.save(
                        update_fields=[
                            "participant",
                            "agent_condition",
                            "role",
                            "interaction_order",
                            "cluster_count",
                            "mean_ideas_per_cluster",
                        ]
                    )

                    for cluster_number, indexes in enumerate(
                        ordered_groups,
                        start=1,
                    ):

                        cluster_texts = [
                            idea_texts[index]
                            for index in indexes
                        ]

                        cluster_vectors = np.asarray(
                            [
                                embeddings[index]
                                for index in indexes
                            ]
                        )

                        similarity_scores, average_similarity = (
                            calculate_cluster_evidence(
                                cluster_vectors
                            )
                        )

                        cluster_name = (
                            generate_local_cluster_name(
                                cluster_texts,
                                cluster_number,
                            )
                        )

                        cluster_reason = build_cluster_reason(
                            cluster_texts,
                            average_similarity,
                        )

                        cluster = IdeaCluster.objects.create(
                            analysis=analysis,
                            cluster_number=cluster_number,
                            cluster_name=cluster_name,
                            cluster_reason=cluster_reason,
                            idea_count=len(cluster_texts),
                        )

                        for local_index, original_index in enumerate(
                            indexes
                        ):

                            ClusterIdea.objects.create(
                                cluster=cluster,
                                extracted_idea=idea_rows[
                                    original_index
                                ],
                                idea_text=idea_texts[
                                    original_index
                                ],
                                similarity_score=(
                                    similarity_scores[
                                        local_index
                                    ]
                                ),
                            )

                processed += 1

                score_text = (
                    f"{result.silhouette_score:.3f}"
                    if result.silhouette_score is not None
                    else "not applicable"
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        (
                            f"  Saved {cluster_count} clusters "
                            f"from {total_ideas} ideas; "
                            f"mean={mean_ideas:.2f}; "
                            f"silhouette={score_text}."
                        )
                    )
                )

            except Exception as error:
                failed += 1

                self.stderr.write(
                    self.style.ERROR(
                        f"  Failed: {error}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "\nClustering finished.\n"
                    f"Processed: {processed}\n"
                    f"Skipped: {skipped}\n"
                    f"Failed: {failed}\n"
                )
            )
        )