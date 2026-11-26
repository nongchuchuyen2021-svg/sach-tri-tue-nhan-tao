import pymupdf
import cv2
import numpy as np

doc = pymupdf.open('lop-10-tri-tue-nhan-tao.pdf')

def inspect_page_figures(pdf_idx):
    page = doc[pdf_idx]
    # Render at 300 DPI
    pix = page.get_pixmap(dpi=300)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    w_pdf, h_pdf = page.rect.width, page.rect.height
    is_spread = w_pdf > h_pdf
    
    blocks = page.get_text('blocks')
    print(f"\n==================== PDF P{pdf_idx} ({pix.width}x{pix.height}) ====================")
    for b in blocks:
        txt = b[4].strip().replace('\n', ' ')
        if 'hình' in txt.lower() or 'hinh' in txt.lower():
            print(f"  Caption: bbox=({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}) -> {txt}")
            
    # Save preview image with bounding boxes drawn
    scale_x = pix.width / w_pdf
    scale_y = pix.height / h_pdf
    
    dbg_img = img.copy()
    for b in blocks:
        txt = b[4].strip().replace('\n', ' ')
        if 'hình' in txt.lower() or 'hinh' in txt.lower():
            x0, y0, x1, y1 = int(b[0]*scale_x), int(b[1]*scale_y), int(b[2]*scale_x), int(b[3]*scale_y)
            cv2.rectangle(dbg_img, (x0, y0), (x1, y1), (0, 0, 255), 3)
            
    cv2.imwrite(f"scripts/preview_p{pdf_idx}.jpg", dbg_img)
    print(f"Saved scripts/preview_p{pdf_idx}.jpg")

for p in [4, 7, 8]:
    inspect_page_figures(p)
