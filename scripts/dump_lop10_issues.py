import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'scripts/all_book_issues.json', encoding='utf-8') as f:
    data = json.load(f)

lop10 = data['lop-10']
print(f"Total lines with issues in lop-10: {len(lop10)}")

with open(ROOT / 'scripts/lop10_issues_readable.txt', 'w', encoding='utf-8') as out:
    for item in lop10:
        issues_str = ", ".join(item['issues'])
        out.write(f"[{item['lesson']}] ({issues_str})\n")
        out.write(f"  Line: {item['line']}\n\n")
