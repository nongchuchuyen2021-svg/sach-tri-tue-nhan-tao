import ast
import html
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(r"E:\du-an\Sach AI")
LESSONS_DIR = ROOT / "lessons" / "lop-10"
DATA_DIR = ROOT / "data"
DICT_PATH = ROOT / "scripts" / "vi_50k.txt"

FORBIDDEN_PATTERNS = [
    (r"tri\s+tuệ", "tri tuệ -> trí tuệ"),
    (r"\bki\s+thuật\b", "ki thuật -> kĩ thuật"),
    (r"một\s+sô\b", "một sô -> một số"),
    (r"\bthiêu\b", "thiêu -> thiếu"),
    (r"kiềm\s+tra|kiếm\s+tra|kiềm\s+chứng|kiềm\s+soát", "kiềm/kiếm -> kiểm"),
    (r"chính\s+xac\b|chinh\s+xác\b|chinh\s+xac\b", "chinh xac -> chính xác"),
    (r"\bphố\s+biến\b|\bphố\s+thông\b", "phố biến/thông -> phổ biến/thông"),
    (r"hộ\s+thống|\bhệ\s+thông\b", "hộ thống / hệ thông -> hệ thống"),
    (r"dữ\s+liêu\b", "dữ liêu -> dữ liệu"),
    (r"minh\s+hoa\b|mình\s+hoa\b", "minh hoa -> minh hoạ"),
    (r"hình\s+ánh\b|hình\s+ành\b|hình\s+anh\b", "hình ánh/ành/anh -> hình ảnh"),
    (r"\bsố\s+tay\b", "số tay -> sổ tay"),
    (r"công\s+cụ\s+Ai\b|hệ\s+thống\s+Ai\b|của\s+Ai\b|nhờ\s+Ai\b|dùng\s+Ai\b|với\s+Ai\b", "Ai -> AI"),
    (r"VẠN\s+DỤNG|ĐỒNG\s+CHÚ\s+ĐIÊN|CHỦ\s+ĐẾ\s+\d|BÃI\s+\d|Bỏi\s+2|Àl\b|(?<!\w)Al(?!\w)", "OCR artifact / Al / CHỦ ĐẾ"),
    (r"hiểu\s+làm|hiếu\s+lầm|hiếu\s+hết|không\s+hiếu|cách\s+hiếu", "hiểu lầm/hiểu"),
    (r"công\s+băng|cản\s+bằng|cản\s+đối|đàm\s+bảo|đám\s+bảo", "tone error (công bằng/đảm bảo/cân bằng)"),
    (r"cơ\s+hội|co\s+hội", "__SKIP_FLAG__"),  # handled carefully below
    (r"\bco\s+hội\b", "co hội -> cơ hội"),
    (r"thân\s+mền|trợ\s+lí\s+ào|triền\s+tư\s+duy|hứng\s+thủ", "Loi noi dau typos"),
    (r"củng\s+có\b", "củng có -> củng cố"),
    (r"\btim\s+thấy\b|\btim\s+thêm\b|\btim\s+hiểu\b|\btim\s+bài\b", "tim -> tìm"),
    (r"học\s+lập\b|kể\s+hoạch\b|luyện\s+lập\b|biên\s+lập\b", "lập/kể hoạch -> tập/kế hoạch"),
    (r"ngôn\s+ngừ\b|ngôn\s+ngũ\b", "ngôn ngừ/ngũ -> ngôn ngữ"),
    (r"tin\s+già\b|nội\s+dung\s+già\b|già\s+mạo|Bia\s+dặt", "tin già/già mạo/Bia dặt"),
    (r"nâu\s+rõ|cua\s+prompt|thầy\s+có\s+giáo", "nâu rõ/cua prompt/thầy có giáo"),
    (r"kì\s+nguyên|ki\s+nguyên|ki\s+nguyễn", "kì/ki -> kỉ nguyên"),
    (r"giữ\s+gin\b|an\s+loàn\b|trò\s+chuyên\b", "giữ gin/an loàn/trò chuyên"),
    (r"điều\s+chinh\b|điều\s+chính\b", "điều chinh/chính -> điều chỉnh"),
    (r"mối\s+đe\s+doa|truyên\s+tranh|Giác\s+mơ|phiên\s+bằn", "bai-12 typos"),
    (r"CHỦ\s+ĐỀ\s+3\.\s+ĐẠO|CHỦ\s+ĐỀ\s+4\.\s+PHÁT", "__ALLOW_TOC__"),
]

# Filter out helper sentinel rules
ACTIVE_FORBIDDEN = [(p, d) for p, d in FORBIDDEN_PATTERNS if not d.startswith("__")]


class TagBalanceParser(HTMLParser):
    VOID = {"img", "br", "hr", "input", "meta", "link", "source"}

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"Unexpected </{tag}> at line {self.getpos()[0]}")
            return
        top, pos = self.stack[-1]
        if top == tag:
            self.stack.pop()
        else:
            found = -1
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    found = i
                    break
            if found == -1:
                self.errors.append(f"Stray </{tag}> at line {self.getpos()[0]} (top is <{top}> from line {pos[0]})")
            else:
                unclosed = self.stack[found + 1 :]
                self.errors.append(
                    f"Unclosed tags {[t[0] for t in unclosed]} before </{tag}> at line {self.getpos()[0]}"
                )
                self.stack = self.stack[:found]


