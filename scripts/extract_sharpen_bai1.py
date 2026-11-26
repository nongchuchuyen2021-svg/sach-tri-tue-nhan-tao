import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "images" / "lop-10" / "bai-1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load full debug pages
im_p8 = Image.open("scripts/debug_page_8.png")
im_p9 = Image.open("scripts/debug_page_9.png")
im_p10 = Image.open("scripts/debug_page_10.png")
im_p11 = Image.open("scripts/debug_page_11.png")
im_p12 = Image.open("scripts/debug_page_12.png")

def auto_trim_margins(im, threshold=242):
    arr = np.asarray(im)
    is_white = (arr >= threshold).all(axis=2)
    non_white_rows = np.where(~is_white.all(axis=1))[0]
    non_white_cols = np.where(~is_white.all(axis=0))[0]
    if len(non_white_rows) == 0 or len(non_white_cols) == 0:
        return im
    y0 = max(0, non_white_rows[0] - 4)
    y1 = min(im.height, non_white_rows[-1] + 5)
    x0 = max(0, non_white_cols[0] - 4)
    x1 = min(im.width, non_white_cols[-1] + 5)
    return im.crop((x0, y0, x1, y1))

def enhance_and_sharpen(im, scale_factor=1.6):
    """
    Làm nét và nâng cao chất lượng ảnh:
    - Xoá nhiễu nền scanner (paper/CamScanner yellow/grey tint)
    - Phóng to độ nét cao với thuật toán Lanczos
    - Tăng độ sắc nét viền (UnsharpMask + Sharpness filter)
    - Tinh chỉnh tương phản và màu sắc tươi sáng
    """
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    # Whiten scanner background
    max_c = np.max(arr, axis=2)
    min_c = np.min(arr, axis=2)
    sat = max_c - min_c
    is_bg = (min_c >= 236) & (sat <= 14)
    arr[is_bg] = 255.0
    cleaned = Image.fromarray(arr.astype(np.uint8))
    
    # Scale up with Lanczos for retina clarity
    new_w = int(cleaned.width * scale_factor)
    new_h = int(cleaned.height * scale_factor)
    resized = cleaned.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Unsharp Mask for fine details
    usm = resized.filter(ImageFilter.UnsharpMask(radius=2.0, percent=150, threshold=2))
    
    # Sharpness enhancement
    sharp = ImageEnhance.Sharpness(usm).enhance(1.4)
    
    # Contrast enhancement
    contrast = ImageEnhance.Contrast(sharp).enhance(1.15)
    
    # Color vibrancy
    final_img = ImageEnhance.Color(contrast).enhance(1.08)
    
    return final_img

# 1. Page 8: Tình huống Khởi động (Bạn Minh)
scale_x8 = im_p8.width / 557.64
scale_y8 = im_p8.height / 788.4
crop_p8 = im_p8.crop((int(375 * scale_x8), int(360 * scale_y8), int(530 * scale_x8), int(465 * scale_y8)))
crop_p8 = auto_trim_margins(crop_p8)
img1 = enhance_and_sharpen(crop_p8, 1.6)
img1.save(OUT_DIR / "khoi-dong-ban-minh.webp", "WEBP", quality=92, method=6)
img1.save(OUT_DIR / "khoi-dong-ban-minh.png")
print("1. Saved khoi-dong-ban-minh:", img1.size)

# 2. Page 9: Hình 1.1 - Nhận dạng sinh trắc của điện thoại thông minh
scale_x9 = im_p9.width / 557.64
scale_y9 = im_p9.height / 788.4
# We crop the phone and biometric unlock graphics neatly above the caption
crop_p9 = im_p9.crop((int(275 * scale_x9), int(220 * scale_y9), int(485 * scale_x9), int(405 * scale_y9)))
crop_p9 = auto_trim_margins(crop_p9)
img2 = enhance_and_sharpen(crop_p9, 1.5)
img2.save(OUT_DIR / "hinh-1-1-nhan-dang-sinh-trac.webp", "WEBP", quality=92, method=6)
img2.save(OUT_DIR / "hinh-1-1-nhan-dang-sinh-trac.png")
print("2. Saved hinh-1-1-nhan-dang-sinh-trac:", img2.size)

# 3. Page 10: Minh họa phân biệt trí thông minh con người và AI
scale_x10 = im_p10.width / 565.0
scale_y10 = im_p10.height / 798.84
crop_p10 = im_p10.crop((int(370 * scale_x10), int(285 * scale_y10), int(530 * scale_x10), int(430 * scale_y10)))
crop_p10 = auto_trim_margins(crop_p10)
img3 = enhance_and_sharpen(crop_p10, 1.6)
img3.save(OUT_DIR / "tri-thong-minh-nguoi-va-ai.webp", "WEBP", quality=92, method=6)
img3.save(OUT_DIR / "tri-thong-minh-nguoi-va-ai.png")
print("3. Saved tri-thong-minh-nguoi-va-ai:", img3.size)

# 4. Page 11: Minh họa AI hẹp và AI tổng quát (Robot AGI)
scale_x11 = im_p11.width / 565.0
scale_y11 = im_p11.height / 798.84
crop_p11 = im_p11.crop((int(360 * scale_x11), int(380 * scale_y11), int(530 * scale_x11), int(530 * scale_y11)))
crop_p11 = auto_trim_margins(crop_p11)
img4 = enhance_and_sharpen(crop_p11, 1.6)
img4.save(OUT_DIR / "ai-hep-va-ai-tong-quat.webp", "WEBP", quality=92, method=6)
img4.save(OUT_DIR / "ai-hep-va-ai-tong-quat.png")
print("4. Saved ai-hep-va-ai-tong-quat:", img4.size)

# 5. Page 12: Minh họa Ô tô tự lái (Tesla / Smart Car) trong phần Vận dụng
scale_x12 = im_p12.width / 557.64
scale_y12 = im_p12.height / 786.2
crop_p12 = im_p12.crop((int(80 * scale_x12), int(230 * scale_y12), int(500 * scale_x12), int(480 * scale_y12)))
crop_p12 = auto_trim_margins(crop_p12)
img5 = enhance_and_sharpen(crop_p12, 1.5)
img5.save(OUT_DIR / "o-to-tu-lai-van-dung.webp", "WEBP", quality=92, method=6)
img5.save(OUT_DIR / "o-to-tu-lai-van-dung.png")
print("5. Saved o-to-tu-lai-van-dung:", img5.size)

print("\nALL 5 FIGURES EXTRACTED, SHARPENED AND SAVED SUCCESSFULLY!")
