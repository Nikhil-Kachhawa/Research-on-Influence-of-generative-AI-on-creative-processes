import os
import logging

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct:groq"

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)


def generate_response(prompt: str):

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=1200,
        )

        return (
            completion.choices[0]
            .message
            .content
            .strip()
        )

    except Exception:
        logger.exception("LLM generation failed")

        return (
            "Sorry, an error occurred while generating a response."
        )