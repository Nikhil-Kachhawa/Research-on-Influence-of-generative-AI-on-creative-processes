import time
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from chatbot.models import (
    ChatSession,
    ConversationAnalysis,
    ExtractedIdea,
)

from chatbot.services.idea_extraction import extract_ideas


SUCCESS_DELAY_SECONDS = 5
FAILED_SESSION_LOG = Path("failed_extraction_sessions.txt")


def get_interaction_order(session):
    """
    Return the session order for the participant.

    First session  -> 1
    Second session -> 2
    """

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


def clean_ideas(raw_ideas):
    """
    Normalize ideas and remove case-insensitive duplicates.
    """

    if not isinstance(raw_ideas, list):
        raise ValueError(
            "'accepted_ideas' must be a JSON list."
        )

    cleaned = []
    seen = set()

    for raw_idea in raw_ideas:
        idea_text = str(raw_idea).strip()
        normalized = idea_text.casefold()

        if not idea_text or normalized in seen:
            continue

        seen.add(normalized)
        cleaned.append(idea_text)

    return cleaned


def log_failed_session(session, error):
    """
    Append permanently failed sessions to a text file.
    """

    with FAILED_SESSION_LOG.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            (
                f"participant=P"
                f"{session.participant.participant_number:03d}, "
                f"session_id={session.session_id}, "
                f"condition={session.condition.name}, "
                f"error={error}\n"
            )
        )