def check_parity_and_json():
    lessons = json.loads((DATA_DIR / "lessons-lop-10.json").read_text(encoding="utf-8"))
    books = json.loads((DATA_DIR / "books.json").read_text(encoding="utf-8"))
    search_items = json.loads((DATA_DIR / "search-lop-10.json").read_text(encoding="utf-8"))

    assert len(lessons) == 19, f"Expected 19 lessons, got {len(lessons)}"
    diffs = []
    for les in lessons:
        p = LESSONS_DIR / f"{les['id']}.html"
        if not p.exists():
            diffs.append(f"Missing HTML: {p}")
            continue
        html_txt = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        if html_txt != les["html"]:
            diffs.append(f"Mismatch in {les['id']}")
    print(f"[CHECK 1] HTML <-> JSON parity across {len(lessons)} lessons: {len(diffs)} diffs")
    for d in diffs:
        print("  DIFF:", d)
    return lessons, books, search_items, diffs


def check_forbidden(lessons, books, search_items):
    books_list = books.get("books", books) if isinstance(books, dict) else books
    lop10_book = next((b for b in books_list if b.get("id") == "lop-10"), None)
    assert lop10_book is not None, "Missing lop-10 in books.json"
    hits = []

    def scan_blob(label, text):
        for pat, desc in ACTIVE_FORBIDDEN:
            flags = 0 if desc == "Ai -> AI" or "Al" in desc else re.IGNORECASE
            for m in re.finditer(pat, text, flags=flags):
                start = max(0, m.start() - 25)
                end = min(len(text), m.end() + 25)
                ctx = text[start:end].replace("\n", " ")
                hits.append(f"[{label}] {desc}: ...{ctx}...")

    for les in lessons:
        prose = re.sub(r'<div class="code-block-wrapper">.*?</div>\s*</div>|<pre><code.*?>.*?</code></pre>', ' ', les["html"], flags=re.S)
        prose = re.sub(r'<[^>]+>', ' ', prose)
        scan_blob(les["id"], prose)
        scan_blob(f"{les['id']}:summary", les.get("summary", ""))
        scan_blob(f"{les['id']}:title", les.get("title", ""))

    for grp in lop10_book.get("toc", []):
        for b_les in grp.get("items", []):
            scan_blob(f"books.json:{b_les['id']}", b_les.get("summary", "") + " " + b_les.get("title", ""))

    for s_les in search_items:
        scan_blob(f"search.json:{s_les['id']}", s_les.get("content", "") + " " + s_les.get("title", ""))

    print(f"[CHECK 2] Forbidden OCR patterns scan: {len(hits)} hits")
    for h in hits[:40]:
        print("  HIT:", h)
    return hits


def check_python_ast(lessons):
    code_failures = []
    total_blocks = 0
    for les in lessons:
        blocks = re.findall(r'<code class="language-python">(.*?)</code>', les["html"], flags=re.S)
        for idx, raw in enumerate(blocks, 1):
            total_blocks += 1
            code = html.unescape(raw).strip()
            lines = [ln for ln in code.splitlines() if not ln.strip().startswith(("pip ", "!pip ", "%pip "))]
            cleaned = "\n".join(lines).strip()
            if not cleaned:
                continue
            try:
                ast.parse(cleaned)
            except SyntaxError as e:
                code_failures.append(f"{les['id']} block #{idx}: {e}")
    print(f"[CHECK 3] Python AST check ({total_blocks} blocks): {len(code_failures)} errors")
    for f in code_failures:
        print("  AST ERR:", f)
    return code_failures


def check_html_balance(lessons):
    tag_errors = []
    for les in lessons:
        parser = TagBalanceParser()
        parser.feed(f"<root>{les['html']}</root>")
        parser.close()
        if parser.stack and [t[0] for t in parser.stack] != ["root"]:
            tag_errors.append(f"{les['id']}: unclosed stack {parser.stack}")
        for err in parser.errors:
            tag_errors.append(f"{les['id']}: {err}")
    print(f"[CHECK 4a] HTML tag balance across {len(lessons)} files: {len(tag_errors)} issues")
    for e in tag_errors[:25]:
        print("  HTML ERR:", e)
    return tag_errors


