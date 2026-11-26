import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

for b in ["lop-11", "lop-10", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    content = lp.read_text(encoding="utf-8")
    content = re.sub(r'minh•\s*\n*\s*họạ', 'minh họa', content)
    content = re.sub(r'họạ\b', 'họa', content)
    content = re.sub(r'đề\s+lan\s+toa\b', 'để lan tỏa', content)
    content = re.sub(r'\blan\s+toa\b', 'lan tỏa', content)
    content = re.sub(r'\blan\s+toả\b', 'lan tỏa', content)
    lp.write_text(content, encoding="utf-8")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for f in html_dir.glob("*.html"):
            c = f.read_text(encoding="utf-8")
            c = re.sub(r'minh•\s*\n*\s*họạ', 'minh họa', c)
            c = re.sub(r'họạ\b', 'họa', c)
            c = re.sub(r'đề\s+lan\s+toa\b', 'để lan tỏa', c)
            c = re.sub(r'\blan\s+toa\b', 'lan tỏa', c)
            c = re.sub(r'\blan\s+toả\b', 'lan tỏa', c)
            f.write_text(c, encoding="utf-8")

bp = DATA_DIR / "books.json"
bc = bp.read_text(encoding="utf-8")
bc = re.sub(r'minh•\s*\n*\s*họạ', 'minh họa', bc)
bc = re.sub(r'họạ\b', 'họa', bc)
bc = re.sub(r'đề\s+lan\s+toa\b', 'để lan tỏa', bc)
bc = re.sub(r'\blan\s+toa\b', 'lan tỏa', bc)
bc = re.sub(r'\blan\s+toả\b', 'lan tỏa', bc)
bp.write_text(bc, encoding="utf-8")

from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("Fixed minh họa and lan tỏa across all files!")
