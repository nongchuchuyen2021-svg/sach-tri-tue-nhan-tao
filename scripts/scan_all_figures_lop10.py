import pymupdf
import re
import json

doc = pymupdf.open('lop-10-tri-tue-nhan-tao.pdf')

figures_found = []

for pdf_idx, page in enumerate(doc):
    w, h = page.rect.width, page.rect.height
    is_spread = w > h
    mid_x = w / 2.0 if is_spread else w
    
    blocks = page.get_text('blocks')
    for b in blocks:
        txt = b[4].strip()
        # Look for Hình X.Y
        matches = re.finditer(r'(H[ìi]nh\s+\d+\.\d+[\.\:]?\s*[^\n\r]*)', txt, re.IGNORECASE)
        for m in matches:
            cap = m.group(1).strip()
            # Determine if left or right page in spread
            if is_spread:
                page_side = "left" if (b[0] + b[2]) / 2.0 < mid_x else "right"
            else:
                page_side = "single"
            figures_found.append({
                "pdf_idx": pdf_idx,
                "side": page_side,
                "bbox": [round(x, 1) for x in b[:4]],
                "caption": cap
            })

print(f"Total figure captions found in lop-10: {len(figures_found)}")
for f in figures_found:
    print(f"PDF {f['pdf_idx']} ({f['side']}) bbox={f['bbox']}: {f['caption']}")
