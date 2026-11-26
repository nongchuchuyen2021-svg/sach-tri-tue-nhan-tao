import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "scripts" / "audit_report.json", encoding="utf-8") as f:
    report = json.load(f)

# Collect all unique suspicious words and a sample line for each
word_samples = {}
for item in report:
    for w in item["suspicious"]:
        wl = w.lower()
        if wl not in word_samples:
            word_samples[wl] = (item["book"], item["lesson"], item["line"], w)

print(f"Total unique suspicious words: {len(word_samples)}")

# Print them grouped by book
for b in ["lop-10", "lop-11", "lop-12"]:
    b_words = [v for v in word_samples.values() if v[0] == b]
    print(f"\n==================== {b} ({len(b_words)} suspicious words) ====================")
    for book, lid, line, orig_w in sorted(b_words, key=lambda x: x[3].lower()):
        # only print if contains non-ascii or has vietnamese tone issues or looks like OCR typo
        clean_ctx = line.replace('\n', ' ')
        if len(clean_ctx) > 120:
            idx = clean_ctx.lower().find(orig_w.lower())
            if idx != -1:
                clean_ctx = clean_ctx[max(0, idx-30):min(len(clean_ctx), idx+len(orig_w)+30)]
        print(f"[{lid}] '{orig_w}': ...{clean_ctx}...")
