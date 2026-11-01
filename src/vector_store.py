"""Store chunks, and the numbers that describe them, in ChromaDB."""
import chromadb

def open_collection(path="chroma_db", name="reports"):
    """Open (or create) the collection that holds our chunks."""
    client = chromadb.PersistentClient(path=path)
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})

def index_chunks(collection, chunks, embed_passages):
    """Embed every chunk and store it. Safe to run twice: same ids are overwritten."""
    texts = [chunk["text"] for chunk in chunks]
    collection.upsert(
        ids=[f"{chunk['source']}::{chunk['section']}" for chunk in chunks],
        documents=texts,
        embeddings=embed_passages(texts),
        metadatas=[{"source": chunk["source"], "section": chunk["section"]} for chunk in chunks],
    )