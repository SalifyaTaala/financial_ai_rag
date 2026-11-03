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

    keyword_rank = {hit["id"]: r for r, hit in enumerate(keyword_hits, start=1)}
    meaning_rank = {hit["id"]: r for r, hit in enumerate(meaning_hits, start=1)}
    by_id = {hit["id"]: hit for hit in keyword_hits + meaning_hits}

    fused = reciprocal_rank_fusion([list(keyword_rank), list(meaning_rank)])
    return [
        {
            "id": chunk_id,
            "source": by_id[chunk_id]["source"],
            "section": by_id[chunk_id]["section"],
            "fused_score": score,
            "keyword_rank": keyword_rank.get(chunk_id),
            "meaning_rank": meaning_rank.get(chunk_id),
            "text": by_id[chunk_id]["text"],
        }
        for chunk_id, score in fused[:n_results]
    ]