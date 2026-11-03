from src.chunking import load_all_chunks
from src.embeddings import load_model, make_embed_fn

chunks = load_all_chunks()
embed = make_embed_fn(load_model())
vectors = embed([chunk["text"] for chunk in chunks])

def similarity(a, b):
    # the vectors have length 1, so multiplying and adding gives the cosine similarity
    return sum(x * y for x, y in zip(a, b))

reference = next(
    i for i, c in enumerate(chunks)
    if c["source"] == "report_2024.md" and c["section"] == "Operating costs breakdown"
)
print(f"Compared with: {chunks[reference]['source']} / {chunks[reference]['section']}\n")
scores = [(similarity(vectors[reference], v), i) for i, v in enumerate(vectors) if i != reference]
for score, i in sorted(scores, reverse=True):
    print(f"{score:.2f}  {chunks[i]['source']} / {chunks[i]['section']}")