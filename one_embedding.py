from src.chunking import load_all_chunks
from src.embeddings import load_model, make_embed_fn

chunk = load_all_chunks()[0]
embed = make_embed_fn(load_model())
vector = embed([chunk["text"]])[0]
print("Chunk:", chunk["source"], "/", chunk["section"])
print("It became", len(vector), "numbers.")
print("The first five:", [round(x, 3) for x in vector[:5]])