import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "scripts" / "audit_report.json", encoding="utf-8") as f:
    report = json.load(f)

print(f"Total report items: {len(report)}")

# Count words
word_counts = Counter()
for item in report:
    for w in item["suspicious"]:
        word_counts[w.lower()] += 1

print("Total unique suspicious words:", len(word_counts))

# Filter out obvious false positives (e.g. capitalized English tech or names)
# Let's print all suspicious words and their count
suspect_list = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

with open(ROOT / "scripts" / "suspicious_words_summary.txt", "w", encoding="utf-8") as f:
    for w, cnt in suspect_list:
        f.write(f"{w}: {cnt}\n")

print("Saved suspicious_words_summary.txt. Top 50:")
for w, cnt in suspect_list[:50]:
    print(f"  {w} (x{cnt})")
