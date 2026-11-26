import json
from pathlib import Path

data = json.loads(Path('data/lessons-lop-11.json').read_text(encoding='utf-8'))
targets = ['nhỏmTự', 'càc', 'rảng', 'nhán', 'ENGUSH', 'promct', 'họạ', 'tàp', 'tưr', 'HANNo']

for les in data:
    for t in targets:
        if t in les.get('html', ''):
            for l in les['html'].split('\n'):
                if t in l:
                    print(f"[{les['id']}] ({t}): {l.strip()}")
