from src.vector_store import open_collection

collection = open_collection()
print("Chunks stored:", collection.count())
record = collection.get(
    ids=["report_2025.md::Financial highlights"],
    include=["documents", "metadatas", "embeddings"],
)
print("\nOne stored record")
print("id:     ", record["ids"][0])
print("label:  ", record["metadatas"][0])
print("text:   ", record["documents"][0][:60].replace("\n", " "), "...")
print("numbers:", len(record["embeddings"][0]))