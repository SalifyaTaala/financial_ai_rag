from pathlib import Path


def load_report(path):
    """Read a report as text. Normalise line endings so Windows and Mac/Linux behave the same."""
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")

def fixed_size_chunks(text, size=500, overlap=50):
    """Naive method: cut every `size` characters, overlapping a little."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks