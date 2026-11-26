import io
import json
import os
import re
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
DATA_DIR = ROOT / "data"

MAIN_WIDTH = 1100
THUMB_WIDTH = 240
COVER_WIDTH = 600
MAIN_QUALITY = 80
THUMB_QUALITY = 72
COVER_QUALITY = 84

BOOKS_META = [
    {
        "id": "lop-10",
        "pdf": "lop-10-tri-tue-nhan-tao.pdf",
        "grade": 10,
        "title": "Trí tuệ nhân tạo 10",
        "subtitle": "Tài liệu giáo dục phổ thông · Lớp 10",
        "authors": "Hà Đặng Cao Tùng – Hoàng Thị Mai – Lê Anh Vinh (Đồng Chủ biên)",
        "coauthors": "Vũ Trung Chính, Nguyễn Quang Đức, Nguyễn Chí Thanh, Nguyễn Thị Vân Anh, Phạm Tuấn Anh, Vũ Văn Luận",
        "publisher": "Nhà xuất bản Giáo dục Việt Nam",
        "isbn": "978-604-0-46630-3",
        "accent": "#2563eb",
        "accentSoft": "rgba(37, 99, 235, 0.12)",
        "pageOffset": 2,
        "firstSpreadStart": 2,
        "toc": [
            {
                "group": "Mở đầu",
                "items": [
                    {"title": "Bìa sách", "page": 1, "printPage": None},
                    {"title": "Công văn thẩm định & Bìa lót", "page": 2, "printPage": None},
                    {"title": "Hướng dẫn sử dụng sách", "page": 4, "printPage": 2},
                    {"title": "Lời nói đầu", "page": 5, "printPage": 3},
                    {"title": "Mục lục", "page": 6, "printPage": 4},
                ],
            },
            {
                "group": "Chủ đề 1. Giới thiệu về AI và AI tạo sinh",
                "page": 7,
                "printPage": 5,
                "items": [
                    {"title": "Bài 1. Trí tuệ nhân tạo", "page": 8, "printPage": 6},
                    {"title": "Bài 2. AI tạo sinh", "page": 13, "printPage": 11},
                    {"title": "Bài 3. Mô hình ngôn ngữ lớn", "page": 21, "printPage": 19},
                    {"title": "Bài 4. Dữ liệu huấn luyện", "page": 28, "printPage": 26},
                ],
            },
            {
                "group": "Chủ đề 2. Khám phá công cụ và ứng dụng AI",
                "page": 33,
                "printPage": 31,
                "items": [
                    {"title": "Bài 5. Prompt – Giao tiếp với AI tạo sinh", "page": 34, "printPage": 32},
                    {"title": "Bài 6. AI tạo sinh hỗ trợ học tập", "page": 41, "printPage": 39},
                ],
            },
            {
                "group": "Chủ đề 3. Đạo đức và trách nhiệm khi sử dụng AI",
                "page": 48,
                "printPage": 46,
                "items": [
                    {"title": "Bài 7. Phân biệt thật – giả trong AI tạo sinh", "page": 49, "printPage": 47},
                    {"title": "Bài 8. Hiểu đúng về AI tạo sinh: thiên vị, hiểu lầm và tác hại với con người", "page": 53, "printPage": 51},
                    {"title": "Bài 9. Công dân số trong kỉ nguyên AI", "page": 58, "printPage": 56},
                ],
            },
            {
                "group": "Chủ đề 4. Phát triển sản phẩm và ứng dụng AI",
                "page": 67,
                "printPage": 65,
                "items": [
                    {"title": "Bài 10. AI và nghề nghiệp", "page": 68, "printPage": 66},
                    {"title": "Bài 11. Môi trường phát triển sản phẩm AI", "page": 72, "printPage": 70},
                    {"title": "Bài 12. Bài tập dự án", "page": 79, "printPage": 77},
                ],
            },
            {
                "group": "Phụ lục",
                "items": [
                    {"title": "Bảng giải thích thuật ngữ", "page": 89, "printPage": 87},
                    {"title": "Thông tin xuất bản & Bìa sau", "page": 90, "printPage": 88},
                ],
            },
        ],
    },
    {
        "id": "lop-11",
        "pdf": "lop-11-tri-tue-nhan-tao.pdf",
        "grade": 11,
        "title": "Trí tuệ nhân tạo 11",
        "subtitle": "Tài liệu giáo dục phổ thông · Lớp 11",
        "authors": "Hà Đặng Cao Tùng – Hoàng Thị Mai – Lê Anh Vinh (Đồng Chủ biên)",
        "coauthors": "Vũ Trung Chính, Nguyễn Quang Đức, Nguyễn Chí Thanh, Nguyễn Thị Vân Anh, Đỗ Đức Lân, Nguyễn Minh Hải",
        "publisher": "Nhà xuất bản Giáo dục Việt Nam",
        "isbn": "978-604-0-46632-7",
        "accent": "#0891b2",
        "accentSoft": "rgba(8, 145, 178, 0.12)",
        "pageOffset": 2,
        "firstSpreadStart": 2,
        "toc": [
            {
                "group": "Mở đầu",
                "items": [
                    {"title": "Bìa sách", "page": 1, "printPage": None},
                    {"title": "Công văn thẩm định & Bìa lót", "page": 2, "printPage": None},
                    {"title": "Hướng dẫn sử dụng sách", "page": 4, "printPage": 2},
                    {"title": "Lời nói đầu", "page": 5, "printPage": 3},
                    {"title": "Mục lục", "page": 6, "printPage": 4},
                ],
            },
            {
                "group": "Chủ đề 1. Mô hình ngôn ngữ lớn sáng tạo nội dung",
                "page": 7,
                "printPage": 5,
                "items": [
                    {"title": "Bài 1. Kĩ thuật viết prompt cơ bản và nâng cao", "page": 8, "printPage": 6},
                    {"title": "Bài 2. Mô hình ngôn ngữ lớn sáng tạo nội dung", "page": 18, "printPage": 16},
                ],
            },
            {
                "group": "Chủ đề 2. Nguyên lí hoạt động của mô hình ngôn ngữ lớn",
                "page": 26,
                "printPage": 24,
                "items": [
                    {"title": "Bài 3. Mô hình ngôn ngữ lớn và hạn chế của nó", "page": 27, "printPage": 25},
                    {"title": "Bài 4. Giới thiệu về RAG", "page": 33, "printPage": 31},
                    {"title": "Bài 5. Mạng nơ-ron nhân tạo", "page": 41, "printPage": 39},
                    {"title": "Bài 6. Phân loại và phân cụm dữ liệu", "page": 50, "printPage": 48},
                ],
            },
            {
                "group": "Chủ đề 3. Đạo đức và trách nhiệm khi sử dụng AI",
                "page": 60,
                "printPage": 58,
                "items": [
                    {"title": "Bài 7. Đạo đức, pháp luật và văn hoá trong sử dụng mô hình ngôn ngữ lớn", "page": 61, "printPage": 59},
                    {"title": "Bài 8. Giá trị con người trong kỉ nguyên AI", "page": 66, "printPage": 64},
                ],
            },
            {
                "group": "Chủ đề 4. Mô hình ngôn ngữ lớn trong học tập",
                "page": 71,
                "printPage": 69,
                "items": [
                    {"title": "Bài 9. Mô hình ngôn ngữ lớn hỗ trợ học tập", "page": 72, "printPage": 70},
                    {"title": "Bài 10. Mô hình ngôn ngữ lớn hỗ trợ học lập trình", "page": 77, "printPage": 75},
                    {"title": "Bài 11. Tạo và sửa hình ảnh bằng mô hình ngôn ngữ lớn", "page": 82, "printPage": 80},
                    {"title": "Bài 12. Tạo video bằng mô hình ngôn ngữ lớn", "page": 90, "printPage": 88},
                    {"title": "Bài 13. Bài tập dự án", "page": 95, "printPage": 93},
                ],
            },
            {
                "group": "Phụ lục",
                "items": [
                    {"title": "Bảng giải thích thuật ngữ", "page": 101, "printPage": 99},
                    {"title": "Thông tin xuất bản & Bìa sau", "page": 102, "printPage": 100},
                ],
            },
        ],
    },
    {
        "id": "lop-12",
        "pdf": "lop-12-tri-tue-nhan-tao.pdf",
        "grade": 12,
        "title": "Trí tuệ nhân tạo 12",
        "subtitle": "Tài liệu giáo dục phổ thông · Lớp 12",
        "authors": "Hà Đặng Cao Tùng – Hoàng Thị Mai – Lê Anh Vinh (Đồng Chủ biên)",
        "coauthors": "Vũ Trung Chính, Nguyễn Quang Đức, Nguyễn Chí Thanh, Nguyễn Thị Vân Anh, Đỗ Đức Lân, Lê Quang Quân",
        "publisher": "Nhà xuất bản Giáo dục Việt Nam",
        "isbn": "978-604-0-46634-1",
        "accent": "#7c3aed",
        "accentSoft": "rgba(124, 58, 237, 0.12)",
        "pageOffset": 1,
        "firstSpreadStart": 3,
        "toc": [
            {
                "group": "Mở đầu",
                "items": [
                    {"title": "Bìa sách", "page": 1, "printPage": None},
                    {"title": "Bìa lót", "page": 2, "printPage": None},
                    {"title": "Hướng dẫn sử dụng sách", "page": 3, "printPage": 2},
                    {"title": "Lời nói đầu", "page": 4, "printPage": 3},
                    {"title": "Mục lục", "page": 5, "printPage": 4},
                ],
            },
            {
                "group": "Chủ đề 1. AI Agents – Hướng tới AI tự hoạt động",
                "page": 6,
                "printPage": 5,
                "items": [
                    {"title": "Bài 1. Giới thiệu về AI Agents", "page": 7, "printPage": 6},
                    {"title": "Bài 2. Cấu trúc AI Agent đơn giản", "page": 14, "printPage": 13},
                ],
            },
            {
                "group": "Chủ đề 2. RAG và công cụ làm việc với LLM",
                "page": 25,
                "printPage": 24,
                "items": [
                    {"title": "Bài 3. RAG nâng cao", "page": 26, "printPage": 25},
                    {"title": "Bài 4. Thư viện nguồn mở LLM", "page": 33, "printPage": 32},
                    {"title": "Bài 5. Khai thác thư viện nguồn mở LLM", "page": 39, "printPage": 38},
                ],
            },
            {
                "group": "Chủ đề 3. Đạo đức, trách nhiệm và tác động xã hội trong AI tạo sinh",
                "page": 47,
                "printPage": 46,
                "items": [
                    {"title": "Bài 6. Tác động của AI đến đời sống con người", "page": 48, "printPage": 47},
                    {"title": "Bài 7. AI mở ra cơ hội và thách thức cho các ngành nghề", "page": 54, "printPage": 53},
                    {"title": "Bài 8. Quyền con người trong kỉ nguyên AI", "page": 60, "printPage": 59},
                    {"title": "Bài 9. Phát triển AI có trách nhiệm", "page": 66, "printPage": 65},
                ],
            },
            {
                "group": "Chủ đề 4. Nguyên lí Học máy",
                "page": 73,
                "printPage": 72,
                "items": [
                    {"title": "Bài 10. Nguyên lí cơ bản của Học máy", "page": 74, "printPage": 73},
                    {"title": "Bài 11. Tối ưu hoá mô hình", "page": 81, "printPage": 80},
                ],
            },
            {
                "group": "Chủ đề 5. Dự án AI Agent",
                "page": 89,
                "printPage": 88,
                "items": [
                    {"title": "Bài 12. Hình thành ý tưởng và lập kế hoạch", "page": 90, "printPage": 89},
                    {"title": "Bài 13. Xây dựng sản phẩm", "page": 96, "printPage": 95},
                    {"title": "Bài 14. Hoàn chỉnh sản phẩm", "page": 105, "printPage": 104},
                    {"title": "Bài 15. Trình bày kết quả dự án", "page": 113, "printPage": 112},
                ],
            },
            {
                "group": "Phụ lục",
                "items": [
                    {"title": "Bảng giải thích thuật ngữ", "page": 119, "printPage": 118},
                    {"title": "Thông tin xuất bản & Bìa sau", "page": 121, "printPage": 120},
                ],
            },
        ],
    },
]


