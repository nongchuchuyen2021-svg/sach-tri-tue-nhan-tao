import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

lines = open(ROOT / "scripts" / "genuine_errors.txt", encoding="utf-8").readlines()

words = Counter()
for l in lines:
    if l.startswith("[") and "SUSP: " in l:
        parts = l.split("SUSP: ")[1].strip().strip("[]").replace("'", "").split(", ")
        for p in parts:
            if p:
                words[p.strip()] += 1

print(f"Total distinct error words: {len(words)}")
# Print by frequency
for w, cnt in words.most_common(200):
    print(f"'{w}': {cnt},")
