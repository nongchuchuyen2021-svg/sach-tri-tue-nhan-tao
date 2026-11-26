import os
import re
import json
import pymupdf
from test_page_generator import get_page_blocks
from ocr_cleaner import clean_ocr_text

def is_major_heading(text):
    t = text.strip()
    upper = t.upper()
    if upper in ["MỤC TIÊU", "MUC TIÊU"]:
        return "MỤC TIÊU"
    if upper in ["KHỞI ĐỘNG", "KHOI ĐỘNG"]:
        return "KHỞI ĐỘNG"
    if upper in ["KHÁM PHÁ", "KHAM PHA"]:
        return "KHÁM PHÁ"
    if upper in ["LUYỆN TẬP", "LUYÊN TÂP", "LUYEN TAP"]:
        return "LUYỆN TẬP"
    if upper in ["VẬN DỤNG", "VÂN DUNG", "VAN DUNG"]:
        return "VẬN DỤNG"
    if upper in ["THỰC HÀNH", "THUC HANH"]:
        return "THỰC HÀNH"
    if upper in ["BÀI TẬP DỰ ÁN", "DỰ ÁN"]:
        return "DỰ ÁN"
    return None

def is_numbered_heading(text):
    t = text.strip()
    # E.g. "1. Trí tuệ nhân tạo", "2. Phân loại AI", "1. AI Agents"
    m = re.match(r"^(\d+)\.\s+([A-ZÀ-Ỹ].*)$", t)
    if m:
        return m.group(1), m.group(2)
    return None

def is_letter_subheading(text):
    t = text.strip()
    # E.g. "a) Trí thông minh", "b) Trí tuệ nhân tạo"
    m = re.match(r"^([a-z])\)\s+([A-ZÀ-Ỹ].*)$", t)
    if m:
        return m.group(1), m.group(2)
    return None

def is_bullet_item(text):
    t = text.strip()
    return t.startswith("•") or t.startswith("-") or t.startswith("–") or t.startswith("­")

def is_question_number(text):
    t = text.strip()
    m = re.match(r"^(\d+)\.\s+(.*)$", t)
    if m:
        return m.group(1), m.group(2)
    return None

def is_mcq_choice(text):
    t = text.strip()
    m = re.match(r"^([A-D])\.\s+(.*)$", t)
    if m:
        return m.group(1), m.group(2)
    return None

def clean_paragraph_text(text):
    text = clean_ocr_text(text)
    # Join broken lines inside paragraphs
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    cleaned_lines = []
    for line in lines:
        if cleaned_lines and not cleaned_lines[-1].endswith((".", ":", "!", "?", "•", "-", "–")):
            # If previous line doesn't end with sentence terminator, join with space
            cleaned_lines[-1] = cleaned_lines[-1] + " " + line
        else:
            cleaned_lines.append(line)
    return "\n\n".join(cleaned_lines)

