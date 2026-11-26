import pymupdf
import re

doc = pymupdf.open('lop-10-tri-tue-nhan-tao.pdf')

print("Mapping all figures across lop-10:")

# For each PDF page, find captions and print their exact context
for pdf_idx in range(len(doc)):
    page = doc[pdf_idx]
    w, h = page.rect.width, page.rect.height
    is_spread = w > h
    mid_x = w / 2.0 if is_spread else w
    
    blocks = page.get_text('blocks')
    for b in blocks:
        txt = b[4].strip()
        m = re.search(r'H[ìi]nh\s+(\d+\.\d+[\.\:]?\s*[^\n\r]*)', txt, re.IGNORECASE)
        if m:
            side = "left" if ((b[0]+b[2])/2.0 < mid_x) else "right"
            rel_x0 = b[0] if side == "left" or not is_spread else b[0] - mid_x
            rel_x1 = b[2] if side == "left" or not is_spread else b[2] - mid_x
            print(f"PDF P{pdf_idx} ({side}): bbox=[{rel_x0:.1f}, {b[1]:.1f}, {rel_x1:.1f}, {b[3]:.1f}] -> {m.group(0)[:60]}")