def scan_unknown_vietnamese_words(lessons):
    if not DICT_PATH.exists():
        print("[CHECK 4b] Dictionary not found, skipping word scan.")
        return []
    raw_words = DICT_PATH.read_text(encoding="utf-8").splitlines()
    vocab = set()
    for w in raw_words:
        w = w.strip().lower()
        if w:
            for part in w.split():
                vocab.add(part)

    EXTRA_VALID = {
        "ai", "genai", "llm", "llms", "agi", "nlp", "cnn", "deepfake", "hallucination", "bias",
        "prompt", "prompts", "token", "tokens", "chatgpt", "gemini", "claude", "copilot", "suno",
        "craiyon", "musicgen", "voicemod", "bing", "creator", "google", "colab", "colaboratory",
        "kaggle", "python", "gtts", "ipython", "numpy", "pandas", "matplotlib", "jupyter",
        "notebook", "notebooks", "markdown", "code", "cell", "run", "edit", "view", "file", "help",
        "share", "login", "sign", "account", "create", "draft", "saved", "session", "autoplay",
        "faceid", "touch", "wifi", "internet", "email", "slide", "poster", "video", "audio",
        "mp3", "blouse", "random", "semi", "realistic", "unesco", "bgdđt", "gdpt", "sgk", "stk",
        "nxb", "tnhh", "cp", "sedidco", "cxbiph", "isbn", "qđxb", "đkxb", "qđ", "vnđ", "40.000đ",
        "giai", "hoá", "hóa", "kĩ", "kỹ", "lí", "lý", "mĩ", "mỹ", "tỉ", "tỷ", "tuỳ", "tùy",
        "xoá", "xóa", "hoạ", "họa", "khoá", "khóa", "toán", "toàn", "no-ron", "nơ-ron", "ron", "nơ",
        "ở", "ạ", "à", "ư", "cô", "thầy", "lan", "nam", "minh", "an", "hoa", "hưng", "linh",
        "trang", "cường", "đức", "mai", "long", "quân", "bình", "tùng", "chính", "vinh", "lê",
        "vân", "tuấn", "luân", "giang", "sơn", "phi", "lân", "thái", "vĩnh", "khánh", "phú",
        "đéc", "đồng", "tháp", "hà", "nội", "huế", "10a2", "14h00", "since", "for",
    }
    vocab.update(EXTRA_VALID)

    STRICT_BAD = {
        "chinh", "xac", "duoc", "khong", "nhung", "thuong", "luong", "nguoi", "hinh",
        "lieu", "kiem", "hieu", "phuong", "trinh", "chuong", "nhieu", "thuc", "hanh",
        "phat", "trien", "ngon", "ngu", "truong", "pham", "nghe", "thong",
        "chuc", "thuat", "tich", "giai", "thich", "duoi", "truoc", "chuyen",
        "nghiep", "luyen", "chuan", "thiet", "buoc", "muon", "cuon", "quyen",
        "phien", "tuyen", "duong", "thieu", "chieu", "nghiem", "khach", "hang", "tieng",
        "tieu", "muc", "khoi", "dong", "kham", "pha", "van", "dung",
    }
    # exclude words that validly appear in English/short-words? None in above except maybe "van" (rare) or "hang" (rare); let's keep & inspect
    VI_DIACRITIC_RE = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", re.I)
    WORD_RE = re.compile(r"[A-Za-zÀ-ỹ]+")

    unknown = {}
    tone_missing = []
    for les in lessons:
        txt = re.sub(r'<div class="code-block-wrapper">.*?</div>\s*</div>|<pre><code.*?>.*?</code></pre>', ' ', les["html"], flags=re.S)
        txt = re.sub(r'<[^>]+>', ' ', txt)
        txt = html.unescape(txt)
        for m in WORD_RE.finditer(txt):
            w = m.group(0)
            wl = w.lower()
            if VI_DIACRITIC_RE.search(wl) and wl not in vocab:
                entry = unknown.setdefault(wl, {"count": 0, "lessons": set(), "raw": w})
                entry["count"] += 1
                entry["lessons"].add(les["id"])
        for m in re.finditer(r'(?<![A-Za-zÀ-ỹ_])[A-Za-z]+(?![A-Za-zÀ-ỹ_])', txt):
            w = m.group(0).lower()
            if w in STRICT_BAD:
                ctx = txt[max(0, m.start()-20):min(len(txt), m.end()+20)].replace("\n", " ")
                tone_missing.append(f"{les['id']}: {m.group(0)!r} in ...{ctx}...")

    sorted_unk = sorted(unknown.items(), key=lambda kv: (-kv[1]["count"], kv[0]))
    print(f"[CHECK 4b] Diacritic words not in vi_50k + domain list: {len(sorted_unk)} distinct tokens")
    for w, info in sorted_unk[:80]:
        ls = ", ".join(sorted(info["lessons"])[:3])
        print(f"  {info['raw']} ({info['count']}x) in [{ls}]")
    print(f"[CHECK 4c] Strict missing-tone ASCII suspects: {len(tone_missing)}")
    for tm in tone_missing[:30]:
        print("  SUSPECT:", tm)
    return sorted_unk


def main():
    lessons, books, search_items, diffs = check_parity_and_json()
    hits = check_forbidden(lessons, books, search_items)
    ast_errs = check_python_ast(lessons)
    html_errs = check_html_balance(lessons)
    unk = scan_unknown_vietnamese_words(lessons)
    if diffs or hits or ast_errs or html_errs:
        print("\n[SUMMARY] VERIFICATION FAILED — see errors above.")
        raise SystemExit(1)
    print("\n[SUMMARY] ALL 4 HARD CHECKS PASSED! Review unknown diacritic tokens above for any subtle typos.")


if __name__ == "__main__":
    main()
