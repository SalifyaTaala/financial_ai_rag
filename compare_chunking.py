from pathlib import Path

from src.chunking import load_report, fixed_size_chunks, section_chunks


def count_cut_rows(chunk_texts):
    """Count chunks whose last line is a table row cut in half."""
    count = 0
    for chunk in chunk_texts:
        last_line = chunk.splitlines()[-1]
        if last_line.startswith("|") and not last_line.rstrip().endswith("|"):
            count += 1
    return count


for path in sorted(Path("data/reports").glob("report_*.md")):
    text = load_report(path)
    fixed = fixed_size_chunks(text)
    by_section = section_chunks(text, path.name)

    print(f"{path.name}")
    print(f"  fixed-size: {len(fixed)} chunks, {count_cut_rows(fixed)} cut a table row")
    print(f"  by section: {len(by_section)} chunks, "
          f"{count_cut_rows([c['text'] for c in by_section])} cut a table row")

    hits = [c["section"] for c in by_section if "operating costs" in c["text"].lower()]
    print(f"  keyword search for 'operating costs': {len(hits)} hit(s)")

# show one finished chunk
text = load_report("data/reports/report_2025.md")
chunk = next(c for c in section_chunks(text, "report_2025.md") if c["section"] == "Financial highlights")
print("\nOne section chunk:\n")
print(chunk["text"])