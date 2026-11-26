import cv2
import numpy as np

# Test on o-to-tu-lai-van-dung.webp
p = "assets/images/lop-10/bai-1/o-to-tu-lai-van-dung.webp"
img = cv2.imread(p)

# 1. Edge-preserving smoothing to wipe out halftone dots completely
smooth = cv2.edgePreservingFilter(img, flags=cv2.RECURS_FILTER, sigma_s=40, sigma_r=0.25)

# 2. Sharpen edges only
blur = cv2.GaussianBlur(smooth, (0, 0), sigmaX=2.0)
sharp = cv2.addWeighted(smooth, 1.5, blur, -0.5, 0)

# 3. Enhance vibrance/contrast
hsv = cv2.cvtColor(sharp, cv2.COLOR_BGR2HSV).astype(np.float32)
# slight contrast stretch on V
v = hsv[:, :, 2]
p2, p98 = np.percentile(v, 2), np.percentile(v, 98)
if p98 > p2:
    hsv[:, :, 2] = np.clip((v - p2) * 255.0 / (p98 - p2), 0, 255)
# boost saturation slightly
hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.15, 0, 255)
enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

cv2.imwrite("assets/images/lop-10/bai-1/o-to-tu-lai-van-dung.webp", enhanced, [cv2.IMWRITE_WEBP_QUALITY, 95])
print("Processed o-to-tu-lai-van-dung with edgePreservingFilter + contrast stretch!")
