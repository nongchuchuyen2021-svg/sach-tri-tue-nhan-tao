import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

patterns = [
    r"\bA/\b",
    r"\blạo\b",
    r"\btao\b",
    r"\bcủ\b",
    r"\bthô\b",
    r"Ií",
    r"!í",
    r"\bkT\b",
    r"\bChatQPT\b",
    r"\bCopilol\b",
    r"\bLlamalndex\b",
    r"\bColaboralory\b",
    r"\bColadl\b",
    r"\bopenal\b",
    r"\blương ứng\b",
    r"\bthuận liện\b",
    r"\btrọng đó\b",
    r"\bkhả náng\b",
    r"\bhình ành\b",
    r"\bkết quá\b",
    r"\bmó tả\b",
    r"\bmô lả\b",
    r"\bBải \d+\b",
    r"\bthúc đầy\b",
    r"\bkhia cạnh\b",
    r"\bthừ nghiệm\b",
    r"\bhóá\b",
    r"\bvàng cug\b",
    r"\bđam mề\b",
    r"\bchù để\b",
    r"\bđổi tượng\b",
    r"\bhoàn chính\b",
    r"\bmiaro\b",
    r"\bvừng chúc\b",
    r"\bmạnh khoe\b",
    r"\bnhiều lâm\b",
    r"\bnu cười\b",
    r"\bbạn bẻ\b",
    r"\bngười thần\b",
    r"\bcủng một\b",
    r"\bbắt kì\b",
    r"\blưu trứ\b",
    r"\bchúc mùng\b",
    r"\bvẽ một bằng\b",
    r"\bBàng \d+\b",
    r"\bkhỏng\b",
]

regex = re.compile("|".join(patterns), re.IGNORECASE)

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    print(f"\n==================== {b} ====================")
    for les in data:
        lid = les["id"]
        html = les.get("html", "")
        # Remove tags
        clean = re.sub(r"<[^>]+>", " ", html)
        matches = list(regex.finditer(clean))
        if matches:
            print(f"[{lid}] {len(matches)} matches:")
            for m in matches:
                start = max(0, m.start() - 35)
                end = min(len(clean), m.end() + 35)
                snippet = clean[start:end].replace("\n", " ").strip()
                print(f"    >>> ...{snippet}...")
