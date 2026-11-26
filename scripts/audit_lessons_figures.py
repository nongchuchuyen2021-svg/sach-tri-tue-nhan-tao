import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.load(open(ROOT / "data" / "lop10_figures_master_manifest.json", encoding="utf-8"))
lessons = json.load(open(ROOT / "data" / "lessons-lop-10.json", encoding="utf-8"))

for les in lessons:
    lid = les["id"]
    m = re.match(r"bai-(\d+)", lid)
    if not m:
        continue
    bnum = m.group(1)
    figs = manifest.get(bnum, [])
    
    html = les.get("html", "")
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    placeholders = re.findall(r'<div class="figure-placeholder">.*?<figcaption[^>]*>(.*?)</figcaption>', html, re.DOTALL)
    
    print(f"=== Bài {bnum} ({lid}) ===")
    print(f"  Manifest figures ({len(figs)}): {[f['id'] for f in figs]}")
    print(f"  HTML img srcs ({len(img_srcs)}): {img_srcs}")
    if placeholders:
        print(f"  HTML placeholders ({len(placeholders)}): {[p.strip() for p in placeholders]}")
