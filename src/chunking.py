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

def section_chunks(text, source):
    """Structure-aware method: one chunk per section, labelled with its report."""
    title = text.splitlines()[0].lstrip("# ").strip()
    chunks = []
    for block in text.split("\n## ")[1:]:
        heading, _, body = block.partition("\n")
        chunks.append({
            "source": source,
            "section": heading.strip(),
            "text": f"{title} - {heading.strip()}\n{body.strip()}",
        })
    return chunks

def load_all_chunks(folder="data/reports"):
    """Chunk every report in the folder by section. Returns one list of chunks."""
    chunks = []
    for path in sorted(Path(folder).glob("report_*.md")):
        chunks += section_chunks(load_report(path), path.name)
    return chunks