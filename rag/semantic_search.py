import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# Load embedding model
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

# Load FAISS index
index = faiss.read_index(
    "gdpr_index.faiss"
)


def search_gdpr(
    query,
    top_k=5
):
    """
    Search the GDPR knowledge base
    using semantic similarity.
    """

    query_embedding = model.encode(
        query
    )

    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i, idx in enumerate(indices[0]):

        results.append(
    {
        "article": chunks[idx]["article"],
        "content": chunks[idx]["content"],
        "distance": float(distances[0][i])
    }
)

    return results


if __name__ == "__main__":

    question = input(
        "Ask a GDPR question: "
    )

    results = search_gdpr(
        question
    )

    print("\nRelevant GDPR Articles\n")

    for result in results:

        print("=" * 60)
        print(result["article"])
        print(f"Similarity Score: {result['distance']:.4f}")
        print()
        print(result["content"][:600])
        print()