def build_lesson_html(lesson_title, topic_title, blocks, book_id, start_page, end_page):
    """
    Assemble the list of blocks into semantic HTML.
    """
    html_parts = []
    
    # Lesson Header
    html_parts.append(f"""
    <header class="lesson-header">
        <div class="lesson-topic-badge">{topic_title}</div>
        <h1 class="lesson-main-title">{lesson_title}</h1>
        <div class="lesson-meta-bar">
            <span class="meta-pages">📄 Trang sách gốc: {start_page} – {end_page}</span>
            <button class="btn-toggle-scan" onclick="openOriginalPages({start_page}, {end_page})">📖 Xem bản in gốc</button>
        </div>
    </header>
    """)

    current_section = "intro"
    in_list = False
    
    i = 0
    while i < len(blocks):
        b = blocks[i]
        txt = b["text"].strip()
        
        # Skip repetitive lesson title in first block
        if i == 0 and ("BÀI " in txt.upper() or "CHỦ ĐỀ" in txt.upper()):
            i += 1
            continue
            
        major_h = is_major_heading(txt)
        if major_h:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
                
            current_section = major_h
            sec_class = {
                "MỤC TIÊU": "target-section",
                "KHỞI ĐỘNG": "warmup-section",
                "KHÁM PHÁ": "discovery-section",
                "THỰC HÀNH": "practice-section",
                "LUYỆN TẬP": "exercise-section",
                "VẬN DỤNG": "apply-section",
                "DỰ ÁN": "project-section",
            }.get(major_h, "content-section")
            
            icon = {
                "MỤC TIÊU": "🎯",
                "KHỞI ĐỘNG": "💡",
                "KHÁM PHÁ": "🔍",
                "THỰC HÀNH": "🛠️",
                "LUYỆN TẬP": "✏️",
                "VẬN DỤNG": "🚀",
                "DỰ ÁN": "📋",
            }.get(major_h, "📌")
            
            html_parts.append(f"""
            <section class="lesson-card {sec_class}" id="sec-{major_h.lower().replace(' ', '-')}">
                <div class="section-badge-header">
                    <span class="sec-icon">{icon}</span>
                    <h2 class="section-title">{major_h}</h2>
                </div>
                <div class="section-body">
            """)
            i += 1
            
            # Consume blocks until next major heading
            while i < len(blocks):
                nxt = blocks[i]["text"].strip()
                if is_major_heading(nxt):
                    break
                
                # Check for numbered heading e.g. 1. Trí tuệ nhân tạo
                num_h = is_numbered_heading(nxt)
                if num_h:
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                    html_parts.append(f'<h3 class="subheading-h3"><span class="h3-num">{num_h[0]}.</span> {num_h[1]}</h3>')
                    i += 1
                    continue
                    
                # Check for letter subheading e.g. a) Trí thông minh
                sub_h = is_letter_subheading(nxt)
                if sub_h:
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                    html_parts.append(f'<h4 class="subheading-h4"><span class="h4-letter">{sub_h[0]})</span> {sub_h[1]}</h4>')
                    i += 1
                    continue
                    
                # Check for bullet points
                if is_bullet_item(nxt):
                    if not in_list:
                        html_parts.append('<ul class="lesson-bullet-list">')
                        in_list = True
                    clean_item = re.sub(r"^[•\-–­]\s*", "", nxt)
                    html_parts.append(f'<li>{clean_paragraph_text(clean_item)}</li>')
                    i += 1
                    continue
                else:
                    if in_list:
                        html_parts.append("</ul>")
                        in_list = False
                        
                # Check for Knowledge Box (Hộp kiến thức / Khái niệm cốt lõi)
                # Usually definition blocks, or marked by keywords
                if ("là khả năng" in nxt or "là một hệ thống" in nxt or "được định nghĩa" in nxt or "là quá trình" in nxt) and len(nxt) < 400 and (current_section == "KHÁM PHÁ"):
                    html_parts.append(f"""
                    <div class="callout-box knowledge-callout">
                        <div class="callout-title">📘 Hộp kiến thức cốt lõi</div>
                        <p>{clean_paragraph_text(nxt)}</p>
                    </div>
                    """)
                    i += 1
                    continue
                    
                # Check for Code blocks or URLs
                if "import " in nxt or "def " in nxt or "print(" in nxt or "```" in nxt or "pip install" in nxt:
                    clean_code = nxt.replace("```python", "").replace("```", "").strip()
                    html_parts.append(f"""
                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">{clean_code}</code></pre>
                    </div>
                    """)
                    i += 1
                    continue

                # Check for Figures
                if nxt.startswith("Hình ") or "Hình " in nxt[:15]:
                    html_parts.append(f"""
                    <figure class="lesson-figure-box">
                        <div class="figure-placeholder">
                            <span class="fig-badge">🖼️ Minh họa trong sách</span>
                            <figcaption class="figure-caption">{clean_ocr_text(nxt)}</figcaption>
                        </div>
                    </figure>
                    """)
                    i += 1
                    continue

                # Regular paragraph
                cleaned_p = clean_paragraph_text(nxt)
                if cleaned_p:
                    html_parts.append(f'<p class="lesson-p">{cleaned_p}</p>')
                i += 1
                
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("</div></section>")
            continue
            
        # Regular text outside any major heading
        cleaned_p = clean_paragraph_text(txt)
        if cleaned_p:
            html_parts.append(f'<p class="lesson-p">{cleaned_p}</p>')
        i += 1
        
    if in_list:
        html_parts.append("</ul>")
        
    return "\n".join(html_parts)

print("build_lesson_html defined")