def detect_camscanner_edges(page):
    """Detect which outer edge(s) carry the CamScanner watermark from PDF OCR words."""
    r = page.rect
    edges = {}
    for w in page.get_text("words"):
        txt = w[4].lower()
        if "camscanner" in txt or "scanner" in txt or w[4] == "CS":
            rx = (w[0] + w[2]) / 2.0 / r.width
            ry = (w[1] + w[3]) / 2.0 / r.height
            dists = {
                "bottom": (1.0 - ry, 1.0 - w[1] / r.height),
                "top": (ry, w[3] / r.height),
                "right": (1.0 - rx, 1.0 - w[0] / r.width),
                "left": (rx, w[2] / r.width),
            }
            best_edge, (center_d, inner_d) = min(dists.items(), key=lambda kv: kv[1][0])
            if center_d < 0.12:
                edges[best_edge] = max(edges.get(best_edge, 0.0), inner_d)
    return edges


def find_cs_cut(profile, max_cut, ocr_inner_frac=None):
    """
    Find exact cut depth for an edge that may contain a CamScanner bar.
    A CamScanner bar always consists of an outer white margin, the CS/CamScanner
    logo (with pixels < 0.96), and an inner pure-white (>= 0.985) separator band
    before the scanned book page begins.
    """
    dim = len(profile)
    lim = min(max_cut, dim)
    if lim <= 0:
        return 0

    # Look for a >= 0.985 pure-white separator band of >= 6px inside outer 8.5%
    # sitting just inward of any logo dip (< 0.95) in outer 6.2%.
    outer_logo_lim = min(int(dim * 0.062), lim)
    dips = np.where(profile[:outer_logo_lim] < 0.955)[0]

    has_cs_bar = False
    start_from = 0
    if ocr_inner_frac is not None:
        ocr_px = int(dim * ocr_inner_frac) + int(dim * 0.008)
        # Verify there is a white separator band (>= 0.98) near/inward of ocr_px
        search_from = max(0, min(ocr_px - int(dim * 0.015), lim - 6))
        for j in range(search_from, min(lim - 5, int(dim * 0.082))):
            if np.min(profile[j : j + 6]) >= 0.98:
                has_cs_bar = True
                start_from = j
                break
        if not has_cs_bar and len(dips) > 0:
            # Even if page margin itself is dark/white, cut past logo dip
            last_dip = int(dips[-1])
            if last_dip < lim - 4 and np.min(profile[last_dip + 1 : min(lim, last_dip + 7)]) >= 0.97:
                has_cs_bar = True
                start_from = last_dip + 1
    elif len(dips) >= 4:
        # Pixel-only fallback when OCR missed the CamScanner text
        # Find the >= 0.985 white separator sitting inward of the logo dips
        last_dip = int(dips[-1])
        for j in range(last_dip + 1, min(lim - 5, int(dim * 0.082))):
            if np.min(profile[j : j + 6]) >= 0.985:
                has_cs_bar = True
                start_from = j
                break

    if has_cs_bar:
        cut = start_from
        while cut < lim and profile[cut] >= 0.98:
            cut += 1
        return min(cut, max_cut)

    # Non-CamScanner edge: only trim solid outer white scanner border (max 1.5%)
    max_border = min(int(dim * 0.015), max_cut)
    cut = 0
    for i in range(max_border):
        if profile[i] >= 0.995:
            cut = i + 1
        else:
            break
    return cut


