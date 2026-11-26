import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Collect all tokens from the 3 books
token_counts = Counter()
token_locations = {}

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        clean = re.sub(r"<[^>]+>", " ", les.get("html", ""))
        words = re.findall(r"\b[a-zA-ZàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđA-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]+\b", clean)
        for w in words:
            wl = w.lower()
            token_counts[wl] += 1
            if wl not in token_locations:
                token_locations[wl] = []
            if len(token_locations[wl]) < 2:
                # store sample context
                idx = clean.lower().find(wl)
                ctx = clean[max(0, idx-20):min(len(clean), idx+len(wl)+20)].replace('\n', ' ')
                token_locations[wl].append((b, les['id'], ctx))

# Let's filter for tokens that contain Vietnamese accented characters and have low frequency (<= 3)
viet_rare = []
for tok, count in token_counts.items():
    if count <= 3 and re.search(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", tok):
        viet_rare.append((tok, count))

print(f"Total rare accented tokens (count <= 3): {len(viet_rare)}")
# Sort alphabetically
viet_rare.sort()

# Print suspicious rare tokens
for tok, cnt in viet_rare:
    # check if suspicious: has weird letter combinations or known bad patterns
    # e.g., ending with unusual consonants or rare vowels with wrong tones
    samples = token_locations[tok]
    print(f"[{tok}] (x{cnt}): {samples[0][0]}/{samples[0][1]} -> {samples[0][2]}")
