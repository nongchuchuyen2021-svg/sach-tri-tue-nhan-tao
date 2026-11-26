import pymupdf
from pathlib import Path

doc = pymupdf.open("lop-10-tri-tue-nhan-tao.pdf")
print("Page 9 text:")
print(doc[9].get_text()[:600])

print("\n--- Page 10 text: ---")
print(doc[10].get_text()[:600])

print("\n--- Page 37 text: ---")
print(doc[37].get_text()[:600])
