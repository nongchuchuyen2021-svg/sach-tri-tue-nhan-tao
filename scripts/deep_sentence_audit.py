import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load vi_50k
with open(ROOT / 'scripts/vi_50k.txt', encoding='utf-8') as f:
    valid_words = set(w.strip().lower() for w in f if w.strip())

# Whitelist common tech and proper nouns
WHITELIST = {
    'ai', 'prompt', 'prompts', 'chatgpt', 'gpt', 'llm', 'llms', 'transformer', 'attention',
    'self-attention', 'encoder', 'decoder', 'token', 'tokens', 'tokenizer', 'embedding',
    'embeddings', 'python', 'code', 'def', 'import', 'print', 'return', 'class', 'for', 'in',
    'if', 'else', 'elif', 'while', 'true', 'false', 'none', 'range', 'len', 'str', 'int', 'float',
    'faceid', 'touchid', 'siri', 'alexa', 'gemini', 'copilot', 'midjourney', 'stable', 'diffusion',
    'dall-e', 'suno', 'runway', 'pika', 'deepseek', 'claude', 'bert', 'resnet', 'yolo', 'cnn', 'rnn',
    'lstm', 'gan', 'reinforcement', 'learning', 'machine', 'deep', 'supervised', 'unsupervised',
    'few-shot', 'one-shot', 'zero-shot', 'chain-of-thought', 'cot', 'rag', 'api', 'dataset',
    'epoch', 'batch', 'loss', 'gradient', 'descent', 'learning_rate', 'adam', 'relu', 'softmax',
    'sigmoid', 'overfitting', 'underfitting', 'bias', 'variance', 'accuracy', 'precision',
    'recall', 'f1-score', 'iou', 'bbox', 'pixel', 'rgb', 'fps', 'gpu', 'tpu', 'cpu', 'ram',
    'html', 'css', 'javascript', 'json', 'url', 'http', 'https', 'pdf', 'mp3', 'mp4', 'wav',
    'png', 'jpg', 'jpeg', 'svg', 'figma', 'canva', 'colab', 'jupyter', 'kaggle', 'github',
    'genai', 'ai-generated', 'multimodal', 'vector', 'matrix', 'tensor', 'tensorflow', 'pytorch',
    'numpy', 'pandas', 'matplotlib', 'sklearn', 'scikit-learn', 'seaborn', 'keras', 'opencv', 'cv2',
    'plt', 'np', 'pd', 'tf', 'nn', 'cuda', 'bert-base', 'gpt-4', 'gpt-3.5', 'llama', 'mistral',
    'whisper', 'clip', 'blip', 'lora', 'qlora', 'peft', 'fine-tuning', 'pre-training',
    'temperature', 'top_p', 'top_k', 'max_tokens', 'presence_penalty', 'frequency_penalty',
    'system_prompt', 'user_prompt', 'assistant', 'system', 'user', 'role', 'content',
    'input', 'output', 'target', 'feature', 'label', 'train', 'test', 'val', 'valid', 'split',
    'fit', 'predict', 'score', 'evaluate', 'history', 'plot', 'show', 'figure', 'ax', 'sub',
    'x_train', 'y_train', 'x_test', 'y_test', 'x_val', 'y_val', 'w', 'b', 'x', 'y', 'z',
    'w1', 'w2', 'b1', 'b2', 'x1', 'x2', 'y1', 'y2', 'dx', 'dy', 'dw', 'db', 'x2', 'y2',
    'thpt', 'bgdđt', 'gdpt', 'isbn', 'qđxb', 'nlp', 'knn', 'inpainting', 'outpainting',
    'retrieval', 'augmented', 'generation', 'generate', 'llamaindex', 'langchain', 'mindstudio',
    'ollama', 'vinamilk', 'shopee', 'autopilot', 'lidar', 'craiyon', 'musicgen', 'voicemod',
    'deepfake', 'hallucination', 'unesco', 'markdown', 'gtts', 'pycharm', 'aqi', 'mse', 'canvas',
    'connectors', 'indexes', 'variable', 'workflow', 'scrape', 'chunking', 'chunk', 'httpx',
    'nguyễn', 'trần', 'lê', 'phạm', 'hoàng', 'huỳnh', 'phan', 'vũ', 'võ', 'đặng', 'bùi', 'đỗ',
    'hồ', 'ngô', 'dương', 'lý', 'đinh', 'hà', 'nội', 'huế', 'đà', 'nẵng', 'sài', 'gòn',
    'kim', 'lân', 'vợ', 'nhặt', 'lưu', 'thế', 'sơn', 'mai', 'anh', 'vinh', 'luân'
}
valid_words.update(WHITELIST)

# Rare accents that are almost always OCR errors in school textbooks
SUSPICIOUS_WORDS = {
    'giài', 'bải', 'cành', 'thém', 'đoan', 'hòi', 'tôm', 'mỏ', 'mò', 'đòng', 'hò', 'chúngta',
    'từ1', 'co', 'bán', 'bàn', 'cầu', 'vl', 'lạo', 'thô', 'sinhx', 'côsin', 'luàn', 'tưy',
    'mỗn', 'họạ', 'chíp', 'chịp', 'sô', 'lăn', 'gáp', 'lạp', 'càn', 'hằng', 'cà', 'thào',
    'giái', 'rờ', 'lôi', 'dũ', 'bậu', 'huân', 'luyên', 'trom', '1lms', 'ok'
}

def audit_book(book_id):
    path = ROOT / 'data' / f'lessons-{book_id}.json'
    with open(path, encoding='utf-8') as f:
        lessons = json.load(f)
        
    results = []
    for les in lessons:
        les_id = les.get('id', '')
        html = les.get('html', '')
        # Split into sentences or lines
        raw_lines = re.split(r'</?(?:p|li|h[1-6]|div|tr|td|th|blockquote|br)[^>]*>', html)
        for raw_line in raw_lines:
            line = re.sub(r'<[^>]+>', ' ', raw_line).strip()
            line = re.sub(r'\s+', ' ', line)
            if not line:
                continue
                
            # Check for words in line
            words = re.findall(r'[a-zA-Zà-ỹÀ-Ỹ0-9_]+', line)
            line_issues = []
            for w in words:
                wl = w.lower()
                if wl in SUSPICIOUS_WORDS:
                    line_issues.append(f"SUSPICIOUS_WORD: {w}")
                elif wl not in valid_words and not wl.isdigit():
                    # Check if compound
                    parts = wl.split('_')
                    if not all(p in valid_words for p in parts if p):
                        line_issues.append(f"UNKNOWN_WORD: {w}")
                        
            # Check conjoined
            conjoined = re.findall(r'([a-zA-Zà-ỹÀ-Ỹ]+[0-9]+|[0-9]+[a-zA-Zà-ỹÀ-Ỹ]+)', line)
            for c in conjoined:
                if not re.match(r'^(x[1-9]|y[1-9]|w[1-9]|b[1-9]|h[1-6]|gpt[34]|v[0-9]|d[0-9]|3d|2d|4k|mp[34]|f[1-9]|fig[0-9]|p[0-9]|l[0-9]|c[0-9]|st25|a1|10a|14h)$', c.lower()):
                    line_issues.append(f"CONJOINED: {c}")
                    
            if line_issues:
                results.append({
                    'lesson': les_id,
                    'issues': line_issues,
                    'line': line
                })
    return results

all_results = {}
for b in ['lop-10', 'lop-11', 'lop-12']:
    res = audit_book(b)
    all_results[b] = res
    print(f"[{b}] Found {len(res)} lines with issues.")

with open(ROOT / 'scripts/all_book_issues.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
