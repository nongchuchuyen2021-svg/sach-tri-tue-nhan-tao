import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / 'scripts/vi_50k.txt', encoding='utf-8') as f:
    valid_words = set(w.strip().lower() for w in f if w.strip())

# Technical / proper words
TECH = {
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
    'thpt', 'bgdđt', 'gdpt', 'isbn', 'qđxb', 'nlp', 'knn', 'inpainting', 'outpainting',
    'retrieval', 'augmented', 'generation', 'generate', 'llamaindex', 'langchain', 'mindstudio',
    'ollama', 'vinamilk', 'shopee', 'autopilot', 'lidar', 'craiyon', 'musicgen', 'voicemod',
    'deepfake', 'hallucination', 'unesco', 'markdown', 'gtts', 'pycharm', 'aqi', 'mse', 'canvas',
    'connectors', 'indexes', 'variable', 'workflow', 'scrape', 'chunking', 'chunk', 'httpx',
    'nguyễn', 'trần', 'lê', 'phạm', 'hoàng', 'huỳnh', 'phan', 'vũ', 'võ', 'đặng', 'bùi', 'đỗ',
    'hồ', 'ngô', 'dương', 'lý', 'đinh', 'hà', 'nội', 'huế', 'đà', 'nẵng', 'sài', 'gòn',
    'kim', 'lân', 'vợ', 'nhặt', 'lưu', 'thế', 'sơn', 'mai', 'anh', 'vinh', 'luân', 'thanh', 'nam',
    'bình', 'an', 'hải', 'hà', 'hùng', 'minh', 'lan', 'thảo', 'tùng', 'hoa', 'tuấn', 'quang',
    'text-to-image', 'image-to-image', 'text-to-video', 'image-to-video', 'text-to-speech', 'speech-to-text',
    'cosin', 'k-means', 'dbscan', 'gmm', 'svm', 'ann', 'rlhf', 'veo', 'imagen', 'media', 'w3schools', 'mdn',
    'docs', 'colab', 'aistudio', 'google', 'openai', 'midjourney', 'runway', 'claude', 'copilot', 'gemini'
}
valid_words.update(TECH)

lp = ROOT / "data" / "lessons-lop-11.json"
with open(lp, encoding="utf-8") as f:
    lessons = json.load(f)

unrecognized = {}
for les in lessons:
    les_id = les["id"]
    html = les.get("html", "")
    text = re.sub(r'<[^>]+>', ' ', html)
    tokens = re.findall(r'[a-zA-Zà-ỹÀ-Ỹ_]+', text)
    for tok in tokens:
        tl = tok.lower()
        if tl in valid_words or len(tl) <= 1:
            continue
        # Split on underscore
        parts = tl.split('_')
        if all(p in valid_words for p in parts if p):
            continue
        unrecognized[tok] = unrecognized.get(tok, 0) + 1

print(f"Unrecognized unique tokens in lop-11: {len(unrecognized)}")
for k, v in sorted(unrecognized.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