class Command(BaseCommand):

    help = (
        "Extract accepted ideas and final research questions "
        "from stored chat sessions."
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--force",
            action="store_true",
            help="Reprocess already completed sessions.",
        )

        parser.add_argument(
            "--session-id",
            type=str,
            help="Process only one ChatSession UUID.",
        )

        parser.add_argument(
            "--participants",
            type=str,
            help=(
                "Comma-separated participant numbers. "
                "Example: 1,3,4,5,77"
            ),
        )

        parser.add_argument(
            "--limit",
            type=int,
            help="Maximum number of sessions to process.",
        )

        parser.add_argument(
            "--delay",
            type=int,
            default=SUCCESS_DELAY_SECONDS,
            help=(
                "Seconds to wait after each processed session. "
                "Default: 5."
            ),
        )

        parser.add_argument(
            "--failed-only",
            action="store_true",
            help=(
                "Process only sessions without a complete analysis."
            ),
        )

    def handle(self, *args, **options):

        force = options["force"]
        session_uuid = options["session_id"]
        participant_numbers_raw = options["participants"]
        limit = options["limit"]
        delay = max(options["delay"], 0)
        failed_only = options["failed_only"]

        selected_participants = None

        if participant_numbers_raw:
            try:
                selected_participants = [
                    int(number.strip())
                    for number in participant_numbers_raw.split(",")
                    if number.strip()
                ]
            except ValueError as error:
                raise ValueError(
                    "--participants must contain only comma-separated "
                    "participant numbers, e.g. 1,3,4,77"
                ) from error

            if not selected_participants:
                raise ValueError(
                    "--participants was provided, but no valid "
                    "participant numbers were found."
                )

            self.stdout.write(
                self.style.SUCCESS(
                    "Filtering participants: "
                    + ", ".join(
                        f"P{number:03d}"
                        for number in selected_participants
                    )
                )
            )

        sessions = (
            ChatSession.objects
            .select_related(
                "participant",
                "condition",
            )
            .filter(
                messages__isnull=False,
            )
            .distinct()
            .order_by(
                "participant_id",
                "created_at",
                "id",
            )
        )

        if selected_participants:
            sessions = sessions.filter(
                participant__participant_number__in=selected_participants,
            )

        if session_uuid:
            sessions = sessions.filter(
                session_id=session_uuid,
            )

        if failed_only:
            sessions = sessions.filter(
                analysis__final_research_question="",
            )

        if limit:
            sessions = sessions[:limit]

        sessions = list(sessions)

        total_sessions = len(sessions)

        processed = 0
        skipped = 0
        failed = 0

        self.stdout.write(
            self.style.SUCCESS(
                f"\nFound {total_sessions} sessions.\n"
            )
        )

        for position, session in enumerate(
            sessions,
            start=1,
        ):

            self.stdout.write(
                (
                    f"\n[{position}/{total_sessions}] "
                    f"Participant "
                    f"P{session.participant.participant_number:03d} | "
                    f"Session {session.session_id} | "
                    f"Condition {session.condition.name}"
                )
            )

            existing_ideas = (
                ExtractedIdea.objects
                .filter(session=session)
            )

            existing_analysis = (
                ConversationAnalysis.objects
                .filter(session=session)
                .first()
            )

            is_complete = (
                existing_ideas.exists()
                and existing_analysis is not None
                and bool(
                    existing_analysis
                    .final_research_question
                    .strip()
                )
            )

            if is_complete and not force:
                skipped += 1

                self.stdout.write(
                    self.style.WARNING(
                        "  Already complete. Skipping."
                    )
                )

                continue

            try:
                self.stdout.write(
                    "  Calling LLM..."
                )

                data = extract_ideas(session)

                final_question = str(
                    data.get(
                        "final_research_question",
                        "",
                    )
                ).strip()

                cleaned_ideas = clean_ideas(
                    data.get(
                        "accepted_ideas",
                        [],
                    )
                )

                if cleaned_ideas and not final_question:
                    raise ValueError(
                        (
                            "Accepted ideas were returned, but "
                            "the final research question is empty."
                        )
                    )

                interaction_order = (
                    get_interaction_order(session)
                )

                with transaction.atomic():

                    analysis, created = (
                        ConversationAnalysis.objects
                        .get_or_create(
                            session=session,
                            defaults={
                                "participant": (
                                    session.participant
                                ),
                                "agent_condition": (
                                    session.condition
                                ),
                                "role": (
                                    session.condition.name
                                ),
                                "interaction_order": (
                                    interaction_order
                                ),
                                "final_research_question": (
                                    final_question
                                ),
                                "cluster_count": 0,
                                "mean_ideas_per_cluster": 0,
                            },
                        )
                    )

                    if not created:
                        analysis.participant = (
                            session.participant
                        )
                        analysis.agent_condition = (
                            session.condition
                        )
                        analysis.role = (
                            session.condition.name
                        )
                        analysis.interaction_order = (
                            interaction_order
                        )
                        analysis.final_research_question = (
                            final_question
                        )

                        analysis.save(
                            update_fields=[
                                "participant",
                                "agent_condition",
                                "role",
                                "interaction_order",
                                "final_research_question",
                            ]
                        )

                    existing_ideas.delete()

                    ExtractedIdea.objects.bulk_create(
                        [
                            ExtractedIdea(
                                participant=(
                                    session.participant
                                ),
                                session=session,
                                agent_condition=(
                                    session.condition
                                ),
                                interaction_order=(
                                    interaction_order
                                ),
                                idea_text=idea_text,
                            )
                            for idea_text in cleaned_ideas
                        ]
                    )

                processed += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        (
                            f"  Saved research question and "
                            f"{len(cleaned_ideas)} ideas."
                        )
                    )
                )

            except Exception as error:
                failed += 1

                self.stderr.write(
                    self.style.ERROR(
                        f"  Permanently failed: {error}"
                    )
                )

                log_failed_session(
                    session,
                    error,
                )

            # Wait after every session, including failed sessions.
            if position < total_sessions and delay > 0:
                self.stdout.write(
                    (
                        f"  Waiting {delay} seconds "
                        f"before the next session..."
                    )
                )

                time.sleep(delay)

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "\nExtraction finished.\n"
                    f"Processed: {processed}\n"
                    f"Skipped: {skipped}\n"
                    f"Failed: {failed}\n"
                    f"Failure log: "
                    f"{FAILED_SESSION_LOG.resolve()}\n"
                )
            )
        )