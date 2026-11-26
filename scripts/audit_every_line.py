import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

# Load vi_50k words
vi_words = set(w.lower().strip() for w in open(ROOT / "scripts" / "vi_50k.txt", encoding="utf-8"))

# Add common valid vietnamese syllables that might be missing in vi_50k
extra_valid_vi = {
    "ở", "và", "là", "có", "được", "cho", "của", "trong", "một", "các", "những",
    "người", "với", "không", "này", "khi", "để", "từ", "nhiều", "đã", "sẽ",
    "học", "sinh", "bài", "sách", "giáo", "khoa", "thực", "hành", "luyện", "tập",
    "vận", "dụng", "khởi", "động", "khám", "phá", "mục", "tiêu", "chủ", "đề",
    "mô", "hình", "ngôn", "ngữ", "lớn", "trí", "tuệ", "nhân", "tạo", "tạo", "sinh",
    "dữ", "liệu", "huấn", "luyện", "thông", "tin", "chính", "xác", "công", "cụ",
    "thuật", "toán", "mạng", "nơ-ron", "nơ", "ron", "hệ", "thống", "ứng", "dụng",
    "đạo", "đức", "pháp", "luật", "văn", "hóa", "trách", "nhiệm", "công", "dân",
    "kỉ", "nguyên", "nghề", "nghiệp", "môi", "trường", "phát", "triển", "dự", "án",
    "bảng", "giải", "thích", "thuật", "ngữ", "lời", "nói", "đầu", "mục", "lục",
    "phần", "biệt", "thật", "giả", "thiên", "vị", "hiểu", "lầm", "tác", "hại",
    "hỗ", "trợ", "giao", "tiếp", "kĩ", "năng", "cơ", "bản", "nâng", "cao",
    "sáng", "lập", "trình", "tạo", "ảnh", "video", "tối", "ưu", "hóa", "ý", "tưởng",
    "lập", "kế", "hoạch", "xây", "dựng", "sản", "phẩm", "hoàn", "chỉnh", "trình",
    "bày", "kết", "quả", "hồi", "quy", "phân", "loại", "cụm", "nguyên", "lí",
    "khai", "thác", "thư", "viện", "nguồn", "mở", "quyền", "con", "hộp", "kiến", "thức",
    "cốt", "lõi", "thảo", "luận", "câu", "hỏi", "tình", "huống", "ví", "dụ", "bước",
    "hướng", "dẫn", "chi", "tiết", "ghi", "nhớ", "cô", "đọng", "thích", "nghi",
    "độc", "lập", "tốc", "độ", "tiếp", "thu", "tư", "duy", "logic", "suy", "nghĩ",
    "thay", "đổi", "vượt", "qua", "khó", "khăn", "kinh", "nghiệm", "tương", "tác",
    "sinh", "học", "tiến", "hóa", "não", "bộ", "linh", "hoạt", "ý", "thức", "bản", "thân",
    "lỗi", "sai", "lầm", "lí", "tưởng", "cảm", "xúc", "chiều", "sâu", "nhanh", "chóng",
    "máy", "móc", "phần", "mềm", "bắt", "chước", "khác", "biệt", "căn", "bản", "giới", "hạn",
    "mở", "rộng", "đặc", "điểm", "riêng", "mỗi", "loại", "văn", "bản", "hình", "ảnh", "âm", "thanh",
    "chữ", "viết", "tranh", "vẽ", "đoạn", "nhạc", "bài", "hát", "giọng", "nói", "khuôn", "mặt",
    "vân", "tay", "mở", "khóa", "camera", "cảm", "biến", "điện", "thoại", "thông", "minh"
}

vi_words.update(extra_valid_vi)

