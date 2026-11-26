import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "data" / "lop10_figures_master_manifest.json"
LESSONS_PATH = ROOT / "data" / "lessons-lop-10.json"
LESSONS_DIR = ROOT / "lessons" / "lop-10"

# 1. Update manifest with extra figures
manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))

# Check Bai 2
b2_figs = manifest.get("2", [])
b2_ids = {f["id"] for f in b2_figs}
if "hinh-2-9" not in b2_ids:
    b2_figs.append({
        "id": "hinh-2-9",
        "bai": 2,
        "caption": "Hình 2.9. Giao diện kết quả của ChatGPT khi tạo đoạn văn",
        "path": "assets/images/lop-10/bai-2/hinh-2-9.webp",
        "size": [1666, 813]
    })
manifest["2"] = b2_figs

# Check Bai 11
b11_figs = manifest.get("11", [])
b11_ids = {f["id"] for f in b11_figs}
if "hinh-11-3" not in b11_ids:
    b11_figs.append({
        "id": "hinh-11-3",
        "bai": 11,
        "caption": "Hình 11.3. Giao diện code, kết quả và ghi chú trong Google Colab",
        "path": "assets/images/lop-10/bai-11/hinh-11-3.webp",
        "size": [1437, 458]
    })
manifest["11"] = b11_figs

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("✓ Updated manifest")

# 2. Process HTML files
lessons = json.load(open(LESSONS_PATH, encoding="utf-8"))

for les in lessons:
    lid = les["id"]
    m = re.match(r"bai-(\d+)", lid)
    if not m:
        continue
    bnum = int(m.group(1))
    html_file = LESSONS_DIR / f"{lid}.html"
    if not html_file.exists():
        continue
    html = html_file.read_text(encoding="utf-8")
    
    # Specific fixes per lesson:
    if bnum == 2:
        # Replace Hình 2.9 placeholder
        p_sub = """<figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-2/hinh-2-9.webp" alt="Hình 2.9. Giao diện kết quả của ChatGPT khi tạo đoạn văn" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 2.9.</strong> Giao diện kết quả của ChatGPT</figcaption>
</figure>"""
        html = re.sub(r'<figure class="lesson-figure-box">\s*<div class="figure-placeholder">.*?Hình 2\.9.*?</div>\s*</figure>', p_sub, html, flags=re.DOTALL)
        
        # Ensure hinh-2-3 references hinh-2-3-2-4 or hinh-2-3
        html = html.replace('alt="Hình 2.3. Tạo tài khoản mới"', 'alt="Hình 2.3 & 2.4. Đăng ký tài khoản mới và đăng nhập ChatGPT"')
        html = html.replace('<strong>Hình 2.3.</strong> Tạo tài khoản mới', '<strong>Hình 2.3 & 2.4.</strong> Đăng ký tài khoản mới và đăng nhập ChatGPT')
        
    elif bnum == 5:
        # Clean stray placeholder in Bai 5
        clean_p = '<p class="lesson-p">+ Hình ảnh nên có biểu tượng liên quan đến học tập (sách, bút,...), đam mê</p>'
        html = re.sub(r'<figure class="lesson-figure-box">\s*<div class="figure-placeholder">.*?Hình ảnh nên có biểu tượng.*?</div>\s*</figure>', clean_p, html, flags=re.DOTALL)
        
    elif bnum == 9:
        # Clean nested placeholder in Bai 9
        clean_f9 = """<figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-9/hinh-9-1.webp" alt="Hình 9.1. Sáu miền năng lực số cho người học" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 9.1.</strong> Sáu miền năng lực số cho người học theo khung tham chiếu năng lực số</figcaption>
</figure>"""
        html = re.sub(r'<figure class="lesson-figure-box">\s*<div class="figure-placeholder">.*?Hình 9\.1.*?</div>\s*</figure>', clean_f9, html, flags=re.DOTALL)

    elif bnum == 11:
        # Insert hinh-11-2 and hinh-11-3 if not present
        if "hinh-11-2.webp" not in html:
            figs_colab = """<figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-11/hinh-11-2.webp" alt="Hình 11.2. Ví dụ kết quả chạy hai ô mã của Google Colab" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 11.2.</strong> Ví dụ kết quả chạy hai ô mã của Google Colab</figcaption>
</figure>
<figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-11/hinh-11-3.webp" alt="Hình 11.3. Giao diện code, kết quả, ghi chú trong Google Colab" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 11.3.</strong> Giao diện code, kết quả, ghi chú trong Google Colab</figcaption>
</figure>"""
            target = '<p class="lesson-p">Đ Tổng của • và b la: 12</p>'
            if target in html:
                html = html.replace(target, target + "\n\n" + figs_colab)
            else:
                target2 = 'Hình 11.4'
                idx = html.find(target2)
                if idx != -1:
                    prev_fig = html.rfind('<figure', 0, idx)
                    if prev_fig != -1:
                        html = html[:prev_fig] + figs_colab + "\n\n" + html[prev_fig:]
                        
    # Save back
    html_file.write_text(html, encoding="utf-8")
    les["html"] = html
    print(f"✓ Finalized Bai {bnum} ({lid})")

with open(LESSONS_PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print("\nAll 12 lessons finalized and synchronized successfully!")
