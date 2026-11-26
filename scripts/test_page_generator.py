import pymupdf
import re
from ocr_cleaner import clean_ocr_text

def get_page_blocks(pdf_path, book_id):
    doc = pymupdf.open(pdf_path)
    seq_pages = []
    
    for idx, page in enumerate(doc):
        w, h = page.rect.width, page.rect.height
        
        # Handling lop-10 rotated page 1
        if book_id == "lop-10" and idx == 1:
            # Rotated spread: in raw PDF it is portrait or landscape
            # Let's check dimensions and blocks
            raw_blocks = page.get_text("blocks")
            # Page was rotated 90 deg CCW in scan, so top half is left page, bottom half is right page
            mid_y = h / 2.0
            top_blocks = [b for b in raw_blocks if (b[1] + b[3]) / 2.0 < mid_y]
            bot_blocks = [b for b in raw_blocks if (b[1] + b[3]) / 2.0 >= mid_y]
            seq_pages.append(top_blocks)
            seq_pages.append(bot_blocks)
            continue
            
        # Handling lop-12 inverted page 84 (page 85)
        if book_id == "lop-12" and idx == 84:
            # 180 degree rotated: invert coordinates
            raw_blocks = page.get_text("blocks")
            inverted_blocks = []
            for b in raw_blocks:
                # b = (x0, y0, x1, y1, text, bno, btype)
                nx0 = w - b[2]
                ny0 = h - b[3]
                nx1 = w - b[0]
                ny1 = h - b[1]
                inverted_blocks.append((nx0, ny0, nx1, ny1, b[4], b[5], b[6]))
            inverted_blocks.sort(key=lambda b: (round(b[1] / 15), b[0]))
            seq_pages.append(inverted_blocks)
            continue
            
        # Check if spread (w > h)
        if w > h:
            mid_x = w / 2.0
            raw_blocks = page.get_text("blocks")
            left = [b for b in raw_blocks if (b[0] + b[2]) / 2.0 < mid_x]
            right = [b for b in raw_blocks if (b[0] + b[2]) / 2.0 >= mid_x]
            # sort vertically
            left.sort(key=lambda b: (round(b[1] / 15), b[0]))
            right.sort(key=lambda b: (round(b[1] / 15), b[0]))
            seq_pages.append(left)
            seq_pages.append(right)
        else:
            raw_blocks = page.get_text("blocks")
            raw_blocks.sort(key=lambda b: (round(b[1] / 15), b[0]))
            seq_pages.append(raw_blocks)
            
    return seq_pages

print("Loaded page blocks extractor")
for bid, pdf in [("lop-10", "lop-10-tri-tue-nhan-tao.pdf"), ("lop-11", "lop-11-tri-tue-nhan-tao.pdf"), ("lop-12", "lop-12-tri-tue-nhan-tao.pdf")]:
    pages = get_page_blocks(pdf, bid)
    print(f"Book {bid}: {len(pages)} sequential pages extracted")
