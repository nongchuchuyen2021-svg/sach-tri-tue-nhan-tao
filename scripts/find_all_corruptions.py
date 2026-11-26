import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Load all text across the 3 books
all_text = ""
for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        # Remove tags
        clean = re.sub(r"<[^>]+>", " ", html)
        all_text += " " + clean

# Tokenize into words
words = re.findall(r"\b[A-Za-zÀ-ỹ\d\-\/\.\!\?\:\;\,\(\)]+\b", all_text)
print(f"Total word tokens: {len(words)}")

# Find words with suspicious characters or patterns
candidates = Counter()
for w in words:
    # Check if contains slash or exclamation or weird combo
    if re.search(r"[!@#$%^&*\/]", w) and not re.match(r"^(https?|and/or|Input/Output|I/O|Train/Test|Precision/Recall|và/hoặc|đ/gói|VND/Lit|low/no|If/Else|A/B)$", w, re.I):
        candidates[w] += 1
    # Check if ends with 'l' instead of 't' (like Copilol)
    if re.search(r"(?:Copilol|ChatQPT|Suno A|Openal|Coladl|Colaboralory)", w, re.I):
        candidates[w] += 1
    # Words with tone marks that look corrupt
    if re.search(r"[a-z][A-Z]", w): # CamelCase in Vietnamese? e.g. ChatQPT, Trách nhiệmgiải
        candidates[w] += 1

print("\nSpecific candidate corruptions:")
for w, c in candidates.most_common(50):
    print(f"  {w}: {c}")
