import pymupdf

doc = pymupdf.open("lop-10-tri-tue-nhan-tao.pdf")
page = doc[9]
w, h = page.rect.width, page.rect.height
print("Page 9 width:", w, "height:", h)

blocks = page.get_text("blocks")
for b in blocks:
    # check right side
    if b[0] > w / 2:
        print(f"[{b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}]: {b[4][:100]!r}")
