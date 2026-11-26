import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

def polish_content(text):
    if not text:
        return text
        
    # Format 1. Prompt cơ bản as proper h3
    text = re.sub(
        r'<p class="lesson-p">1\.\s+Prompt cơ bản\s*\n*\s*',
        '<h3 class="subheading-h3"><span class="h3-num">1.</span> Prompt cơ bản</h3>\n<p class="lesson-p">',
        text
    )
    
    # Common name typo Binh -> Bình
    text = re.sub(r'\bBinh thu được\b', 'Bình thu được', text)
    text = re.sub(r'\bđể Binh thu\b', 'để Bình thu', text)
    text = re.sub(r'\bBinh đã\b', 'Bình đã', text)
    text = re.sub(r'\bBinh cũng\b', 'Bình cũng', text)
    
    # Common accent mixups
    text = re.sub(r'\byêu câu sau\b', 'yêu cầu sau', text)
    text = re.sub(r'\byêu câu\b', 'yêu cầu', text)
    text = re.sub(r'\btrả lời cầu hỏi\b', 'trả lời câu hỏi', text)
    text = re.sub(r'\bcầu hỏi\b', 'câu hỏi', text)
    text = re.sub(r'\bcầu lệnh\b', 'câu lệnh', text)
    text = re.sub(r'\bcác cầu trúc\b', 'các cấu trúc', text)
    text = re.sub(r'\bcầu trúc\b', 'cấu trúc', text)
    text = re.sub(r'\bcầu sau\b', 'câu sau', text)
    text = re.sub(r'\bđọc câu sạu\b', 'đọc câu sau', text)
    text = re.sub(r'\bCầu trúc\b', 'Cấu trúc', text)
    text = re.sub(r'\bCẦU TRÚC\b', 'CẤU TRÚC', text)
    text = re.sub(r'\bCầu sau\b', 'Câu sau', text)
    text = re.sub(r'\bCầu hỏi\b', 'Câu hỏi', text)
    
    return text

def clean_data_structure(data):
    if isinstance(data, str):
        return polish_content(data)
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
    print(f"Polished {lp}")
    
    html_dir = LESSONS_DIR / b
    if html_dir.exists():
        for html_file in html_dir.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            cleaned_content = polish_content(content)
            html_file.write_text(cleaned_content, encoding="utf-8")
    print(f"Polished HTMLs for {b}")

bp = DATA_DIR / "books.json"
with open(bp, encoding="utf-8") as f:
    bdata = json.load(f)
cleaned_b = clean_data_structure(bdata)
with open(bp, "w", encoding="utf-8") as f:
    json.dump(cleaned_b, f, ensure_ascii=False, indent=2)
print("Polished books.json")

# Rebuild search indexes
from master_deep_fix import rebuild_search_indexes
rebuild_search_indexes()
print("Polishing and search indexes rebuilding complete!")
