import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Collect all tokens containing digits mixed with letters
mixed_tokens = Counter()

# Exclude valid technical tokens
VALID_TOKENS = {
    "mp4", "mp3", "gpt-4", "gpt-4o", "gpt-3.5", "gpt4", "gpt3", "4k", "2k", "3d", "2d",
    "h1", "h2", "h3", "h4", "h5", "h6", "st25", "w3schools", "f1", "k-nearest", "k-means",
    "x1", "x2", "y1", "y2", "v1", "v2", "p1", "p2", "000đ", "100%", "50%", "30%", "20%",
    "claude-3", "llama-2", "llama-3", "llama2", "llama3", "gemini-1.5", "python3", "utf-8",
    "sha256", "ipv4", "ipv6", "html5", "css3", "oauth2", "b1", "b2", "c1", "c2", "a1", "a2"
}

for grade in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{grade}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        # Remove tags and code blocks
        clean = re.sub(r"<code>.*?</code>", "", html, flags=re.DOTALL)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = re.sub(r"https?://\S+", "", clean)
        
        words = re.findall(r"\b[A-Za-zÀ-ỹ\d]+\b", clean)
        for w in words:
            if re.search(r"[A-Za-zÀ-ỹ]", w) and re.search(r"\d", w):
                wl = w.lower()
                if wl not in VALID_TOKENS and not re.match(r"^\d+(?:px|pt|em|rem|kg|g|ml|l|m|cm|mm|s|ms|h|w|k|gb|mb|tb|b|đ|d)$", wl):
                    mixed_tokens[(grade, les["id"], w)] += 1

print(f"Total mixed tokens found: {len(mixed_tokens)}")
for (grade, lid, w), count in mixed_tokens.most_common(40):
    print(f"[{grade} - {lid}] '{w}': {count}")
