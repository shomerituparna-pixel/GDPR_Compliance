import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Load GDPR chunks
with open(
    "data/gdpr_chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

embeddings = []

for chunk in chunks:

    text = f"""
    {chunk['article']}
    {chunk['content']}
    """

    embedding = model.encode(text)

    embeddings.append(embedding)

embeddings = np.array(
    embeddings
).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

# Save index
faiss.write_index(
    index,
    "gdpr_index.faiss"
)

print(
    f"Indexed {len(chunks)} GDPR articles."
)