import pymupdf

doc = pymupdf.open("lop-10-tri-tue-nhan-tao.pdf")
page = doc[37]
w, h = page.rect.width, page.rect.height
print("Page 37 width:", w, "height:", h)

blocks = page.get_text("blocks")
for b in blocks:
    print(f"[{b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}]: {b[4][:80]!r}")
