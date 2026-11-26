import os
import re
import json
import io
from pathlib import Path
import pymupdf
import cv2
import numpy as np
from PIL import Image
from sharpen_engine import super_sharpen_image_array

ROOT = Path(__file__).resolve().parent.parent
IMG_BASE = ROOT / "assets" / "images" / "lop-10"
DOC_PATH = ROOT / "lop-10-tri-tue-nhan-tao.pdf"

doc = pymupdf.open(DOC_PATH)

def auto_trim(img, threshold=242):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    is_white = gray >= threshold
    non_white_rows = np.where(~is_white.all(axis=1))[0]
    non_white_cols = np.where(~is_white.all(axis=0))[0]
    if len(non_white_rows) == 0 or len(non_white_cols) == 0:
        return img
    y0 = max(0, non_white_rows[0] - 6)
    y1 = min(img.shape[0], non_white_rows[-1] + 7)
    x0 = max(0, non_white_cols[0] - 6)
    x1 = min(img.shape[1], non_white_cols[-1] + 7)
    return img[y0:y1, x0:x1]

# Lesson page map for lop-10:
# Bai 1: p.8-12 (PDF 4-6)
# Bai 2: p.13-20 (PDF 6-10)
# Bai 3: p.21-27 (PDF 10-13)
# Bai 4: p.28-33 (PDF 14-16)
# Bai 5: p.34-40 (PDF 17-20)
# Bai 6: p.41-48 (PDF 20-24)
# Bai 7: p.49-52 (PDF 24-26)
# Bai 8: p.53-57 (PDF 26-28)
# Bai 9: p.58-67 (PDF 29-33)
# Bai 10: p.68-71 (PDF 34-35)
# Bai 11: p.72-78 (PDF 36-39)
# Bai 12: p.79-88 (PDF 39-44)

lesson_figures = {}

for pdf_idx, page in enumerate(doc):
    w_pdf, h_pdf = page.rect.width, page.rect.height
    is_spread = w_pdf > h_pdf
    mid_x_pdf = w_pdf / 2.0 if is_spread else w_pdf
    
    # Extract page background high-res image
    imgs_on_page = page.get_images(full=True)
    if not imgs_on_page:
        continue
    xref = imgs_on_page[0][0]
    base = doc.extract_image(xref)
    im_pil = Image.open(io.BytesIO(base["image"]))
    im_full = cv2.cvtColor(np.array(im_pil), cv2.COLOR_RGB2BGR)
    h_img, w_img = im_full.shape[:2]
    
    blocks = page.get_text('blocks')
    # Sort blocks
    for b in blocks:
        txt = b[4].strip()
        # Look for Hình X.Y
        m = re.search(r'H[ìi]nh\s+(\d+)\.(\d+)([\.\:]?\s*[^\n\r]*)', txt, re.IGNORECASE)
        if not m:
            continue
            
        bai_num = int(m.group(1))
        hinh_num = int(m.group(2))
        suffix = m.group(3).strip().lstrip(".:- ")
        full_caption = f"Hình {bai_num}.{hinh_num}. {suffix}" if suffix else f"Hình {bai_num}.{hinh_num}"
        
        # Determine side
        bx0, by0, bx1, by1 = b[:4]
        is_left = (bx0 + bx1) / 2.0 < mid_x_pdf if is_spread else True
        
        # Crop coordinates on the full image
        if is_spread:
            half_w_img = w_img // 2
            half_w_pdf = w_pdf / 2.0
            if is_left:
                page_img = im_full[:, :half_w_img]
                scale_x = half_w_img / half_w_pdf
                rel_bx0, rel_bx1 = bx0, bx1
            else:
                page_img = im_full[:, half_w_img:]
                scale_x = half_w_img / half_w_pdf
                rel_bx0, rel_bx1 = bx0 - half_w_pdf, bx1 - half_w_pdf
        else:
            page_img = im_full
            scale_x = w_img / w_pdf
            rel_bx0, rel_bx1 = bx0, bx1
            
        scale_y = page_img.shape[0] / h_pdf
        
        # The illustration is typically above the caption
        # Determine upper boundary: look for text block above this caption
        cap_top_pdf = by0
        prev_bottom_pdf = 50.0  # default top margin
        for ob in blocks:
            ob_side = (ob[0] + ob[2]) / 2.0 < mid_x_pdf if is_spread else True
            if ob_side == is_left:
                ob_bottom = ob[3]
                if ob_bottom < cap_top_pdf - 8.0:
                    if ob_bottom > prev_bottom_pdf:
                        prev_bottom_pdf = ob_bottom
                        
        # Bounding box for crop
        fig_y0 = max(0, int(prev_bottom_pdf * scale_y) + 4)
        fig_y1 = min(page_img.shape[0], int(cap_top_pdf * scale_y) - 2)
        
        # For width: take column width or caption width with padding
        col_x0 = max(0, int(35 * scale_x))
        col_x1 = min(page_img.shape[1], int((half_w_pdf if is_spread else w_pdf) * scale_x) - int(35 * scale_x))
        
        # If caption is centered / wide, use column width; if in a narrow sub-column, adjust
        crop_w = int((rel_bx1 - rel_bx0) * scale_x)
        if crop_w > page_img.shape[1] * 0.5:
            fig_x0, fig_x1 = col_x0, col_x1
        else:
            fig_x0 = max(col_x0, int(rel_bx0 * scale_x) - 40)
            fig_x1 = min(col_x1, int(rel_bx1 * scale_x) + 40)
            
        if fig_y1 - fig_y0 < 60 or fig_x1 - fig_x0 < 60:
            continue
            
        raw_crop = page_img[fig_y0:fig_y1, fig_x0:fig_x1]
        trimmed = auto_trim(raw_crop)
        
        if trimmed.shape[0] < 50 or trimmed.shape[1] < 50:
            continue
            
        # Run super sharpen pipeline
        sharpened = super_sharpen_image_array(trimmed, scale=1.5)
        
        # Save figure
        bai_dir = IMG_BASE / f"bai-{bai_num}"
        bai_dir.mkdir(parents=True, exist_ok=True)
        fig_id = f"hinh-{bai_num}-{hinh_num}"
        out_webp = bai_dir / f"{fig_id}.webp"
        cv2.imwrite(str(out_webp), sharpened, [cv2.IMWRITE_WEBP_QUALITY, 94])
        
        fig_entry = {
            "id": fig_id,
            "bai": bai_num,
            "hinh": hinh_num,
            "caption": full_caption,
            "path": f"assets/images/lop-10/bai-{bai_num}/{fig_id}.webp",
            "size": [sharpened.shape[1], sharpened.shape[0]]
        }
        
        if bai_num not in lesson_figures:
            lesson_figures[bai_num] = {}
        # Keep the best crop if multiple captions mention it
        if fig_id not in lesson_figures[bai_num] or (sharpened.shape[0] * sharpened.shape[1] > lesson_figures[bai_num][fig_id]["size"][0] * lesson_figures[bai_num][fig_id]["size"][1]):
            lesson_figures[bai_num][fig_id] = fig_entry
            print(f"✓ Extracted & Sharpened {fig_id}: {full_caption} -> {sharpened.shape[1]}x{sharpened.shape[0]}")

# Save manifest
with open(ROOT / "data" / "lop10_figures_manifest.json", "w", encoding="utf-8") as f:
    json.dump({k: list(v.values()) for k, v in lesson_figures.items()}, f, ensure_ascii=False, indent=2)

print("\nFinished extracting and sharpening all figures for Lop 10!")
