import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

SPECIFIC_RESIDUALS = [
    # lop-11
    (r'Vì dụ cầu "Hôm nay', 'Ví dụ câu "Hôm nay'),
    (r'Vì dụ cầu', 'Ví dụ câu'),
    (r'Vì dụ:', 'Ví dụ:'),
    (r'x\(t\)\s*=\s*A\.\s*COS\(wt\s*\+\s*Ф\)', 'x(t) = A.cos(ωt + φ)'),
    (r'x\(t\)\s*=\s*A\.\s*cos\(wt\s*\+\s*Ф\)', 'x(t) = A.cos(ωt + φ)'),
    (r'Hãy tớm', 'Hãy tóm'),
    (r'hàm số côsin:', 'hàm số cosin:'),
    (r'hàm số cô-sin:', 'hàm số cosin:'),
    (r'Chỉ thị \(directive\):', 'Chỉ thị:'),
    (r'Ví dụ \(examples\):', 'Ví dụ:'),
    (r'Ngữ cảnh \(contexl\):', 'Ngữ cảnh (context):'),
    (r'Ngữ cảnh \(context\):', 'Ngữ cảnh:'),
    (r'Định dạng đầu ra \(output format\):', 'Định dạng đầu ra:'),
    (r'đàu ra', 'đầu ra'),
    
    # lop-12
    (r'\*LOP 12', 'LỚP 12'),
    (r'trả lời cầu hỏi', 'trả lời câu hỏi'),
    (r'dưa trện do liệu huấn', 'dựa trên dữ liệu huấn'),
    (r'Thực Hiện nhiệm vu tư đöng', 'Thực hiện nhiệm vụ tự động'),
    (r'Rs quyệt đinh thông minh', 'Ra quyết định thông minh'),
    (r'GisO ID ho Thoas Ms rener', ''),
    (r'Tes lori eDu Ach thrstng g8p', ''),
    (r'ADUOO', ''),
    (r'Output UBI', ''),
    (r'Explorm Errors Detuana CWn toy', ''),
    (r'Ovarview Quick Heic', ''),
    (r'v E Dsta Sources', 'Data Sources'),
    (r'y a Functions', 'Functions'),
    (r'l Usor Inputs', 'User Inputs'),
    (r'v S Workflows', 'Workflows'),
    (r'B Main\.fow', 'Main.flow'),
    (r'Start End No Overview', 'Overview'),
    (r'X Generator Agent Le Edit Overvien', 'Overview'),
    (r'Preview v Publish', 'Preview & Publish'),
    (r'800 \*\) Vi dá»¥ Demo SÃ¡ch - Dian Soveu:', 'Ví dụ Demo Sách:'),
    (r'800 \*\) Vi dụ Demo Sách - Dian Soveu:', 'Ví dụ Demo Sách:'),
    (r'Dian Soveu', ''),
    (r'Create Podcast Two-hast podcast about a topic', 'Create Podcast: Two-host podcast about a topic'),
    (r'Transoribe Audio', 'Transcribe Audio'),
    (r'Colleci data', 'Collect data'),
    (r'Two-hast podcast', 'Two-host podcast')
]

def apply_residuals(text):
    if not text:
        return text
    current = text
    for pat, repl in SPECIFIC_RESIDUALS:
        current = re.sub(pat, repl, current)
    return current

def clean_data_structure(data):
    if isinstance(data, str):
        return apply_residuals(data)
    elif isinstance(data, list):
        return [clean_data_structure(it) for it in data]
    elif isinstance(data, dict):
        return {k: clean_data_structure(v) for k, v in data.items()}
    return data

for b in ["lop-10", "lop-11", "lop-12"]:
    lp = DATA_DIR / f"lessons-{b}.json"
    with open(lp, encoding="utf-8") as f:
        data = json.load(f)
    cleaned = clean_data_structure(data)
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Residual cleaned {lp}")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for html_file in html_dir.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            cleaned_content = apply_residuals(content)
            html_file.write_text(cleaned_content, encoding="utf-8")
    print(f"Residual cleaned HTMLs for {b}")

# Also books.json
bp = DATA_DIR / "books.json"
with open(bp, encoding="utf-8") as f:
    bdata = json.load(f)
cleaned_b = clean_data_structure(bdata)
with open(bp, "w", encoding="utf-8") as f:
    json.dump(cleaned_b, f, ensure_ascii=False, indent=2)
print("Residual cleaned books.json")

# Rebuild search
from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("All residual cleaning and index rebuilding complete!")
