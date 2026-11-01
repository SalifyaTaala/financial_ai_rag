from src.chunking import load_all_chunks
from src.embeddings import load_model, make_embed_fn
from src.vector_store import open_collection, index_chunks
chunks = load_all_chunks()
collection = open_collection()
index_chunks(collection, chunks, make_embed_fn(load_model()))
print(f"Indexed {len(chunks)} chunks. The collection now holds {collection.count()}.")