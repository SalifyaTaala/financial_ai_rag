"""Turn text into embeddings (lists of numbers) with the BGE model."""
from sentence_transformers import SentenceTransformer
MODEL_NAME = "BAAI/bge-base-en-v1.5"
# BGE works best when a short question gets this sentence in front of it.
# Chunks are embedded as they are, without a prefix.
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

def load_model():
    """Load the embedding model. The first call downloads it (about 440 MB)."""
    return SentenceTransformer(MODEL_NAME)

def make_embed_fn(model, prefix=""):
    """Return a function that turns a list of texts into a list of embeddings."""
    def embed(texts):
        prefixed = [prefix + text for text in texts]
        return model.encode(prefixed, normalize_embeddings=True).tolist()
    return embed