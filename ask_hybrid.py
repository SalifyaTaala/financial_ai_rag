
import sys
from src.chunking import load_all_chunks
from src.embeddings import load_model, make_embed_fn, QUERY_PREFIX
from src.fusion import hybrid_search
from src.keyword_search import KeywordIndex
from src.vector_store import open_collection
question = " ".join(sys.argv[1:]) or "How did operating costs change between 2024 and 2025?"
keyword_index = KeywordIndex(load_all_chunks())
embed_query = make_embed_fn(load_model(), QUERY_PREFIX)
hits = hybrid_search(question, keyword_index, open_collection(), embed_query, n_results=3)
print(f"Question: {question}\n")
for rank, hit in enumerate(hits, start=1):
    print(f"{rank}. {hit['source']} / {hit['section']}")
    print(f"   score {hit['fused_score']:.4f}  (keyword rank: {hit['keyword_rank']}, meaning rank: {hit['meaning_rank']})")