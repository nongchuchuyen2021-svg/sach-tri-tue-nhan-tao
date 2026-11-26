import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

# Load vi_50k
with open(ROOT / 'scripts/vi_50k.txt', encoding='utf-8') as f:
    valid_words = set(w.strip().lower() for w in f if w.strip())

# Common English and technical words in AI books
TECH_WORDS = {
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
    'w1', 'w2', 'b1', 'b2', 'x1', 'x2', 'y1', 'y2', 'dx', 'dy', 'dw', 'db',
    'sinh', 'tuệ', 'lập', 'trình', 'giáo', 'khoa', 'tin', 'học', 'nguyễn', 'trần', 'lê', 'phạm',
    'hoàng', 'huỳnh', 'phan', 'vũ', 'võ', 'đặng', 'bùi', 'đỗ', 'hồ', 'ngô', 'dương', 'lý',
    'việt', 'nam', 'hà', 'nội', 'huế', 'đà', 'nẵng', 'sài', 'gòn', 'hồ', 'chí', 'minh',
    'giáo', 'dục', 'xuất', 'bản', 'tri', 'thức', 'kết', 'nối', 'cánh', 'diều', 'chân', 'trời', 'sáng', 'tạo'
}
valid_words.update(TECH_WORDS)

def scan_book(book_id):
    path = ROOT / 'data' / f'lessons-{book_id}.json'
    with open(path, encoding='utf-8') as f:
        lessons = json.load(f)
        
    print(f'\n========================================')
    print(f'=== SCANNING {book_id} ===')
    print(f'========================================')
    
    anomalies = []
    word_freq = Counter()
    conjoined_freq = Counter()
    
    for les in lessons:
        les_id = les.get('id', '')
        html = les.get('html', '')
        
        # Check conjoined words: e.g. chùngta, từ1, 1giờ, textWord, etc.
        # Find token with mixed lower and digit or lower followed by digit
        conjoined_nums = re.findall(r'([a-zA-Zà-ỹÀ-Ỹ]+[0-9]+|[0-9]+[a-zA-Zà-ỹÀ-Ỹ]+)', html)
        for c in conjoined_nums:
            if not re.match(r'^(x[1-9]|y[1-9]|w[1-9]|b[1-9]|h[1-6]|gpt[34]|v[0-9]|d[0-9]|3d|2d|4k|mp[34]|f[1-9]|fig[0-9]|p[0-9]|l[0-9]|c[0-9])$', c.lower()):
                conjoined_freq[c] += 1
                anomalies.append((les_id, 'CONJOINED_NUM', c))
                
        # Split into text lines
        text = re.sub(r'<[^>]+>', ' ', html)
        tokens = re.findall(r'[a-zA-Zà-ỹÀ-Ỹ_]+', text)
        for t in tokens:
            tl = t.lower()
            if tl in valid_words or len(tl) <= 1:
                continue
            # Check if compound hyphenated or snake_case
            parts = tl.split('_')
            if all(p in valid_words or p in TECH_WORDS for p in parts if p):
                continue
            word_freq[t] += 1
            
    print(f'Top conjoined num/letter patterns:')
    for c, cnt in conjoined_freq.most_common(20):
        print(f'  {c}: {cnt}')
        
    print(f'\nTop unknown words:')
    for w, cnt in word_freq.most_common(50):
        print(f'  {w}: {cnt}')
        
    return word_freq, conjoined_freq

scan_book('lop-11')
scan_book('lop-10')
scan_book('lop-12')
