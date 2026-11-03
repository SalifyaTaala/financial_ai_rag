from src.chunking import load_all_chunks
from src.keyword_search import KeywordIndex, tokenize

QUESTION = "How did operating costs change between 2024 and 2025?"

def test_tokenize_keeps_decimals_whole():
    assert tokenize("Operating expenses rose to USD 4.8 million") == [
        "operating", "expenses", "rose", "to", "usd", "4.8", "million",
    ]

def test_costs_question_finds_the_2024_breakdown_first():
    hits = KeywordIndex(load_all_chunks()).search(QUESTION)
    assert (hits[0]["source"], hits[0]["section"]) == ("report_2024.md", "Operating costs breakdown")

def test_keyword_search_misses_2025_when_the_wording_differs():
    # This documents the gap that fusion closes: the 2025 report says "expenses", not "costs".
    hits = KeywordIndex(load_all_chunks()).search(QUESTION)
    assert all(hit["source"] == "report_2024.md" for hit in hits)