######################################### IDEA CLUSTER ####################################
import json
import logging

from chatbot.models import (
    ChatSession,
    ConversationAnalysis,
    IdeaCluster,
    ClusterIdea,
)


def get_interaction_order(session):
    """
    Returns the interaction order (1 or 2)
    for this participant's session.
    """

    sessions = (
        ChatSession.objects
        .filter(participant=session.participant)
        .order_by("created_at")
    )

    for index, s in enumerate(sessions, start=1):
        if s.id == session.id:
            return index

    return 1

from chatbot.services.llm import generate_response

logger = logging.getLogger(__name__)


def build_conversation(session):
    """
    Build the conversation from one session only.
    """

    messages = session.messages.order_by("created_at")

    conversation = ""

    for msg in messages:

        conversation += f"""
User:
{msg.user_message}

Assistant:
{msg.ai_response}

"""

    return conversation


def build_prompt(session, conversation):

    role = session.condition.name
    participant = session.participant
    interaction = get_interaction_order(session)

    return f"""
You are an expert researcher analysing brainstorming conversations.

Participant:
P{participant.participant_number:03d}

Session ID:
{session.session_id}

Agent Condition:
{role}

Interaction Order:
{interaction}

Analyse ONLY this conversation.

Return ONLY valid JSON.

Schema:

{{
    "final_research_question": "",

    "clusters":[
        {{
            "cluster_name":"",
            "ideas":[]
        }}
    ]
}}

Rules:

1. Ignore greetings.
2. Ignore small talk.
3. Ignore spelling mistakes.
4. Group only RESEARCH IDEAS.
5. Similar ideas belong to one cluster.
6. Every idea belongs to exactly one cluster.
7. Each idea should be concise.
8. The final research question should represent the final outcome of the discussion.
9. Return JSON only.
10.Do not include ideas or cluster_name like "Sorry, an error occured while generating a response.".


Conversation:

{conversation}
"""


def analyze_session(session):

    conversation = build_conversation(session)

    prompt = build_prompt(session, conversation)

    response = generate_response([
        {
            "role": "user",
            "content": prompt,
        }
    ])

    print(response)

    try:
        data = json.loads(response)
    except Exception as e:
        print("JSON ERROR")
        print(response)
        raise

    return data

def generate_cluster_name(ideas):
    """
    Generate a short academic topic label for one cluster.
    """

    prompt = f"""
You are an expert researcher.

Below are research ideas that belong to ONE cluster.

Ideas:

{chr(10).join("- " + idea for idea in ideas)}

Give ONE short academic topic label.

Rules:

- Maximum 4 words.
- Prefer 2–3 words.
- No full sentences.
- No punctuation.
- No quotation marks.
- No explanation.

Good examples:

Recommendation Systems
AI in Education
Student Motivation
Explainable AI
Trust in AI
Music Recommendation
Educational Technology
Digital Learning
Federated Learning
Social Media Analysis

Return ONLY the topic label.
"""

    response = generate_response([
        {
            "role": "user",
            "content": prompt,
        }
    ])

    return response.strip()

def save_analysis(session):

    ConversationAnalysis.objects.filter(
        session=session
    ).delete()

    print("=" * 80)
    print(f"Starting analysis for session {session.id}")
    print(f"Participant: {session.participant.participant_number}")
    print(f"Role: {session.condition.name}")

    data = analyze_session(session)

    print("Analysis completed successfully")
    print("=" * 80)

    clusters = data.get("clusters", [])

    cluster_count = len(clusters)

    total_ideas = sum(
        len(cluster.get("ideas", []))
        for cluster in clusters
    )

    mean_ideas = (
        total_ideas / cluster_count
        if cluster_count else 0
    )

    analysis = ConversationAnalysis.objects.create(

        session=session,

        participant=session.participant,

        agent_condition=session.condition,

        role=session.condition.name,

        interaction_order=get_interaction_order(session),

        final_research_question=data.get(
            "final_research_question",
            ""
        ),

        cluster_count=cluster_count,

        mean_ideas_per_cluster=mean_ideas,
    )

    for index, cluster_data in enumerate(clusters, start=1):

        print(f"Saving cluster {index}")
        print(f"Cluster name from LLM: {cluster_data['cluster_name']}")
        print(f"Ideas: {cluster_data['ideas']}")

        cluster_name = generate_cluster_name(
        cluster_data["ideas"]
        )

        print(f"Generated short name: {cluster_name}")

        cluster = IdeaCluster.objects.create(
            analysis=analysis,
            cluster_number=index,
            cluster_name=cluster_name,
            idea_count=len(cluster_data["ideas"]),
        )

        print(f"Cluster {index} saved with database ID: {cluster.id}")

        for idea in cluster_data["ideas"]:

            print(f"Saving idea: {idea}")

            ClusterIdea.objects.create(
                cluster=cluster,
                idea_text=idea,
            )

            print("Idea saved successfully.")

    return analysis