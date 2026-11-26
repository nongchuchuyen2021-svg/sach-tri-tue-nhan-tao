import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'scripts/all_book_issues.json', encoding='utf-8') as f:
    data = json.load(f)

for book in ['lop-10', 'lop-11', 'lop-12']:
    items = data[book]
    print(f"\n=== Remaining in {book} ({len(items)}) ===")
    for it in items[:15]:
        print(f"[{it['lesson']}] {it['issues']}")
        print(f"   {it['line'][:110]}...")
