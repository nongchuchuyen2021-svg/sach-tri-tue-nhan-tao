import re
import pymupdf

doc = pymupdf.open("lop-10-tri-tue-nhan-tao.pdf")
all_found = []
for pno in range(len(doc)):
    text = doc[pno].get_text()
    matches = re.findall(r'(H[ìi]nh\s+(\d+)[\.\:](\d+)[^\n\.\,\;]*)', text, re.IGNORECASE)
    for m in matches:
        all_found.append({
            "pdf_page": pno,
            "text": m[0].strip(),
            "bai": int(m[1]),
            "hinh": int(m[2])
        })

print(f"Total 'Hình X.Y' found in PDF: {len(all_found)}")
for item in all_found:
    print(f"Page {item['pdf_page']}: Bai {item['bai']} Hinh {item['hinh']} -> {item['text']}")
