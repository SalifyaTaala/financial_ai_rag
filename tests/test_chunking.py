from pathlib import Path

import pytest

from src.chunking import load_report, section_chunks

REPORTS = sorted(Path("data/reports").glob("report_*.md"))


def test_reports_exist():
    assert len(REPORTS) == 2, "expected report_2024.md and report_2025.md in data/reports"


@pytest.mark.parametrize("path", REPORTS, ids=lambda p: p.name)
def test_no_chunk_cuts_a_table_row(path):
    for chunk in section_chunks(load_report(path), path.name):
        for line in chunk["text"].splitlines():
            if line.startswith("|"):
                assert line.rstrip().endswith("|"), f"cut row: {line!r}"


@pytest.mark.parametrize("path", REPORTS, ids=lambda p: p.name)
def test_every_chunk_names_its_report(path):
    year = path.stem.split("_")[1]
    for chunk in section_chunks(load_report(path), path.name):
        assert f"Annual Report {year}" in chunk["text"]


@pytest.mark.parametrize("path", REPORTS, ids=lambda p: p.name)
def test_each_report_gives_six_chunks(path):
    assert len(section_chunks(load_report(path), path.name)) == 6

def test_load_all_chunks_gives_twelve():
    from src.chunking import load_all_chunks
    assert len(load_all_chunks()) == 12