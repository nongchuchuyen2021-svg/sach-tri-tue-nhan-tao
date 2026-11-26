import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

for b in ["lop-10", "lop-11", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    content = lp.read_text(encoding="utf-8")
    content = content.replace("<Chi thị>", "[Chỉ thị]").replace("Chi thị", "Chỉ thị")
    lp.write_text(content, encoding="utf-8")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for f in html_dir.glob("*.html"):
            c = f.read_text(encoding="utf-8")
            c = c.replace("<Chi thị>", "[Chỉ thị]").replace("Chi thị", "Chỉ thị")
            f.write_text(c, encoding="utf-8")

bp = DATA_DIR / "books.json"
bc = bp.read_text(encoding="utf-8")
bc = bc.replace("<Chi thị>", "[Chỉ thị]").replace("Chi thị", "Chỉ thị")
bp.write_text(bc, encoding="utf-8")

from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("Fixed Chi thị -> Chỉ thị across all files")
