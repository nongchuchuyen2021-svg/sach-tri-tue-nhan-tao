import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'scripts/all_book_issues.json', encoding='utf-8') as f:
    data = json.load(f)

lop11 = data['lop-11']
print(f"Total lines with issues in lop-11: {len(lop11)}")

# Group by issue type
for item in lop11:
    issues_str = ", ".join(item['issues'])
    print(f"[{item['lesson']}] ({issues_str})")
    print(f"  Line: {item['line']}\n")
