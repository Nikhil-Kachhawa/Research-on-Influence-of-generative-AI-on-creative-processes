import os

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# print("HF_TOKEN:", os.getenv("HF_TOKEN")) #testing of token

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

def generate_response(prompt):

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(e)
        return str(e)