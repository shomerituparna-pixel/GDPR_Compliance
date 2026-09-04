import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Import our semantic search function
from rag.semantic_search import search_gdpr

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. Please add it to your .env file."
    )

# Initialize Hugging Face client
client = InferenceClient(
    api_key=HF_TOKEN,
)


def get_gdpr_context(document_text, top_k=5):
    """
    Retrieve the most relevant GDPR articles
    for the uploaded document.
    """

    results = search_gdpr(
        document_text,
        top_k
    )

    context = ""

    for result in results:

        context += f"""
{result["article"]}

{result["content"]}

------------------------------------------------------------

"""

    return context


def build_prompt(document_text, gdpr_context):
    """
    Build the prompt sent to the LLM.
    """

    return f"""
You are an expert GDPR Compliance Officer.

Your job is to analyse the uploaded document
using ONLY the GDPR articles provided.

If information is missing,
mention that it is missing.

Do NOT make up GDPR rules.

========================================================
GDPR ARTICLES
========================================================

{gdpr_context}

========================================================
DOCUMENT
========================================================

{document_text}

========================================================

Return ONLY valid JSON in the following format:

{{
  "compliance_score": 0,
  "risk_level": "",
  "summary": "",
  "issues": [
    {{
      "article": "",
      "severity": "",
      "issue": "",
      "recommendation": ""
    }}
  ],
  "strengths": [
    ""
  ]
}}
"""


def analyze_document(document_text):
    """
    Perform GDPR compliance analysis.
    """

    gdpr_context = get_gdpr_context(
        document_text
    )

    prompt = build_prompt(
        document_text,
        gdpr_context
    )

    completion = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1500,
    )

    return completion.choices[0].message.content


# ------------------------
# Testing
# ------------------------

if __name__ == "__main__":

    sample_document = """
Our company collects customer names,
email addresses and phone numbers.

Users may request deletion of their data.

We use personal data to provide our services.

Users may withdraw consent at any time.
"""

    result = analyze_document(
        sample_document
    )

    print(result)