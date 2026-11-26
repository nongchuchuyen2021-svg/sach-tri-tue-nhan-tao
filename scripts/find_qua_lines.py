import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for b in ['lop-10', 'lop-11', 'lop-12']:
    data = json.load(open(ROOT / f'data/lessons-{b}.json', encoding='utf-8'))
    for les in data:
        for line in les.get('html', '').splitlines():
            if 'quà' in line:
                print(f"{b} / {les['id']}: {line.strip()}")