def crop_camscanner_and_margins(im, cs_edges):
    """Remove CamScanner strip and tiny solid outer scanner borders safely."""
    arr = np.asarray(im)
    h, w, _ = arr.shape
    white = (arr >= 249).all(axis=2)
    row_white = white.mean(axis=1)
    col_white = white.mean(axis=0)

    max_h = int(h * 0.088)
    max_w = int(w * 0.088)

    top = find_cs_cut(row_white, max_h, cs_edges.get("top"))
    bottom = find_cs_cut(row_white[::-1], max_h, cs_edges.get("bottom"))
    left = find_cs_cut(col_white, max_w, cs_edges.get("left"))
    right = find_cs_cut(col_white[::-1], max_w, cs_edges.get("right"))

    return im.crop((left, top, w - right, h - bottom))


def find_spine_split_x(im):
    """Find book gutter column near the horizontal center of a 2-page spread."""
    gray = np.asarray(im.convert("L"), dtype=np.float32)
    h, w = gray.shape
    lo = int(w * 0.475)
    hi = int(w * 0.525)
    col_means = gray[int(h * 0.08) : int(h * 0.92), lo:hi].mean(axis=0)
    # 11px moving average
    kernel = np.ones(11, dtype=np.float32) / 11.0
    smooth = np.convolve(col_means, kernel, mode="same")
    # Ignore edge effects of convolution
    valid = smooth[5:-5]
    if valid.max() - valid.min() < 4.0:
        return w // 2
    return lo + 5 + int(np.argmin(valid))


