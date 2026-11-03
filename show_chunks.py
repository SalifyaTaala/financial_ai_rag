from src.chunking import load_all_chunks

chunks = load_all_chunks()
print(len(chunks), "chunks")
for chunk in chunks:
    print(f"{chunk['source']} / {chunk['section']}")