import sys

from src.chunking import load_all_chunks
from src.keyword_search import KeywordIndex
question = " ".join(sys.argv[1:]) or "How did operating costs change between 2024 and 2025?"
hits = KeywordIndex(load_all_chunks()).search(question, n_results=3)
print(f"Question: {question}\n")
for rank, hit in enumerate(hits, start=1):
    print(f"{rank}. {hit['source']} / {hit['section']}  (score {hit['score']:.2f})")