def clean_words_text(words, filter_fn=None):
    parts = []
    for w in words:
        txt = w[4].strip()
        if not txt:
            continue
        low = txt.lower()
        if "camscanner" in low or "cscamscanner" in low or txt == "CS":
            continue
        if filter_fn is not None and not filter_fn(w):
            continue
        parts.append(txt)
    text = " ".join(parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def save_webp_variants(im, out_dir, page_num):
    """Save main WebP, thumbnail WebP, and cover WebP (if page 1)."""
    w, h = im.size
    if w > MAIN_WIDTH:
        nh = round(h * MAIN_WIDTH / w)
        main_im = im.resize((MAIN_WIDTH, nh), Image.Resampling.LANCZOS)
    else:
        main_im = im
    main_path = out_dir / f"page-{page_num:03d}.webp"
    main_im.save(main_path, "WEBP", quality=MAIN_QUALITY, method=4)

    tw = THUMB_WIDTH
    th = round(h * tw / w)
    thumb_im = im.resize((tw, th), Image.Resampling.LANCZOS)
    thumb_path = out_dir / "thumbs" / f"page-{page_num:03d}.webp"
    thumb_im.save(thumb_path, "WEBP", quality=THUMB_QUALITY, method=4)

    if page_num == 1:
        cw = min(COVER_WIDTH, w)
        ch = round(h * cw / w)
        cover_im = im.resize((cw, ch), Image.Resampling.LANCZOS)
        cover_im.save(out_dir / "cover.webp", "WEBP", quality=COVER_QUALITY, method=4)


def page_label(book_meta, page_num, total_pages):
    if page_num == 1:
        return "Bìa trước"
    if page_num == total_pages:
        return "Bìa sau"
    if book_meta["pageOffset"] == 2 and page_num in (2, 3):
        return "Công văn thẩm định" if page_num == 2 else "Bìa lót"
    if book_meta["pageOffset"] == 1 and page_num == 2:
        return "Bìa lót"
    p_in = page_num - book_meta["pageOffset"]
    return f"Trang {p_in}"


def process_book(meta):
    pdf_path = ROOT / meta["pdf"]
    out_dir = BOOKS_DIR / meta["id"]
    (out_dir / "thumbs").mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    page_entries = []  # list of (pil_image, ocr_text)

    for idx, page in enumerate(doc):
        xref = page.get_images(full=True)[0][0]
        base = doc.extract_image(xref)
        im = Image.open(io.BytesIO(base["image"]))
        im = ImageOps.exif_transpose(im).convert("RGB")

        cs_edges = detect_camscanner_edges(page)
        cropped = crop_camscanner_and_margins(im, cs_edges)

        # Page-specific rotations identified during inspection
        if meta["id"] == "lop-10" and idx == 1:
            cropped = cropped.transpose(Image.Transpose.ROTATE_90)
        elif meta["id"] == "lop-12" and idx == 84:
            cropped = cropped.transpose(Image.Transpose.ROTATE_180)

        rect = page.rect
        words = page.get_text("words")

        # Filter out words sitting right inside CamScanner corner/strip
        def non_cs_word(w):
            rx = (w[0] + w[2]) / 2.0 / rect.width
            ry = (w[1] + w[3]) / 2.0 / rect.height
            if "bottom" in cs_edges and ry > 0.92:
                return False
            if "top" in cs_edges and ry < 0.08:
                return False
            if "right" in cs_edges and rx > 0.92:
                return False
            if "left" in cs_edges and rx < 0.08:
                return False
            return True

        cw, ch = cropped.size
        if cw > ch:
            split_x = find_spine_split_x(cropped)
            left_im = cropped.crop((0, 0, split_x, ch))
            right_im = cropped.crop((split_x, 0, cw, ch))

            if meta["id"] == "lop-10" and idx == 1:
                # Before ROTATE_90, top half became left page, bottom half became right page
                left_txt = clean_words_text(
                    words, lambda w: non_cs_word(w) and ((w[1] + w[3]) / 2.0 < rect.height / 2.0)
                )
                right_txt = clean_words_text(
                    words, lambda w: non_cs_word(w) and ((w[1] + w[3]) / 2.0 >= rect.height / 2.0)
                )
            else:
                left_txt = clean_words_text(
                    words, lambda w: non_cs_word(w) and ((w[0] + w[2]) / 2.0 < rect.width / 2.0)
                )
                right_txt = clean_words_text(
                    words, lambda w: non_cs_word(w) and ((w[0] + w[2]) / 2.0 >= rect.width / 2.0)
                )

            page_entries.append((left_im, left_txt))
            page_entries.append((right_im, right_txt))
        else:
            txt = clean_words_text(words, non_cs_word)
            page_entries.append((cropped, txt))

    total_pages = len(page_entries)
    search_docs = []
    for i, (pg_im, pg_txt) in enumerate(page_entries, start=1):
        save_webp_variants(pg_im, out_dir, i)
        search_docs.append(
            {
                "p": i,
                "label": page_label(meta, i, total_pages),
                "t": pg_txt,
            }
        )

    search_path = DATA_DIR / f"search-{meta['id']}.json"
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search_docs, f, ensure_ascii=False, separators=(",", ":"))

    # Compute directory size
    total_bytes = sum(p.stat().st_size for p in out_dir.rglob("*.webp"))
    print(f"[{meta['id']}] pages={total_pages}, webp_size={total_bytes / (1024*1024):.2f} MB")

    return {
        "id": meta["id"],
        "grade": meta["grade"],
        "title": meta["title"],
        "subtitle": meta["subtitle"],
        "authors": meta["authors"],
        "coauthors": meta["coauthors"],
        "publisher": meta["publisher"],
        "isbn": meta["isbn"],
        "accent": meta["accent"],
        "accentSoft": meta["accentSoft"],
        "pages": total_pages,
        "pageOffset": meta["pageOffset"],
        "firstSpreadStart": meta["firstSpreadStart"],
        "cover": f"books/{meta['id']}/cover.webp",
        "thumb": f"books/{meta['id']}/thumbs/page-001.webp",
        "toc": meta["toc"],
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    catalog = []
    for meta in BOOKS_META:
        catalog.append(process_book(meta))

    with open(DATA_DIR / "books.json", "w", encoding="utf-8") as f:
        json.dump({"books": catalog}, f, ensure_ascii=False, indent=2)

    all_bytes = sum(p.stat().st_size for p in BOOKS_DIR.rglob("*.webp"))
    print(f"TOTAL books/ size: {all_bytes / (1024*1024):.2f} MB")


if __name__ == "__main__":
    main()
