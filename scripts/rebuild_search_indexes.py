import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    sp = ROOT / "data" / f"search-{b}.json"
    
    lessons = json.loads(lp.read_text(encoding="utf-8"))
    search_data = []
    
    for item in lessons:
        html = item.get("html", "")
        # Strip HTML tags
        clean_text = re.sub(r"<[^>]+>", " ", html)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        
        # Combine title, group, and content
        full_content = f"{item.get('group', '')} {item.get('title', '')} {clean_text}".strip()
        full_content = re.sub(r"\s+", " ", full_content)
        
        search_data.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "group": item.get("group"),
            "startPage": item.get("startPage", 1),
            "content": full_content
        })
    
    sp.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt {sp} with {len(search_data)} entries.")
