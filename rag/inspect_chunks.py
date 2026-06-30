import json

with open(
    "data/gdpr_chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

for chunk in chunks[:5]:

    print("=" * 50)

    print(chunk["article"])

    print(chunk["content"][:500])

    print()