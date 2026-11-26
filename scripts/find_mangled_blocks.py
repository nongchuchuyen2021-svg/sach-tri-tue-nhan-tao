import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Let's inspect all lessons across all grades for gibberish lines or bad OCR blocks
for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        # look at paragraphs or list items
        elements = re.findall(r"<(p|li|h1|h2|h3|h4|div)[^>]*>(.*?)</\1>", html, re.DOTALL)
        for tag, text in elements:
            clean = re.sub(r"<[^>]+>", " ", text).strip()
            # check if line contains multiple weird english-like non-words or OCR junk
            # e.g., words with mixed vowels/consonants that make no sense
            words = clean.split()
            if len(words) >= 4:
                # count words that look like gibberish
                gib_count = 0
                for w in words:
                    w_stripped = re.sub(r"[^\w]", "", w)
                    # if word has both lower and upper mixed oddly or weird characters
                    if re.search(r"[a-z][A-Z]", w_stripped) or re.search(r"[0-9][a-zA-Z]", w_stripped):
                        gib_count += 1
                    elif w_stripped.lower() in ["coia", "xuy", "tưân", "coirh", "ckcy", "vill", "cont", "dese", "kac", "vito", "erito", "contnuovo", "koy", "oes", "kích", "d0"]:
                        gib_count += 1
                if gib_count >= 2 or (len(words) <= 10 and gib_count >= 1 and re.search(r"[0-9][a-zA-Z]", clean)):
                    print(f"[{b}/{les['id']}] Suspicious block: {clean}")
