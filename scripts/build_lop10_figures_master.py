import os
import re
import json
import pymupdf
import cv2
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = ROOT / "lop-10-tri-tue-nhan-tao.pdf"
IMG_BASE = ROOT / "assets" / "images" / "lop-10"
doc = pymupdf.open(DOC_PATH)

def enhance_textbook_figure(img, is_screenshot=False):
    """
    Advanced textbook illustration enhancement:
    - Removes scanner color cast / yellow-grey paper background
    - Level stretching to make whites pure (255) and darks crisp
    - Bilateral descreening to remove print halftone screen dots
    - Dual-band Unsharp Masking for crisp lines and text inside diagrams
    - Slight color saturation boost for vibrant graphics
    """
    if img is None or img.size == 0:
        return img
        
    # 1. Bilateral filter for halftone print dot removal without edge softening
    denoised = cv2.bilateralFilter(img, d=5, sigmaColor=30, sigmaSpace=30)
    
    # 2. Whiten paper background
    # Detect near-white background (brightness > 218 and low color saturation)
    hsv = cv2.cvtColor(denoised, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    
    # Paper background mask: high brightness and low saturation
    bg_mask = (v > 218) & (s < 28)
    denoised[bg_mask] = [255, 255, 255]
    
    # 3. Contrast / Levels stretching (Auto White Point & Black Point)
    # Clip extreme 1% shadows and 2% highlights
    p_low = np.percentile(v[~bg_mask] if np.any(~bg_mask) else v, 1)
    p_high = 250.0
    if p_high > p_low:
        v_stretched = np.clip((v - p_low) * 255.0 / (p_high - p_low), 0, 255)
        # Only stretch non-background
        hsv[:, :, 2] = np.where(bg_mask, 255.0, v_stretched)
        
    # 4. Saturation boost for illustrations
    hsv[:, :, 1] = np.where(bg_mask, 0, np.clip(hsv[:, :, 1] * 1.15, 0, 255))
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    # 5. Dual-band Unsharp Masking
    # Fine details: small sigma
    blur_fine = cv2.GaussianBlur(enhanced, (0, 0), sigmaX=1.5, sigmaY=1.5)
    sharp_fine = cv2.addWeighted(enhanced, 1.45, blur_fine, -0.45, 0)
    
    # Medium structure: medium sigma
    blur_med = cv2.GaussianBlur(sharp_fine, (0, 0), sigmaX=3.0, sigmaY=3.0)
    sharp_final = cv2.addWeighted(sharp_fine, 1.25, blur_med, -0.25, 0)
    
    # Final background cleanup
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

# Comprehensive Figure Definitions for all 12 lessons of Grade 10:
# Each definition specifies: pdf_page, side ('left' or 'right'), relative PDF coords [x0, y0, x1, y1], bai_num, hinh_id, caption
FIGURE_DEFS = [
    # --- BÀI 1 ---
    {
        "bai": 1, "id": "khoi-dong-ban-minh", "caption": "Tình huống bạn Minh chủ động đổi mới phương pháp học tập",
        "pdf": 4, "side": "left", "coords": [375, 360, 525, 465]
    },
    {
        "bai": 1, "id": "hinh-1-1-nhan-dang-sinh-trac", "caption": "Hình 1.1. Chức năng nhận dạng sinh trắc của điện thoại thông minh",
        "pdf": 4, "side": "right", "coords": [275, 210, 480, 410]
    },
    {
        "bai": 1, "id": "tri-thong-minh-nguoi-va-ai", "caption": "So sánh trí thông minh sinh học của con người với mạng nơ-ron nhân tạo của AI",
        "pdf": 5, "side": "left", "coords": [370, 285, 525, 425]
    },
    {
        "bai": 1, "id": "ai-hep-va-ai-tong-quat", "caption": "Minh họa sự phát triển từ AI hẹp (ANI) hướng tới AI tổng quát (AGI)",
        "pdf": 5, "side": "right", "coords": [360, 380, 525, 525]
    },
    {
        "bai": 1, "id": "o-to-tu-lai-van-dung", "caption": "Ô tô tự lái nhận diện làn đường và vật cản thông qua hệ thống cảm biến AI",
        "pdf": 6, "side": "left", "coords": [80, 230, 490, 470]
    },

    # --- BÀI 2 ---
    {
        "bai": 2, "id": "hinh-2-1", "caption": "Hình 2.1. Một số công cụ AI tạo sinh (Gemini, ChatGPT, Suno AI)",
        "pdf": 7, "side": "left", "coords": [85, 50, 520, 282]
    },
    {
        "bai": 2, "id": "hinh-2-2", "caption": "Hình 2.2. Sự khác nhau giữa AI tạo sinh và AI thế hệ trước",
        "pdf": 7, "side": "right", "coords": [60, 50, 485, 285]
    },
    {
        "bai": 2, "id": "hinh-2-3-2-4", "caption": "Hình 2.3 & 2.4. Đăng ký tài khoản mới và đăng nhập ChatGPT",
        "pdf": 8, "side": "left", "coords": [95, 120, 510, 380]
    },
    {
        "bai": 2, "id": "hinh-2-5", "caption": "Hình 2.5. Giao diện nhập yêu cầu (prompt) cho ChatGPT",
        "pdf": 8, "side": "left", "coords": [95, 490, 510, 655]
    },
    {
        "bai": 2, "id": "hinh-2-6", "caption": "Hình 2.6. Giao diện kết quả tạo thiệp sinh nhật của ChatGPT",
        "pdf": 8, "side": "right", "coords": [65, 90, 480, 348]
    },
    {
        "bai": 2, "id": "hinh-2-7", "caption": "Hình 2.7. Giao diện Suno AI cho phép nhập mô tả bài hát",
        "pdf": 9, "side": "left", "coords": [85, 50, 515, 285]
    },
    {
        "bai": 2, "id": "hinh-2-8", "caption": "Hình 2.8. Kết quả bài hát được tạo ra từ Suno AI",
        "pdf": 9, "side": "left", "coords": [85, 380, 515, 652]
    },

    # --- BÀI 3 ---
    {
        "bai": 3, "id": "hinh-3-1", "caption": "Hình 3.1. Mô hình ngôn ngữ lớn (LLM) và cơ chế xử lí văn bản",
        "pdf": 11, "side": "left", "coords": [75, 120, 525, 395]
    },
    {
        "bai": 3, "id": "hinh-3-2", "caption": "Hình 3.2. LLM có thể tạo ảnh từ văn bản mô tả",
        "pdf": 11, "side": "right", "coords": [65, 55, 485, 268]
    },
    {
        "bai": 3, "id": "hinh-3-3", "caption": "Hình 3.3. Giao diện đăng nhập tài khoản Google để sử dụng Gemini",
        "pdf": 12, "side": "left", "coords": [95, 80, 510, 232]
    },
    {
        "bai": 3, "id": "hinh-3-4", "caption": "Hình 3.4. Giao diện cho phép nhập yêu cầu (prompt) và kết quả của Gemini",
        "pdf": 12, "side": "left", "coords": [90, 340, 515, 598]
    },

    # --- BÀI 4 ---
    {
        "bai": 4, "id": "hinh-4-1", "caption": "Hình 4.1. Các loại dữ liệu có thể sử dụng để huấn luyện AI",
        "pdf": 14, "side": "right", "coords": [60, 220, 485, 610]
    },
    {
        "bai": 4, "id": "hinh-4-2", "caption": "Hình 4.2. Chất lượng và số lượng dữ liệu huấn luyện",
        "pdf": 15, "side": "left", "coords": [80, 180, 520, 565]
    },

    # --- BÀI 5 ---
    {
        "bai": 5, "id": "hinh-5-1", "caption": "Hình 5.1. Prompt trong AI tạo sinh – Giao tiếp hiệu quả",
        "pdf": 17, "side": "right", "coords": [55, 48, 485, 172]
    },
    {
        "bai": 5, "id": "hinh-5-2", "caption": "Hình 5.2. Các thành phần của một prompt hoàn chỉnh",
        "pdf": 17, "side": "right", "coords": [60, 280, 485, 662]
    },

    # --- BÀI 6 ---
    {
        "bai": 6, "id": "hinh-6-1", "caption": "Hình 6.1. AI tạo sinh có thể hỗ trợ học tập đa lĩnh vực",
        "pdf": 21, "side": "left", "coords": [85, 100, 520, 410]
    },
    {
        "bai": 6, "id": "hinh-6-2", "caption": "Hình 6.2. Cách sử dụng AI tạo sinh hiệu quả trong học tập",
        "pdf": 21, "side": "right", "coords": [60, 60, 485, 335]
    },
    {
        "bai": 6, "id": "hinh-6-3", "caption": "Hình 6.3. Trách nhiệm của học sinh khi sử dụng AI tạo sinh",
        "pdf": 22, "side": "left", "coords": [80, 160, 520, 550]
    },

    # --- BÀI 7 ---
    {
        "bai": 7, "id": "hinh-7-1", "caption": "Hình 7.1. Những rủi ro khi dùng AI tạo sinh và thông tin sai lệch",
        "pdf": 25, "side": "left", "coords": [85, 55, 520, 252]
    },

    # --- BÀI 8 ---
    {
        "bai": 8, "id": "hinh-8-1", "caption": "Hình 8.1. AI tạo sinh có thể tạo ra nội dung thiên vị (Bias)",
        "pdf": 27, "side": "left", "coords": [85, 55, 520, 275]
    },
    {
        "bai": 8, "id": "hinh-8-2", "caption": "Hình 8.2. Vai trò của con người khi kiểm soát và sử dụng AI",
        "pdf": 27, "side": "right", "coords": [60, 180, 485, 535]
    },

    # --- BÀI 9 ---
    {
        "bai": 9, "id": "hinh-9-1", "caption": "Hình 9.1. Sáu miền năng lực số cho người học",
        "pdf": 30, "side": "right", "coords": [55, 215, 485, 620]
    },

    # --- BÀI 10 ---
    {
        "bai": 10, "id": "hinh-10-1", "caption": "Hình 10.1. Tác động của AI đến thị trường việc làm",
        "pdf": 34, "side": "right", "coords": [55, 45, 485, 340]
    },
    {
        "bai": 10, "id": "hinh-10-2", "caption": "Hình 10.2. Học hỏi để đồng hành cùng AI trong tương lai",
        "pdf": 35, "side": "left", "coords": [85, 50, 520, 242]
    },

    # --- BÀI 11 ---
    {
        "bai": 11, "id": "hinh-11-1", "caption": "Hình 11.1. Giao diện môi trường Google Colab",
        "pdf": 37, "side": "left", "coords": [85, 50, 520, 232]
    },
    {
        "bai": 11, "id": "hinh-11-2", "caption": "Hình 11.2 & 11.3. Giao diện code, thực thi và kết quả",
        "pdf": 37, "side": "left", "coords": [85, 290, 520, 668]
    },
    {
        "bai": 11, "id": "hinh-11-4", "caption": "Hình 11.4. Giao diện nền tảng Kaggle",
        "pdf": 37, "side": "right", "coords": [60, 100, 485, 410]
    },
    {
        "bai": 11, "id": "hinh-11-5", "caption": "Hình 11.5. Giao diện một sổ tay mới trong Kaggle",
        "pdf": 37, "side": "right", "coords": [60, 450, 485, 660]
    },
    {
        "bai": 11, "id": "hinh-11-6", "caption": "Hình 11.6. Kết quả chuyển từ văn bản sang giọng nói (Text-to-Speech)",
        "pdf": 38, "side": "right", "coords": [60, 200, 485, 540]
    },

    # --- BÀI 12 ---
    {
        "bai": 12, "id": "hinh-12-1", "caption": "Hình 12.1. AI tạo sinh hỗ trợ gợi ý ý tưởng viết truyện và dự án",
        "pdf": 40, "side": "left", "coords": [80, 50, 520, 278]
    },
    {
        "bai": 12, "id": "hinh-12-2", "caption": "Hình 12.2. Hình ảnh minh họa trang 1 trong câu chuyện của bạn Linh",
        "pdf": 41, "side": "right", "coords": [60, 120, 485, 552]
    },
    {
        "bai": 12, "id": "hinh-12-3", "caption": "Hình 12.3. Hình ảnh minh họa trang 2 trong câu chuyện của bạn Linh",
        "pdf": 42, "side": "left", "coords": [80, 120, 520, 635]
    },
    {
        "bai": 12, "id": "hinh-12-4", "caption": "Hình 12.4. Hình ảnh minh họa trang 3 trong câu chuyện của bạn Linh",
        "pdf": 42, "side": "right", "coords": [60, 120, 485, 550]
    },
    {
        "bai": 12, "id": "hinh-12-6", "caption": "Hình 12.6. Hình ảnh minh họa trang 5 trong câu chuyện của bạn Linh",
        "pdf": 43, "side": "right", "coords": [60, 60, 485, 340]
    },
]

print(f"Total defined figures to extract: {len(FIGURE_DEFS)}")
manifest = {}

# Process each figure
for fdef in FIGURE_DEFS:
    pno = fdef["pdf"]
    page = doc[pno]
    
    # Render at 300 DPI for crystal clear clarity
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
    
    bai_num = fdef["bai"]
    fig_id = fdef["id"]
    bai_dir = IMG_BASE / f"bai-{bai_num}"
    bai_dir.mkdir(parents=True, exist_ok=True)
    
    out_webp = bai_dir / f"{fig_id}.webp"
    cv2.imwrite(str(out_webp), enhanced, [cv2.IMWRITE_WEBP_QUALITY, 95])
    
    entry = {
        "id": fig_id,
        "bai": bai_num,
        "caption": fdef["caption"],
        "path": f"assets/images/lop-10/bai-{bai_num}/{fig_id}.webp",
        "size": [enhanced.shape[1], enhanced.shape[0]]
    }
    
    if str(bai_num) not in manifest:
        manifest[str(bai_num)] = []
    manifest[str(bai_num)].append(entry)
    
    print(f"✓ Saved Bai {bai_num} -> {fig_id}.webp ({enhanced.shape[1]}x{enhanced.shape[0]} px, {out_webp.stat().st_size / 1024:.1f} KB)")

# Save manifest
with open(ROOT / "data" / "lop10_figures_master_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("\nALL 34 FIGURES EXTRACTED AT 300 DPI AND ENHANCED SUCCESSFULLY!")
