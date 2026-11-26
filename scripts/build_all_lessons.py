import os
import re
import json
from pathlib import Path
from test_page_generator import get_page_blocks
from ocr_cleaner import clean_ocr_text
from lesson_html_builder import build_lesson_html

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

def slugify(text):
    text = text.lower()
    text = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", text)
    text = re.sub(r"[èéẹẻẽêềếệểễ]", "e", text)
    text = re.sub(r"[ìíịỉĩ]", "i", text)
    text = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", text)
    text = re.sub(r"[ùúụủũưừứựửữ]", "u", text)
    text = re.sub(r"[ỳýỵỷỹ]", "y", text)
    text = re.sub(r"[đ]", "d", text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text

def process_all_books():
    with open(DATA_DIR / "books.json", encoding="utf-8") as f:
        books_data = json.load(f)
        
    books = books_data.get("books", books_data)
    
    for book in books:
        book_id = book["id"]
        pdf_name = f"{book_id}-tri-tue-nhan-tao.pdf"
        pdf_path = ROOT / pdf_name
        
        print(f"\n==========================================")
        print(f"Processing {book_id}: {book['title']}")
        print(f"==========================================")
        
        seq_pages = get_page_blocks(pdf_path, book_id)
        print(f"Loaded {len(seq_pages)} sequential pages for {book_id}")
        
        # Flatten all items in toc
        all_items = []
        for g_idx, group in enumerate(book.get("toc", [])):
            g_title = group.get("group", "")
            for it in group.get("items", []):
                all_items.append({
                    "group": g_title,
                    "title": it["title"],
                    "page": it["page"],
                    "printPage": it.get("printPage"),
                })
                
        lessons_data = []
        book_out_dir = LESSONS_DIR / book_id
        book_out_dir.mkdir(parents=True, exist_ok=True)
        
        for i, item in enumerate(all_items):
            title = item["title"]
            group = item["group"]
            start_p = item["page"]
            
            # Determine end page
            if i + 1 < len(all_items):
                end_p = all_items[i + 1]["page"] - 1
            else:
                end_p = len(seq_pages)
                
            if end_p < start_p:
                end_p = start_p
                
            slug = slugify(title)
            if not slug:
                slug = f"trang-{start_p}"
                
            # Collect blocks
            blocks = []
            for pnum in range(start_p, end_p + 1):
                if 1 <= pnum <= len(seq_pages):
                    for b in seq_pages[pnum - 1]:
                        txt = clean_ocr_text(b[4])
                        if not txt:
                            continue
                        if re.match(r"^\d{1,3}$", txt.strip()):
                            continue
                        blocks.append({
                            "page": pnum,
                            "bbox": (round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1)),
                            "text": txt
                        })
                        
            # Build semantic HTML
            html_content = build_lesson_html(title, group, blocks, book_id, start_p, end_p)
            
            # Plain text snippet for search
            full_plain_text = " ".join(b["text"] for b in blocks)
            full_plain_text = re.sub(r"\s+", " ", full_plain_text).strip()
            summary = full_plain_text[:280] + ("..." if len(full_plain_text) > 280 else "")
            
            lesson_entry = {
                "id": slug,
                "bookId": book_id,
                "title": title,
                "group": group,
                "startPage": start_p,
                "endPage": end_p,
                "pageCount": end_p - start_p + 1,
                "summary": summary,
                "textLength": len(full_plain_text),
                "html": html_content
            }
            lessons_data.append(lesson_entry)
            
            # Also write individual lesson HTML snippet
            with open(book_out_dir / f"{slug}.html", "w", encoding="utf-8") as f_html:
                f_html.write(html_content)
                
            print(f"  ✓ [{slug}] {title} (p.{start_p}-{end_p}): {len(blocks)} blocks, {len(full_plain_text)} chars")
            
        # Save lessons JSON
        out_json_path = DATA_DIR / f"lessons-{book_id}.json"
        with open(out_json_path, "w", encoding="utf-8") as f_json:
            json.dump(lessons_data, f_json, ensure_ascii=False, indent=2)
            
        print(f"Saved {len(lessons_data)} lessons to {out_json_path}")
        
    print("\nALL 3 BOOKS PROCESSED SUCCESSFULLY!")

if __name__ == "__main__":
    process_all_books()
