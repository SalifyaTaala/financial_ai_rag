"""Turn text into embeddings (lists of numbers) with the BGE model."""
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-base-en-v1.5"

def load_model():
    """Load the embedding model. The first call downloads it (about 440 MB)."""
    return SentenceTransformer(MODEL_NAME)

def make_embed_fn(model):
    """Return a function that turns a list of texts into a list of embeddings."""
    def embed(texts):
        return model.encode(texts, normalize_embeddings=True).tolist()
    return embed