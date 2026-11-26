import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

lp = DATA_DIR / "lessons-lop-11.json"
with open(lp, encoding="utf-8") as f:
    lessons = json.load(f)

out_dir = ROOT / "scripts" / "lop11_plain"
out_dir.mkdir(parents=True, exist_ok=True)

all_text = []

for idx, les in enumerate(lessons):
    les_id = les["id"]
    title = les.get("title", "")
    html = les.get("html", "")
    
    # Strip html tags while keeping linebreaks
    # replace <p>, <li>, <h3>, etc with newlines
    text = re.sub(r'</?(?:p|li|h[1-6]|div|tr|blockquote)[^>]*>', '\n', html)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize multiple blank lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    lesson_file = out_dir / f"{idx:02d}_{les_id}.txt"
    lesson_content = f"=== {idx}: {les_id} - {title} ===\n\n" + "\n".join(f"[{i+1}] {line}" for i, line in enumerate(lines))
    lesson_file.write_text(lesson_content, encoding="utf-8")
    
    all_text.append(lesson_content)
    print(f"Exported {les_id} with {len(lines)} paragraphs.")

combined_file = out_dir / "all_lop11.txt"
combined_file.write_text("\n\n" + "="*80 + "\n\n".join(all_text), encoding="utf-8")
print(f"Total {len(lessons)} lessons exported to {out_dir}")
