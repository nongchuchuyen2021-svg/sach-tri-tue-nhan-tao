import pymupdf
import cv2
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
doc = pymupdf.open(ROOT / "lop-10-tri-tue-nhan-tao.pdf")

def enhance_textbook_figure(img):
    if img is None or img.size == 0:
        return img
    denoised = cv2.bilateralFilter(img, d=5, sigmaColor=30, sigmaSpace=30)
    hsv = cv2.cvtColor(denoised, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    bg_mask = (v > 218) & (s < 28)
    denoised[bg_mask] = [255, 255, 255]
    p_low = np.percentile(v[~bg_mask] if np.any(~bg_mask) else v, 1)
    p_high = 250.0
    if p_high > p_low:
        v_stretched = np.clip((v - p_low) * 255.0 / (p_high - p_low), 0, 255)
        hsv[:, :, 2] = np.where(bg_mask, 255.0, v_stretched)
    hsv[:, :, 1] = np.where(bg_mask, 0, np.clip(hsv[:, :, 1] * 1.15, 0, 255))
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    blur_fine = cv2.GaussianBlur(enhanced, (0, 0), sigmaX=1.5, sigmaY=1.5)
    sharp_fine = cv2.addWeighted(enhanced, 1.45, blur_fine, -0.45, 0)
    blur_med = cv2.GaussianBlur(sharp_fine, (0, 0), sigmaX=3.0, sigmaY=3.0)
    sharp_final = cv2.addWeighted(sharp_fine, 1.25, blur_med, -0.25, 0)
    gray_fin = cv2.cvtColor(sharp_final, cv2.COLOR_BGR2GRAY)
    sharp_final[gray_fin > 242] = [255, 255, 255]
    return sharp_final

def auto_trim_edges(img, threshold=245):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    non_white = gray < threshold
    rows = np.where(non_white.any(axis=1))[0]
    cols = np.where(non_white.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return img
    y0 = max(0, rows[0] - 6)
    y1 = min(img.shape[0], rows[-1] + 7)
    x0 = max(0, cols[0] - 6)
    x1 = min(img.shape[1], cols[-1] + 7)
    return img[y0:y1, x0:x1]

EXTRA_FIGURES = [
    {
        "bai": 2, "id": "hinh-2-9", "caption": "Hình 2.9. Giao diện kết quả của ChatGPT khi tạo đoạn văn",
        "pdf": 9, "side": "right", "coords": [50, 320, 450, 515]
    },
    {
        "bai": 11, "id": "hinh-11-2", "caption": "Hình 11.2. Ví dụ kết quả chạy hai ô mã của Google Colab",
        "pdf": 37, "side": "left", "coords": [140, 390, 485, 485]
    },
    {
        "bai": 11, "id": "hinh-11-3", "caption": "Hình 11.3. Giao diện code, kết quả và ghi chú trong Google Colab",
        "pdf": 37, "side": "left", "coords": [140, 555, 485, 665]
    }
]

for fdef in EXTRA_FIGURES:
    pno = fdef["pdf"]
    page = doc[pno]
    pix = page.get_pixmap(dpi=300)
    img_page = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
    img_page = cv2.cvtColor(img_page, cv2.COLOR_RGB2BGR)
    
    w_pdf, h_pdf = page.rect.width, page.rect.height
    is_spread = w_pdf > h_pdf
    
    if is_spread:
        half_w = img_page.shape[1] // 2
        page_side_img = img_page[:, :half_w] if fdef["side"] == "left" else img_page[:, half_w:]
        scale_x = half_w / (w_pdf / 2.0)
    else:
        page_side_img = img_page
        scale_x = img_page.shape[1] / w_pdf
        
    scale_y = img_page.shape[0] / h_pdf
    
    x0, y0, x1, y1 = fdef["coords"]
    px0, py0, px1, py1 = int(x0 * scale_x), int(y0 * scale_y), int(x1 * scale_x), int(y1 * scale_y)
    
    crop = page_side_img[py0:py1, px0:px1]
    trimmed = auto_trim_edges(crop)
    enhanced = enhance_textbook_figure(trimmed)
    
    bai_dir = ROOT / "assets" / "images" / "lop-10" / f"bai-{fdef['bai']}"
    bai_dir.mkdir(parents=True, exist_ok=True)
    out_webp = bai_dir / f"{fdef['id']}.webp"
    cv2.imwrite(str(out_webp), enhanced, [cv2.IMWRITE_WEBP_QUALITY, 95])
    print(f"✓ Saved Bai {fdef['bai']} -> {fdef['id']}.webp ({enhanced.shape[1]}x{enhanced.shape[0]} px, {out_webp.stat().st_size / 1024:.1f} KB)")

# Also ensure hinh-2-3.webp and hinh-2-4.webp exist (copy of hinh-2-3-2-4.webp)
b2_comb = ROOT / "assets" / "images" / "lop-10" / "bai-2" / "hinh-2-3-2-4.webp"
if b2_comb.exists():
    with open(b2_comb, "rb") as f_in:
        data = f_in.read()
    with open(ROOT / "assets" / "images" / "lop-10" / "bai-2" / "hinh-2-3.webp", "wb") as f_out:
        f_out.write(data)
    with open(ROOT / "assets" / "images" / "lop-10" / "bai-2" / "hinh-2-4.webp", "wb") as f_out:
        f_out.write(data)
    print("✓ Synced hinh-2-3.webp and hinh-2-4.webp from hinh-2-3-2-4.webp")
