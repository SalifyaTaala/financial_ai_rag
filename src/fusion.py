"""Combine several ranked lists into one with Reciprocal Rank Fusion."""
from src.vector_store import search
def reciprocal_rank_fusion(rankings, k=60):
    """rankings: a list of ranked lists of ids, best first. Returns (id, score) pairs, best first."""
    scores = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)

def hybrid_search(question, keyword_index, collection, embed_query, n_results=3, pool=6):
    """Search by keywords and by meaning, then merge the two rankings."""
    keyword_hits = keyword_index.search(question, n_results=pool)
    meaning_hits = search(collection, embed_query, question, n_results=pool)