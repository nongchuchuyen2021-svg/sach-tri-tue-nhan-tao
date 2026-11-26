import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "scripts" / "audit_report.json", encoding="utf-8") as f:
    report = json.load(f)

# Words that are valid English or code or math variables
safe_terms = {
    "generate", "settings", "no-code/low-code", "workflow", "analyze", "localhost",
    "http/1", "11434/api/chat", "www", "jupyter", "01-stk", "sedidco", "function",
    "object", "notation", "aistudio", "ctrl", "automations", "scrape", "if/else",
    "cau_hoi", "label", "cau_hoi_khach_hang", "thong_tin_tim_kiem", "include", "chunk",
    "documents", "logging", "httpx", "y_pred", "utf-8", "google-generativeai",
    "langchain-core", "langchain-community", "llama-index", "ollama", "st25",
    "csv", "json", "png", "jpg", "jpeg", "pdf", "docx", "pptx", "txt", "mp3", "mp4",
    "coca-cola", "000đ", "10a", "10a2", "14h00", "50k", "v1", "v2", "v3", "2d", "3d",
    "4d", "x_train", "y_train", "x_test", "y_test", "x_val", "y_val", "lr", "loss_fn",
    "optimizer", "relu", "sigmoid", "softmax", "epoch_loss", "model.fit", "model.predict",
    "train_test_split", "mean_squared_error", "standardscaler", "minmaxscaler"
}

# Collect all real errors with their corrections
errors_to_inspect = []

for item in report:
    b = item["book"]
    lid = item["lesson"]
    line = item["line"]
    words = item["suspicious"]
    
    # filter out known safe terms
    susp = [w for w in words if w.lower() not in safe_terms and not w.isdigit()]
    if susp:
        errors_to_inspect.append((b, lid, line, susp))

print(f"Total lines with genuine potential errors: {len(errors_to_inspect)}")

with open(ROOT / "scripts" / "genuine_errors.txt", "w", encoding="utf-8") as f:
    for b, lid, line, susp in errors_to_inspect:
        f.write(f"[{b}/{lid}] SUSP: {susp}\n  LINE: {line}\n\n")

print("Saved to scripts/genuine_errors.txt!")
