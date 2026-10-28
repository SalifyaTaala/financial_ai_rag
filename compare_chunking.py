from pathlib import Path

from src.chunking import load_report, fixed_size_chunks

for path in sorted(Path("data/reports").glob("report_*.md")):
    text = load_report(path)
    chunks = fixed_size_chunks(text)
    print(f"{path.name}: {len(text)} characters -> {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        last_line = chunk.splitlines()[-1]
        if last_line.startswith("|") and not last_line.rstrip().endswith("|"):
            print(f"  chunk {i} ends in the middle of a table row: {last_line!r}")