import os
import re
import json
from pathlib import Path
import pymupdf
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_BASE = ROOT / "assets" / "images" / "lop-10"
IMG_BASE.mkdir(parents=True, exist_ok=True)

def super_sharpen_image_array(img, scale=1.5):
    """
    OpenCV 3x Super-Sharpening Pipeline:
    1. Denoise halftone print screen dots with bilateral filter
    2. Whiten scanner background
    3. Multi-scale Unsharp Masking + Laplacian edge matrix
    4. Auto-levels contrast & saturation stretch
    5. HiDPI Lanczos upscaling
    """
    # Whiten background
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b, g, r = cv2.split(img)
    diff = np.maximum(np.maximum(np.abs(b - g), np.abs(g - r)), np.abs(r - b))
    img[(gray > 228) & (diff < 15)] = [255, 255, 255]
    
    # Bilateral filter
    denoised = cv2.bilateralFilter(img, d=7, sigmaColor=40, sigmaSpace=40)
    
    # Lanczos upscaling
    h, w = denoised.shape[:2]
    new_w, new_h = int(w * scale), int(h * scale)
    upscaled = cv2.resize(denoised, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # Multi-scale Unsharp Masking
    blur = cv2.GaussianBlur(upscaled, (0, 0), sigmaX=1.8, sigmaY=1.8)
    sharp1 = cv2.addWeighted(upscaled, 1.6, blur, -0.6, 0)
    
    # Laplacian edge enhancement
    lap_kernel = np.array([
        [-0.5, -1.0, -0.5],
        [-1.0,  7.0, -1.0],
        [-0.5, -1.0, -0.5]
    ], dtype=np.float32)
    sharp2 = cv2.filter2D(sharp1, -1, lap_kernel * 0.15 + np.eye(3)[1,1] * 0.85)
    
    # Contrast & vibrancy
    hsv = cv2.cvtColor(sharp2, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.12, 0, 255)
    v = hsv[:, :, 2]
    p_low, p_high = np.percentile(v, 2), np.percentile(v, 98)
    if p_high > p_low:
        v = np.clip((v - p_low) * 255.0 / (p_high - p_low), 0, 255)
    hsv[:, :, 2] = v
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    # Final background whiten
    gray_res = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    b_r, g_r, r_r = cv2.split(result)
    diff_res = np.maximum(np.maximum(np.abs(b_r - g_r), np.abs(g_r - r_r)), np.abs(r_r - b_r))
    result[(gray_res > 240) & (diff_res < 12)] = [255, 255, 255]
    
    return result

print("Sharpness engine ready")
