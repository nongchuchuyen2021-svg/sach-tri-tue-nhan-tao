import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

vi_words = set(w.lower().strip() for w in open(ROOT / "scripts" / "vi_50k.txt", encoding="utf-8"))

# Load audit report
with open(ROOT / "scripts" / "audit_report.json", encoding="utf-8") as f:
    report = json.load(f)

# Find all suspicious tokens containing Vietnamese accented letters
viet_errors = Counter()
viet_error_contexts = {}

for item in report:
    for w in item["suspicious"]:
        wl = w.lower()
        # if contains vietnamese accented characters
        if re.search(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", wl):
            if wl not in vi_words:
                viet_errors[w] += 1
                if w not in viet_error_contexts:
                    viet_error_contexts[w] = (item["book"], item["lesson"], item["line"])

print(f"Total Vietnamese tokens with spelling issues: {len(viet_errors)}")
for w, cnt in viet_errors.most_common(150):
    b, lid, line = viet_error_contexts[w]
    idx = line.lower().find(w.lower())
    ctx = line[max(0, idx-25):min(len(line), idx+len(w)+25)].replace('\n', ' ')
    print(f"'{w}' (x{cnt}) in {b}/{lid}: ...{ctx}...")