# Technical / proper noun allowed words
allowed = {
    "ai", "llm", "llms", "agent", "agents", "prompt", "prompts", "prompting", "chatgpt", "gemini",
    "copilot", "claude", "rag", "api", "apis", "python", "numpy", "pandas", "plt", "fig",
    "matplotlib", "langchain", "llamaindex", "ollama", "mindstudio", "flowise", "openai",
    "google", "microsoft", "meta", "facebook", "youtube", "tiktok", "apple", "siri",
    "alexa", "faceid", "touchid", "qr", "gpu", "cpu", "ram", "ssd", "usb", "pc", "app",
    "apps", "web", "website", "html", "css", "javascript", "js", "url", "http", "https",
    "vector", "store", "embedding", "embeddings", "chunking", "tokens", "token", "zero",
    "shot", "few", "one", "chain", "thought", "loss", "epoch", "epochs", "mse", "gradient",
    "descent", "learning", "rate", "dataset", "train", "test", "validation", "overfitting",
    "underfitting", "bias", "variance", "outliers", "noise", "accuracy", "precision", "recall",
    "f1", "regression", "classification", "clustering", "kmeans", "knn", "svm", "neural",
    "network", "neuron", "neurons", "deep", "machine", "reinforcement", "supervised",
    "unsupervised", "multimodal", "generative", "genai", "diffusion", "midjourney", "dall",
    "sora", "runway", "pika", "suno", "musicgen", "voicemod", "stable", "inpainting",
    "outpainting", "hallucination", "temperature", "top", "context", "window", "nlp", "cv",
    "ui", "ux", "nocode", "code", "debug", "debugger", "run", "start", "selection", "terminal",
    "console", "log", "import", "def", "return", "print", "true", "false", "none", "self",
    "class", "for", "while", "if", "else", "elif", "in", "is", "not", "and", "or", "try",
    "except", "with", "as", "from", "int", "float", "str", "bool", "list", "dict", "tuple",
    "len", "range", "zip", "enumerate", "lambda", "args", "kwargs", "main", "init", "name",
    "value", "key", "keys", "values", "items", "append", "extend", "insert", "remove", "pop",
    "index", "count", "sort", "reverse", "split", "join", "strip", "replace", "lower", "upper",
    "title", "find", "startswith", "endswith", "format", "encode", "decode", "open", "read",
    "write", "close", "json", "dumps", "loads", "dump", "load", "math", "random", "os", "sys",
    "re", "datetime", "time", "sleep", "request", "requests", "response", "status", "headers",
    "body", "params", "query", "payload", "result", "results", "output", "input", "error",
    "errors", "warn", "warning", "info", "debug", "trace", "step", "steps", "task", "tasks",
    "user", "assistant", "system", "role", "content", "model", "messages", "message", "text",
    "choice", "choices", "finish", "reason", "usage", "total", "prompt_tokens", "completion_tokens",
    "vinamilk", "minh", "lan", "nam", "an", "hải", "cường", "linh", "hoa", "khoa", "bình",
    "hà", "đặng", "cao", "tùng", "hoàng", "thị", "mai", "lê", "anh", "vinh", "vũ", "trung",
    "chính", "nguyễn", "quang", "đức", "chí", "thanh", "văn", "luân", "phạm", "tuấn", "sa", "đéc",
    "đồng", "tháp", "bgdđt", "gdpt", "thpt", "thcs", "sgk", "nxb", "đkxb", "qđ", "isbn",
    "slide", "slides", "powerpoint", "canva", "craiyon", "copilot", "chat", "bing", "bard",
    "chatbot", "colab", "kaggle", "deepfake", "configuration", "agi", "variable", "framework",
    "language", "gd", "qđxb", "augmented", "retrieval", "gpt", "canvas", "vnd", "llama",
    "connectors", "indexes", "vnđ", "hki", "hkii", "scatter", "plot", "grad", "unesco",
    "markdown", "gtts", "tuoi", "lahocsinh", "criteria", "tuning", "processing", "imagen",
    "source", "create", "data", "studio", "google", "media", "support", "vector", "machines",
    "k-means", "support", "loss_hist", "xlabel", "ylabel", "verbose", "epochs", "login", "create",
    "account", "welcome", "back", "imagen", "imagen-3", "seed", "aspect", "ratio", "negative",
    "cinematic", "photorealistic", "ultra", "realistic", "4k", "8k", "lighting", "dramatic",
    "shot", "angle", "close-up", "wide", "landscape", "portrait", "isometric", "cyberpunk",
    "steampunk", "anime", "watercolor", "oil", "painting", "pencil", "sketch", "coca-cola",
    "coca", "cola", "st25", "lit", "lít", "kg", "vnd/lit", "vnd/kg", "vnd/lon"
}

# Scan every lesson and report all suspicious lines
report = []

for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    lessons = json.loads(lp.read_text(encoding="utf-8"))
    for les in lessons:
        html = les.get("html", "")
        # Split into blocks / lines
        lines = re.split(r"</?(?:p|li|h[1-6]|div|tr|td|th)[^>]*>", html)
        for lno, line in enumerate(lines):
            clean_line = re.sub(r"<[^>]+>", " ", line).strip()
            if not clean_line or len(clean_line) < 3:
                continue
            # Extract words
            tokens = re.findall(r"\b[a-zA-ZàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđA-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ0-9_/-]+\b", clean_line)
            suspicious_words = []
            for t in tokens:
                tl = t.lower().strip("-_/")
                if not tl or tl.isdigit() or re.match(r"^\d+([.,]\d+)?(px|%|em|rem|k|m|b|s|ms|fps)?$", tl):
                    continue
                if tl not in vi_words and tl not in allowed:
                    # check if word is hyphenated
                    parts = tl.split("-")
                    if all(p in vi_words or p in allowed for p in parts):
                        continue
                    # Flag this word
                    suspicious_words.append(t)
            if suspicious_words:
                report.append((b, les['id'], clean_line, suspicious_words))

print(f"Total lines with suspicious words: {len(report)}")
# Save full report to file
with open(ROOT / "scripts" / "audit_report.json", "w", encoding="utf-8") as f:
    json.dump([{"book": b, "lesson": lid, "line": line, "suspicious": sw} for b, lid, line, sw in report], f, ensure_ascii=False, indent=2)

print("First 30 suspicious occurrences:")
for b, lid, line, sw in report[:30]:
    print(f"[{b}/{lid}] Words: {sw}")
    print(f"   Line: {line[:100]}...")
