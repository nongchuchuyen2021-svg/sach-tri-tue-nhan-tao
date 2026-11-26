import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Load vi_50k words
vi_words = set(w.lower().strip() for w in open(ROOT / "scripts" / "vi_50k.txt", encoding="utf-8"))

# Common allowed english tech words and proper nouns
allowed = {
    "ai", "llm", "agent", "agents", "prompt", "prompts", "prompting", "chatgpt", "gemini",
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
    "slide", "slides", "powerpoint", "canva", "craiyon", "copilot", "chat", "bing", "bard"
}

# Scan each book line by line
unrecognized = Counter()
unrec_examples = {}

for b in ["lop-10", "lop-11", "lop-12"]:
    p = ROOT / "data" / f"lessons-{b}.json"
    data = json.load(open(p, encoding="utf-8"))
    for les in data:
        html = les.get("html", "")
        clean = re.sub(r"<[^>]+>", "\n", html)
        for line in clean.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            words = re.findall(r"\b[a-zA-ZàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđA-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]+\b", line_str)
            for w in words:
                wl = w.lower()
                if wl not in vi_words and wl not in allowed and not re.match(r"^\d+$", wl):
                    unrecognized[wl] += 1
                    if wl not in unrec_examples:
                        unrec_examples[wl] = (b, les['id'], line_str)

print(f"Total unrecognized word types: {len(unrecognized)}")
print("\nTop 100 most frequent unrecognized words:")
for w, cnt in unrecognized.most_common(100):
    b, lid, sample = unrec_examples[w]
    print(f"[{w}] (x{cnt}) in {b}/{lid}: ...{sample[:80]}...")
