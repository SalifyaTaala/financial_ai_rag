import sys
from src.embeddings import load_model, make_embed_fn, QUERY_PREFIX
from src.vector_store import open_collection, search
question = " ".join(sys.argv[1:]) or "How did operating costs change between 2024 and 2025?"
embed_query = make_embed_fn(load_model(), QUERY_PREFIX)
hits = search(open_collection(), embed_query, question, n_results=3)
print(f"Question: {question}\n")
for rank, hit in enumerate(hits, start=1):
    print(f"{rank}. {hit['source']} / {hit['section']}  (distance {hit['distance']:.3f})")