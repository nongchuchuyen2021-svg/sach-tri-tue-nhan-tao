import pymupdf
import cv2
import numpy as np
from pathlib import Path

doc = pymupdf.open('lop-10-tri-tue-nhan-tao.pdf')

def get_300dpi_page(pdf_idx):
    page = doc[pdf_idx]
    pix = page.get_pixmap(dpi=300)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR), page.rect.width, page.rect.height

# Let's test P4 (Bài 1)
img4, w4, h4 = get_300dpi_page(4)
print(f"P4 300 DPI size: {img4.shape[1]}x{img4.shape[0]}")
# Right page is from width//2 to width
half_w4 = img4.shape[1] // 2
right_p4 = img4[:, half_w4:]
scale_x4 = half_w4 / (w4 / 2.0)
scale_y4 = img4.shape[0] / h4

# Hinh 1.1 coordinates in PDF on right half:
# x in [835, 1025] -> relative to right half: x_rel in [835 - 557.6, 1025 - 557.6] = [277.4, 467.4]
# y in [210, 405]
crop_h1_1 = right_p4[int(205 * scale_y4):int(408 * scale_y4), int(270 * scale_x4):int(475 * scale_x4)]
print(f"Hinh 1.1 at 300 DPI: {crop_h1_1.shape[1]}x{crop_h1_1.shape[0]}")
cv2.imwrite("scripts/test_300dpi_h1_1.png", crop_h1_1)

# Let's test P7 (Bài 2)
img7, w7, h7 = get_300dpi_page(7)
half_w7 = img7.shape[1] // 2
left_p7 = img7[:, :half_w7]
right_p7 = img7[:, half_w7:]
scale_x7 = half_w7 / (w7 / 2.0)
scale_y7 = img7.shape[0] / h7

# Hinh 2.1: left page, caption is at y=283..296, x=216..396
# The illustration is from y=48 to y=280, x=80 to x=520
crop_h2_1 = left_p7[int(48 * scale_y7):int(280 * scale_y7), int(75 * scale_x7):int(525 * scale_x7)]
print(f"Hinh 2.1 at 300 DPI: {crop_h2_1.shape[1]}x{crop_h2_1.shape[0]}")
cv2.imwrite("scripts/test_300dpi_h2_1.png", crop_h2_1)

# Hinh 2.2: right page, caption is at y=285..298
# The diagram is from y=48 to y=282, x in [600, 1030] -> rel x in [40, 470]
crop_h2_2 = right_p7[int(48 * scale_y7):int(282 * scale_y7), int(35 * scale_x7):int(480 * scale_x7)]
print(f"Hinh 2.2 at 300 DPI: {crop_h2_2.shape[1]}x{crop_h2_2.shape[0]}")
cv2.imwrite("scripts/test_300dpi_h2_2.png", crop_h2_2)
