import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "data" / "lop10_figures_manifest.json"
LESSONS_PATH = ROOT / "data" / "lessons-lop-10.json"

with open(MANIFEST_PATH, encoding="utf-8") as f:
    manifest = json.load(f)

with open(LESSONS_PATH, encoding="utf-8") as f:
    lessons = json.load(f)

# Loop through lessons
updated_count = 0

for les in lessons:
    # E.g. les["id"] == "bai-2-ai-tao-sinh" -> bai_num = 2
    m = re.match(r"bai-(\d+)", les["id"])
    if not m:
        continue
    bai_num = int(m.group(1))
    if bai_num == 1:
        # Bài 1 is already custom polished with all 5 figures
        continue
        
    bai_figs = manifest.get(str(bai_num), [])
    if not bai_figs:
        continue
        
    html = les.get("html", "")
    figs_inserted = 0
    
    for fig in bai_figs:
        hinh_num = fig["hinh"]
        fig_path = fig["path"]
        caption = fig["caption"]
        
        # Clean caption text
        caption_clean = re.sub(r"^H[ìi]nh\s+\d+\.\d+[\.\:]?\s*", "", caption).strip()
        if not caption_clean:
            caption_clean = f"Minh họa bài học {bai_num}.{hinh_num}"
            
        fig_html = f"""
<figure class="lesson-figure-box figure-highlight">
    <img src="{fig_path}" alt="Hình {bai_num}.{hinh_num}. {caption_clean}" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình {bai_num}.{hinh_num}.</strong> {caption_clean}</figcaption>
</figure>
"""
        # Look for placeholder or caption in text to replace
        pattern = re.compile(rf'(<figure class="lesson-figure-box">.*?Hình\s+{bai_num}\.{hinh_num}.*?</figure>)', re.DOTALL | re.IGNORECASE)
        if pattern.search(html):
            html = pattern.sub(fig_html.strip(), html, count=1)
            figs_inserted += 1
        else:
            # Look for paragraph mentioning Hình X.Y
            p_pattern = re.compile(rf'(<p class="lesson-p">.*?H[ìi]nh\s+{bai_num}\.{hinh_num}.*?</p>)', re.DOTALL | re.IGNORECASE)
            if p_pattern.search(html):
                html = p_pattern.sub(r'\1\n' + fig_html.strip(), html, count=1)
                figs_inserted += 1
            else:
                # Append to discovery or content section
                if '</section>' in html:
                    parts = html.rsplit('</section>', 1)
                    html = parts[0] + "\n" + fig_html.strip() + "\n</section>" + parts[1]
                    figs_inserted += 1

    les["html"] = html
    # Save individual file
    file_path = ROOT / "lessons" / "lop-10" / f"{les['id']}.html"
    with open(file_path, "w", encoding="utf-8") as f_out:
        f_out.write(html)
        
    print(f"Bài {bai_num} ({les['id']}): embedded {figs_inserted} figures")
    updated_count += 1

with open(LESSONS_PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"\nEmbedded all figures across {updated_count} lessons of Lop 10!")
