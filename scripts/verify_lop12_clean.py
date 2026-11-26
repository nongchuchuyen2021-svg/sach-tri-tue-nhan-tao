import ast
import html
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(r"E:\du-an\Sach AI")
LESSONS_DIR = ROOT / "lessons" / "lop-12"
DATA_DIR = ROOT / "data"
DICT_PATH = ROOT / "scripts" / "vi_50k.txt"

FORBIDDEN_PATTERNS = [
    (r"tri\s+tuệ", "tri tuệ -> trí tuệ"),
    (r"ki\s+thuật\b", "ki thuật -> kĩ thuật"),
    (r"một\s+sô\b", "một sô -> một số"),
    (r"\bthiêu\b", "thiêu -> thiếu"),
    (r"kiềm\s+tra", "kiềm tra -> kiểm tra"),
    (r"chính\s+xac\b|chinh\s+xác\b|chinh\s+xac\b", "chinh xac -> chính xác"),
    (r"lựa\s+đề\b|hiệu\s*\n\s*lựa", "lựa đề/hiệu lựa"),
    (r"kháchh", "kháchh"),
    (r"phương\s+trinh\b", "phương trinh -> phương trình"),
    (r"sản\s+phầm|sạn\s+phầm", "sản phầm -> sản phẩm"),
    (r"\bhệ\s+thông\b", "hệ thông -> hệ thống"),
    (r"dữ\s+liêu\b", "dữ liêu -> dữ liệu"),
    (r"thuật\s+toan\b", "thuật toan -> thuật toán"),
    (r"tìm\s+kiêm\b|tim\s+kiếm\b|tim\s+kiêm\b", "tìm kiêm -> tìm kiếm"),
    (r"cụ\s+thế\?", "cụ thế? -> cụ thể?"),
    (r"thân\s+mền\b", "thân mền -> thân mến"),
    (r"VẠN\s+DỤNG", "VẠN DỤNG -> VẬN DỤNG"),
    (r"ĐÓNG\s+CHÚ\s+BIÊN", "ĐÓNG CHÚ BIÊN"),
    (r"CHỦ\s+ĐẾ\s+\d|CHỦ\s+ĐỂ\s+\d", "CHỦ ĐẾ/ĐỂ"),
    (r"đon\s+giản", "đon giản -> đơn giản"),
    (r"dãy\s+sô\b", "dãy sô -> dãy số"),
    (r"hiêu\s+được", "hiêu được -> hiểu được"),
    (r"hiêu\s+quả", "hiêu quả -> hiệu quả"),
    (r"gỡ\s+lối", "gỡ lối -> gỡ lỗi"),
    (r"mô\s+hinh\b", "mô hinh -> mô hình"),
    (r"điều\s+chinh\b", "điều chinh -> điều chỉnh"),
    (r"tối\s+vu\b", "tối vu -> tối ưu"),
    (r"xây\s+dụng\b", "xây dụng -> xây dựng"),
    (r"mã\s+hoa\s+thành", "mã hoa thành -> mã hoá thành"),
    (r"sứ\s+dụng\b", "sứ dụng -> sử dụng"),
    (r"ngôn\s+ngừ\b", "ngôn ngừ -> ngôn ngữ"),
    (r"ứng\s+đụng\b", "ứng đụng -> ứng dụng"),
    (r"giài\s+thích", "giài thích -> giải thích"),
    (r"đươc\b", "đươc -> được"),
    (r"VẬN\s+ANH\b|VÁN\s+ANH\b", "VÂN ANH typo"),
    (r"CÁC\s+TÁC\s+GIÁ", "CÁC TÁC GIÁ"),
    (r"về\s+tranh\s+vẽ|bằng\s+hình\s+ảnh,\s+về\s+tranh", "về tranh"),
]


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
            # try to find matching ancestor
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
    lessons = json.loads((DATA_DIR / "lessons-lop-12.json").read_text(encoding="utf-8"))
    books = json.loads((DATA_DIR / "books.json").read_text(encoding="utf-8"))
    search_items = json.loads((DATA_DIR / "search-lop-12.json").read_text(encoding="utf-8"))

    assert len(lessons) == 22, f"Expected 22 lessons, got {len(lessons)}"
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
    lop12_book = next((b for b in books_list if b.get("id") == "lop-12"), None)
    assert lop12_book is not None, "Missing lop-12 in books.json"
    hits = []

    def scan_blob(label, text):
        for pat, desc in FORBIDDEN_PATTERNS:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                start = max(0, m.start() - 25)
                end = min(len(text), m.end() + 25)
                ctx = text[start:end].replace("\n", " ")
                hits.append(f"[{label}] {desc}: ...{ctx}...")

    for les in lessons:
        # Check non-code content for Vietnamese spelling typos
        prose = re.sub(r'<div class="code-block-wrapper">.*?</div>\s*</div>|<pre><code.*?>.*?</code></pre>', ' ', les["html"], flags=re.S)
        prose = re.sub(r'<[^>]+>', ' ', prose)
        scan_blob(les["id"], prose)
        scan_blob(f"{les['id']}:summary", les.get("summary", ""))
        scan_blob(f"{les['id']}:title", les.get("title", ""))

    for grp in lop12_book.get("toc", []):
        for b_les in grp.get("items", []):
            scan_blob(f"books.json:{b_les['id']}", b_les.get("summary", "") + " " + b_les.get("title", ""))

    for s_les in search_items:
        scan_blob(f"search.json:{s_les['id']}", s_les.get("content", "") + " " + s_les.get("title", ""))

    print(f"[CHECK 2] Forbidden OCR patterns scan: {len(hits)} hits")
    for h in hits[:30]:
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
            # Filter pip install shell lines
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
    print(f"[CHECK 4a] HTML tag balance across 22 files: {len(tag_errors)} issues")
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

    # Extra domain/valid Vietnamese/English words expected in Grade 12 AI textbook
    EXTRA_VALID = {
        "ai", "agent", "agents", "llm", "llms", "rag", "prompt", "prompts", "chunking", "chunk", "chunks",
        "embedding", "embeddings", "vector", "vectors", "store", "stores", "retrieval", "augmented",
        "generation", "mindstudio", "langchain", "llamaindex", "huggingface", "openai", "gemini", "chatgpt",
        "python", "pip", "colab", "numpy", "pandas", "matplotlib", "sklearn", "scikit", "learn", "kaggle",
        "regression", "classification", "linear", "gradient", "descent", "mse", "loss", "epoch", "epochs",
        "learning", "rate", "bias", "fairness", "deepfake", "api", "apis", "json", "csv", "pdf", "txt",
        "docx", "html", "css", "url", "http", "https", "google", "search", "gmail", "drive", "youtube",
        "workflow", "workflows", "input", "output", "block", "blocks", "model", "models", "token", "tokens",
        "context", "window", "temperature", "top", "system", "user", "assistant", "chain", "chains",
        "tool", "tools", "memory", "planning", "action", "actions", "feedback", "loop", "loops",
        "nearest", "neighbors", "cosine", "similarity", "faiss", "chroma", "pinecone", "database",
        "streamlit", "gradio", "github", "vercel", "demo", "slide", "slides", "rubric", "kpi",
        "stem", "thpt", "sgk", "nxb", "tnhh", "gd", "hn", "hcm", "tp", "thcs", "vn", "vnd",
        "chatgpt", "claude", "copilot", "siri", "alexa", "chatbot", "chatbots", "transformer",
        "transformers", "attention", "zero", "few", "shot", "cot", "thought", "hallucination",
        "privacy", "security", "copyright", "ethics", "ethical", "responsible", "transparency",
        "accountability", "interpretability", "explainable", "dataset", "datasets", "train", "test",
        "split", "overfitting", "underfitting", "feature", "features", "label", "labels", "target",
        "supervised", "unsupervised", "reinforcement", "outlier", "outliers", "missing", "normalization",
        "standardization", "metric", "metrics", "accuracy", "precision", "recall", "score", "variance",
        "rmse", "mae", "r2", "slope", "intercept", "weights", "weight", "parameters", "parameter",
        "hyperparameter", "hyperparameters", "optimization", "optimizer", "iteration", "iterations",
        "converge", "convergence", "minimum", "local", "global", "matrix", "scalar", "array", "arrays",
        "dataframe", "series", "plot", "scatter", "xlabel", "ylabel", "title", "legend", "show",
        "import", "from", "def", "return", "print", "true", "false", "none", "verbose",
        "giai", "hoá", "hóa", "kĩ", "kỹ", "lí", "lý", "mĩ", "mỹ", "tỉ", "tỷ", "qui", "quy",
        "bốn", "chín", "mươi", "linh", "trăm", "nghìn", "vạn", "triệu", "tỉ",
        "st25", "gpt", "3kg", "hki", "hkii", "cô", "anh", "chị", "minh", "an", "châu", "nam", "hùng",
        "hà", "linh", "hoa", "ngọc", "long", "lan", "phương", "phụng", "tuấn", "bình", "dũng", "tuấn",
        "dương", "thủy", "thắng", "oanh", "hải", "hiền", "hiếu", "hoài", "hoàng", "vân", "làn", "quản",
        "hoà", "hòa", "khoá", "khóa", "toán", "toả", "tỏa", "loà", "lòa", "ngoà", "ngòa", "xoá", "xóa",
        "toạ", "tọa", "đoạ", "đọa", "hoạ", "họa", "thoả", "thỏa", "chú", "tiêu", "chủ",
        "kể", "kết", "kị", "từ", "vì", "ai", "agent", "v.v", "tức", "như", "để", "nên", "nếu", "vậy",
        "web", "app", "apps", "code", "coding", "bug", "bugs", "debug", "debugging", "log", "logs",
        "prompting", "fine", "tuning", "pre", "trained", "open", "source", "closed", "metadata",
        "indexing", "index", "query", "queries", "rank", "ranking", "rerank", "reranking", "hybrid",
        "semantic", "keyword", "keywords", "chunker", "splitter", "recursive", "character",
        "auto", "autonomous", "orchestration", "planner", "executor", "critic", "reflect", "reflection",
        "automation", "automate", "api-key", "apikey", "endpoint", "server", "client", "cloud",
        "vnpay", "momo", "shopee", "lazada", "tiki", "tiktok", "facebook", "zalo", "excel", "word",
        "powerpoint", "canva", "figma", "notion", "trello", "jira", "slack", "discord",
        "gdpr", "unesco", "oecd", "eu", "mit", "stanford", "nvidia", "tesla", "deepmind", "anthropic",
        "meta", "llama", "mistral", "qwen", "deepseek", "cohere", "bedrock", "azure", "aws",
        "covid", "iot", "vr", "ar", "cv", "nlp", "ml", "dl", "nn", "cnn", "rnn", "lstm", "gan",
        "knn", "svm", "dt", "rf", "xgb", "pca", "k-means", "k-nn", "f1", "roc", "auc",
        "ocr", "tts", "stt", "asr", "ner", "pos", "vqa", "rlhf", "lora", "qlora", "gguf",
    }
    vocab.update(EXTRA_VALID)

    # Check only words containing Vietnamese diacritics that are NOT in vocab (this reliably catches corrupted tones!)
    VI_DIACRITIC_RE = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", re.I)
    WORD_RE = re.compile(r"[A-Za-zÀ-ỹ]+")
    MISSING_TONE_SUSPECTS = {
        "chinh", "xac", "duoc", "khong", "nhung", "thuong", "luong", "nguoi", "hinh",
        "du", "lieu", "cau", "hoi", "tra", "loi", "kiem", "tra", "hieu", "qua", "toan",
        "phuong", "trinh", "chuong", "nhieu", "thuc", "hanh", "phat", "trien", "ung",
        "dung", "ngon", "ngu", "bang", "tu", "vung", "moi", "truong", "gia", "tri",
        "san", "pham", "cong", "nghe", "thong", "tin", "chuc", "nang", "mo", "ta",
    }

    unknown = {}
    tone_missing_hits = []
    for les in lessons:
        # strip code blocks & tags & figure captions? Keep figcaption because we also want clean captions!
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
            elif wl in MISSING_TONE_SUSPECTS:
                # Filter expected non-accented English/brand/code tokens like "to" or "van" -> none in set above
                ctx = txt[max(0, m.start()-20):min(len(txt), m.end()+20)].replace("\n", " ")
                tone_missing_hits.append(f"{les['id']}: {w!r} in ...{ctx}...")

    sorted_unk = sorted(unknown.items(), key=lambda kv: (-kv[1]["count"], kv[0]))
    print(f"[CHECK 4b] Diacritic words not in vi_50k + domain list: {len(sorted_unk)} distinct tokens")
    for w, info in sorted_unk[:80]:
        ls = ", ".join(sorted(info["lessons"])[:3])
        print(f"  {info['raw']} ({info['count']}x) in [{ls}]")
    print(f"[CHECK 4c] Potential missing-tone ASCII Vietnamese suspects: {len(tone_missing_hits)}")
    for t in tone_missing_hits[:40]:
        print("  SUSPECT:", t)
    return sorted_unk, tone_missing_hits


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
