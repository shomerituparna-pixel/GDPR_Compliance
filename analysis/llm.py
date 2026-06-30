import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from config import (
    HF_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. Please check your .env file."
    )

# Initialize Hugging Face client
client = InferenceClient(
    api_key=HF_TOKEN
)


def generate_response(prompt):
    """
    Sends a prompt to the configured Hugging Face model
    and returns the generated response.
    """

    try:

        response = client.chat.completions.create(
            model=HF_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

        return response.choices[0].message.content

    except Exception as e:

        print("\nLLM Error:")
        print(e)

        return None


if __name__ == "__main__":

    print("=" * 60)
    print("Testing Hugging Face LLM")
    print("=" * 60)

    prompt = """
Reply with exactly one word:

SUCCESS
"""

    result = generate_response(prompt)

    print("\nModel Response:\n")

    print(result)

    print("\nDone!")