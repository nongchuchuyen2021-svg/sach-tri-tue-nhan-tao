import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Common Vietnamese syllables / words
vietnamese_typos = Counter()

def extract_vietnamese_words(text):
    clean = re.sub(r"<[^>]+>", " ", text)
    # clean code, URLs
    clean = re.sub(r"https?://\S+", " ", clean)
    words = re.findall(r"\b[A-Za-zÀ-ỹ]+\b", clean)
    return words

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        # Find single words with suspicious characters or accents
        # e.g., words with 'I' in the middle of lowercases, like 'xử Ií'
        for m in re.finditer(r"\b\w*I[a-zà-ỹ]\w*\b", html):
            vietnamese_typos[m.group(0)] += 1
        # Words ending with unusual vowels + accents
        for m in re.finditer(r"\b[a-zà-ỹ]*(?:áng|óá|iền|uông|khoe|lâm)\b", html, re.I):
            vietnamese_typos[m.group(0)] += 1

print("Sample detected words:")
for w, c in vietnamese_typos.most_common(40):
    print(f"  {w}: {c}")
