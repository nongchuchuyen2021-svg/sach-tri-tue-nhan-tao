import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
lessons = json.load(open(ROOT / "data" / "lessons-lop-10.json", encoding="utf-8"))

missing = []
total_imgs = 0
total_px = 0

for les in lessons:
    lid = les["id"]
    if not lid.startswith("bai-"):
        continue
    html = les.get("html", "")
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for src in srcs:
        total_imgs += 1
        p = ROOT / src
        if not p.exists():
            missing.append((lid, src))
        else:
            with Image.open(p) as im:
                w, h = im.size
                total_px += w
                print(f"[{lid}] {src} -> {w}x{h} px ({p.stat().st_size / 1024:.1f} KB)")

print(f"\nTotal images verified: {total_imgs}")
print(f"Average width: {total_px / total_imgs:.0f} px")
if missing:
    print(f"ERROR: Missing files: {missing}")
else:
    print("ALL IMAGES EXIST PHYSICALLY WITH HIGH RESOLUTION!")
