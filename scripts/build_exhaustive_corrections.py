import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

vi_words = set(w.lower().strip() for w in open(ROOT / "scripts" / "vi_50k.txt", encoding="utf-8"))

with open(ROOT / "scripts" / "audit_report.json", encoding="utf-8") as f:
    report = json.load(f)

# Find all suspicious tokens containing Vietnamese accented letters or known typos
problematic_tokens = []
for item in report:
    b = item["book"]
    lid = item["lesson"]
    line = item["line"]
    for w in item["suspicious"]:
        wl = w.lower()
        if re.search(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", wl) and wl not in vi_words:
            problematic_tokens.append((b, lid, line, w))

print("Total occurrences of problematic accented tokens:", len(problematic_tokens))

# Print each unique problem with context
unique_problems = {}
for b, lid, line, w in problematic_tokens:
    if w not in unique_problems:
        unique_problems[w] = (b, lid, line)

for w, (b, lid, line) in sorted(unique_problems.items(), key=lambda x: x[0]):
    idx = line.lower().find(w.lower())
    s = max(0, idx - 30)
    e = min(len(line), idx + len(w) + 30)
    print(f"[{w}] in {b}/{lid}: ...{line[s:e].replace(chr(10), ' ')}...")
