from src.chunking import load_all_chunks
from src.fusion import reciprocal_rank_fusion, hybrid_search
from src.keyword_search import KeywordIndex
from src.vector_store import open_collection, index_chunks
from test_vector_store import fake_embed  # reuse the stand-in embedder from the vector store tests
def test_a_chunk_in_both_lists_beats_a_chunk_that_is_first_in_only_one():
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["d", "b", "e"]])
    assert fused[0][0] == "b"

def test_scores_follow_the_formula():
    fused = dict(reciprocal_rank_fusion([["a"]], k=60))
    assert abs(fused["a"] - 1 / 61) < 1e-9

def test_hybrid_search_merges_both_lists(tmp_path):
    chunks = load_all_chunks()
    collection = open_collection(path=str(tmp_path))
    index_chunks(collection, chunks, fake_embed)
    hits = hybrid_search("operating costs", KeywordIndex(chunks), collection, fake_embed, n_results=3)
    assert len(hits) == 3
    assert len({hit["id"] for hit in hits}) == 3
    assert hits[0]["fused_score"] >= hits[1]["fused_score"] >= hits[2]["fused_score"]
    assert any(hit["keyword_rank"] is not None for hit in hits)