"""Tests for the vector store. A tiny stand-in embedder keeps them fast and offline."""
import hashlib
import math

from src.chunking import load_all_chunks
from src.vector_store import open_collection, index_chunks

def fake_embed(texts, dim=64):
    """Stand-in for the real model: counts words into 64 buckets. Not smart, but deterministic."""
    vectors = []
    for text in texts:
        v = [0.0] * dim
        for word in text.lower().split():
            v[int(hashlib.md5(word.encode()).hexdigest(), 16) % dim] += 1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        vectors.append([x / norm for x in v])
    return vectors

def test_index_holds_every_chunk(tmp_path):
    collection = open_collection(path=str(tmp_path))
    index_chunks(collection, load_all_chunks(), fake_embed)
    assert collection.count() == 12

def test_indexing_twice_does_not_duplicate(tmp_path):
    collection = open_collection(path=str(tmp_path))
    index_chunks(collection, load_all_chunks(), fake_embed)
    index_chunks(collection, load_all_chunks(), fake_embed)
    assert collection.count() == 12

def test_each_chunk_is_stored_with_its_numbers_and_label(tmp_path):
    collection = open_collection(path=str(tmp_path))
    index_chunks(collection, load_all_chunks(), fake_embed)
    record = collection.get(
        ids=["report_2025.md::Financial highlights"],
        include=["documents", "metadatas", "embeddings"],
    )
    assert len(record["embeddings"][0]) == 64
    assert record["metadatas"][0]["section"] == "Financial highlights"
    assert "Annual Report 2025" in record["documents"][0]