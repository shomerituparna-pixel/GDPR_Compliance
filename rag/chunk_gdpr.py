import json
import re

# Read GDPR text
with open(
    "data/gdpr.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

# Find where the actual GDPR articles start
start_index = text.find("CHAPTER I")

if start_index == -1:
    raise Exception(
        "Could not find 'CHAPTER I' in GDPR text."
    )

# Keep only the GDPR content
text = text[start_index:]

# Split only on article headings
articles = re.split(
    r"\nArticle\s+(\d+)\s*\n",
    text
)

chunks = []

for i in range(1, len(articles), 2):

    article_number = articles[i]

    article_content = articles[i + 1].strip()

    # Skip empty articles
    if len(article_content) < 50:
        continue

    chunks.append(
        {
            "article": f"Article {article_number}",
            "content": article_content
        }
    )

# Save chunks
with open(
    "data/gdpr_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Created {len(chunks)} GDPR article chunks."
)