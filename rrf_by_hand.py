from src.fusion import reciprocal_rank_fusion

keyword_ranking = ["chunk A", "chunk B", "chunk C"]
meaning_ranking = ["chunk D", "chunk B", "chunk E"]
print("Keyword search says:", keyword_ranking)
print("Meaning search says:", meaning_ranking)
print()
for chunk, score in reciprocal_rank_fusion([keyword_ranking, meaning_ranking]):
    print(f"{score:.4f}  {chunk}")
