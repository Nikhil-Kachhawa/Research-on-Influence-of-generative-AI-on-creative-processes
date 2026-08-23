import json
import logging

from chatbot.services.llm import generate_response

logger = logging.getLogger(__name__)


def build_conversation(session):
    """
    Convert one chat session into plain text.
    """

    conversation = ""

    messages = session.messages.order_by("created_at")

    for msg in messages:

        conversation += f"""
User:
{msg.user_message}

Assistant:
{msg.ai_response}

"""

    return conversation


def build_prompt(session, conversation):

    return f"""
You are an expert researcher analysing brainstorming conversations.

Analyse ONLY this participant conversation.

Your task is to identify ONLY research ideas that the participant
actually accepted, explored, or developed.

Ignore:

- greetings
- assistant introductions
- rejected ideas
- ideas the participant clearly declined
- spelling mistakes
- assistant examples that were never discussed further

Language rules:

- Detect the primary language used by the participant.
- Write final_research_question in the participant's primary language.
- Write accepted_ideas in the participant's primary language.
- If the conversation mixes German and English, preserve the language
  used by the participant when describing each idea.
- Do not translate everything into English unless the participant
  mainly used English.

Return ONLY valid JSON.

Schema:

{{
    "final_research_question": "",

    "accepted_ideas":[
        "idea 1",
        "idea 2",
        "idea 3"
    ]
}}

Rules:

- accepted_ideas must contain ONLY ideas accepted or explored.
- Do NOT include rejected ideas.
- Do NOT include duplicate ideas.
- Do NOT explain.
- Return JSON only.

Conversation:

{conversation}
"""

def extract_ideas(session):

    conversation = build_conversation(session)

    prompt = build_prompt(
        session,
        conversation,
    )

    response = generate_response(
        [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
        max_tokens=1800,
        max_retries=3,
        retry_delay=10,
    )

    print("=" * 80)
    print(f"Participant {session.participant.participant_number}")
    print(response)
    print("=" * 80)

    return json.loads(response)