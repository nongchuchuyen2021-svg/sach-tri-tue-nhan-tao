import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'scripts/all_book_issues.json', encoding='utf-8') as f:
    data = json.load(f)

lop12 = data['lop-12']
print(f"Total lines with issues in lop-12: {len(lop12)}")

with open(ROOT / 'scripts/lop12_issues_readable.txt', 'w', encoding='utf-8') as out:
    for item in lop12:
        issues_str = ", ".join(item['issues'])
        out.write(f"[{item['lesson']}] ({issues_str})\n")
        out.write(f"  Line: {item['line']}\n\n")
