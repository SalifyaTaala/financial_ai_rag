"""Keyword search over the chunks with BM25."""
import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    """Split text into lowercase words and numbers, keeping decimals like 4.8 whole."""
    return re.findall(r"\d+(?:\.\d+)?|[a-z]+", text.lower())

class KeywordIndex:
    def __init__(self, chunks):
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(chunk["text"]) for chunk in chunks])
    def search(self, question, n_results=3):
        """Return the chunks with the best keyword score, best first."""
        scores = self.bm25.get_scores(tokenize(question))
        best = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_results]
        return [
            {
                "id": f"{self.chunks[i]['source']}::{self.chunks[i]['section']}",
                "source": self.chunks[i]["source"],
                "section": self.chunks[i]["section"],
                "score": float(scores[i]),
                "text": self.chunks[i]["text"],
            }
            for i in best
        ]