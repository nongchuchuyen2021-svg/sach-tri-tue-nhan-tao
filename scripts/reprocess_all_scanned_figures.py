import cv2
import numpy as np
from pathlib import Path
import glob

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "images" / "lop-10"

DIGITAL_FIGS = {
    "hinh-1-1-nhan-dang-sinh-trac.webp",
    "khoi-dong-ban-minh.webp",
    "tri-thong-minh-nguoi-va-ai.webp"
}

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

def ultra_enhance(img):
    if img is None or img.size == 0:
        return img
        
    # 1. Edge-preserving smoothing: completely eliminates halftone print screen dots
    # while keeping sharp cartoon/diagram edges and UI text crisp
    smoothed = cv2.edgePreservingFilter(img, flags=cv2.RECURS_FILTER, sigma_s=35, sigma_r=0.25)
    
    # 2. Paper background detection & whitening
    hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    bg_mask = (v > 215) & (s < 30)
    smoothed[bg_mask] = [255, 255, 255]
    
    # 3. Dynamic contrast stretch (Levels) on non-background
    if np.any(~bg_mask):
        p_low = np.percentile(v[~bg_mask], 1.5)
        p_high = np.percentile(v[~bg_mask], 98.5)
        if p_high > p_low + 10:
            v_stretched = np.clip((v - p_low) * 255.0 / (p_high - p_low), 0, 255)
            hsv[:, :, 2] = np.where(bg_mask, 255.0, v_stretched)
            
    # 4. Color vibrance boost
    hsv[:, :, 1] = np.where(bg_mask, 0, np.clip(hsv[:, :, 1] * 1.15, 0, 255))
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    # 5. Dual-band unsharp mask on the smoothed, dot-free image
    blur = cv2.GaussianBlur(enhanced, (0, 0), sigmaX=1.8, sigmaY=1.8)
    sharpened = cv2.addWeighted(enhanced, 1.45, blur, -0.45, 0)
    
    # 6. Final pure white threshold
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    sharpened[gray > 240] = [255, 255, 255]
    
    return auto_trim_edges(sharpened)

count = 0
all_files = sorted(BASE.glob("*/*.webp"))
for p in all_files:
    if p.name in DIGITAL_FIGS:
        print(f"Skipping digital master: {p.name}")
        continue
    img = cv2.imread(str(p))
    if img is None:
        continue
    proc = ultra_enhance(img)
    cv2.imwrite(str(p), proc, [cv2.IMWRITE_WEBP_QUALITY, 95])
    count += 1
    print(f"✓ Enhanced: {p.relative_to(ROOT)} ({proc.shape[1]}x{proc.shape[0]} px)")

print(f"\nAll {count} scanned figures successfully ultra-enhanced!")
