import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load vi_50k
with open(ROOT / 'scripts/vi_50k.txt', encoding='utf-8') as f:
    valid_words = set(w.strip().lower() for w in f if w.strip())

# Common English technical words
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
    'w1', 'w2', 'b1', 'b2', 'x1', 'x2', 'y1', 'y2', 'dx', 'dy', 'dw', 'db', 'x2', 'y2',
    'thpt', 'bgdđt', 'gdpt', 'isbn', 'qđxb', 'nlp', 'knn', 'inpainting', 'outpainting',
    'retrieval', 'augmented', 'generation', 'generate', 'llamaindex', 'langchain', 'mindstudio',
    'ollama', 'vinamilk', 'shopee', 'autopilot', 'lidar', 'craiyon', 'musicgen', 'voicemod',
    'deepfake', 'hallucination', 'unesco', 'markdown', 'gtts', 'pycharm', 'aqi', 'mse', 'canvas',
    'connectors', 'indexes', 'variable', 'workflow', 'scrape', 'chunking', 'chunk', 'httpx',
    'nguyễn', 'trần', 'lê', 'phạm', 'hoàng', 'huỳnh', 'phan', 'vũ', 'võ', 'đặng', 'bùi', 'đỗ',
    'hồ', 'ngô', 'dương', 'lý', 'đinh', 'hà', 'nội', 'huế', 'đà', 'nẵng', 'sài', 'gòn',
    'kim', 'lân', 'vợ', 'nhặt', 'lưu', 'thế', 'sơn', 'mai', 'anh', 'vinh', 'luân', 'thanh', 'nam',
    'bình', 'an', 'hải', 'hà', 'hùng', 'minh', 'lan', 'thảo', 'tùng', 'hoa', 'tuấn', 'quang'
}
valid_words.update(TECH_WORDS)

# Contextual ngram anomalies where individual words may be valid, but combination is wrong
CONTEXT_TYPO_PATTERNS = [
    # Common OCR letter shifts
    (r'\blự\s+(động|chọn|khám phá|giác|nhận thức)', 'lự -> tự'),
    (r'\blừ\s+(đó|1|2|3|4|5|6|7|8|9|10|ngày|năm|khi|lúc)', 'lừ -> từ'),
    (r'\bliếp\s+theo', 'liếp -> tiếp'),
    (r'\bnú[!\?]\s+', 'nú! -> nút'),
    (r'\bthưc\s+(hiện|hành|tế)', 'thưc -> thực'),
    (r'\btôc\s+độ', 'tôc -> tốc'),
    (r'\bchât\s+lượng', 'chât -> chất'),
    (r'\bkíp\s+thời', 'kíp -> kịp'),
    (r'\bbạn\s+bé\b', 'bạn bé -> bạn bè'),
    (r'\btim\s+(kiếm|hiểu|ra|thấy|được)', 'tim -> tìm'),
    (r'\bdưa\s+(ra|vào)', 'dưa -> đưa'),
    (r'\bdứ\s+liệu', 'dứ -> dữ'),
    (r'\bdừ\s+liệu', 'dừ -> dữ'),
    (r'\bdo\s+liệu', 'do -> dữ'),
    (r'\bthây\s+(rằng|các|là|được)', 'thây -> thấy'),
    (r'\bvê\s+(khói|mặt|phương diện|việc)', 'vê -> về'),
    (r'\bchỉ\s+tiết\b', 'chỉ tiết -> chi tiết'),
    (r'\bcơ\s+bàn\b', 'cơ bàn -> cơ bản'),
    (r'\bvăn\s+bàn\b', 'văn bàn -> văn bản'),
    (r'\bkịch\s+bàn\b', 'kịch bàn -> kịch bản'),
    (r'\bbàn\s+đồ\b', 'bàn đồ -> bản đồ'),
    (r'\bbàn\s+quyền\b', 'bàn quyền -> bản quyền'),
    (r'\bbàng\s+cách\b', 'bàng cách -> bằng cách'),
    (r'\bkhá\s+năng\b', 'khá năng -> khả năng'),
    (r'\bphán\s+ánh\b', 'phán ánh -> phản ánh'),
    (r'\bnguòn\b', 'nguòn -> nguồn'),
    (r'\bchuối\s+tư\s+duy\b', 'chuối tư duy -> chuỗi tư duy'),
    (r'\bquả\s+trình\b', 'quả trình -> quá trình'),
    (r'\bchủ\s+ý\b', 'chủ ý -> chú ý'),
    (r'\bsàn\s+phẩm\b', 'sàn phẩm -> sản phẩm'),
    (r'\bdầu\s+["\':]', 'dầu -> dấu'),
    (r'\bxắp\s+xếp\b', 'xắp xếp -> sắp xếp'),
    (r'\bxử\s+dụng\b', 'xử dụng -> sử dụng'),
    (r'\bsuất\s+sắc\b', 'suất sắc -> xuất sắc'),
    (r'\bgiải\s+quyết\s+bải\b', 'bải -> bài'),
    (r'\bđoạn\s+văn\s+giài\b', 'giài -> giải'),
    (r'\bngữ\s+cành\b', 'ngữ cành -> ngữ cảnh'),
    (r'\bbối\s+cành\b', 'bối cành -> bối cảnh'),
    (r'\bthông\s+tin\s+thém\b', 'thém -> thêm'),
    (r'\btôm\s+tắt\b', 'tôm tắt -> tóm tắt'),
    (r'\bđoan\s+văn\b', 'đoan văn -> đoạn văn'),
    (r'\bđoan\s+thơ\b', 'đoan thơ -> đoạn thơ'),
    (r'\bphương\s+trinh\b', 'phương trinh -> phương trình'),
    (r'\bchương\s+trinh\b', 'chương trinh -> chương trình'),
    (r'\btiêu\s+chi\b', 'tiêu chi -> tiêu chí'),
    (r'\bgiá\s+sử\b', 'giá sử -> giả sử'),
    (r'\btất\s+cà\b', 'tất cà -> tất cả'),
    (r'\bhàng\s+fỉ\b', 'hàng fỉ -> hàng tỉ'),
    (r'\bchẳng\s+chịt\b', 'chẳng chịt -> chằng chịt'),
    (r'\btin\s+hiệu\b', 'tin hiệu -> tín hiệu'),
    (r'\bnhiệt\s+độ\s+co\s+thể\b', 'co thể -> cơ thể'),
    (r'\bđiều\s+chình\b', 'điều chình -> điều chỉnh'),
    (r'\bhọc\s+lăng\s+cường\b', 'lăng cường -> tăng cường'),
    (r'\bhọc\s+có\s+giảm\s+sát\b', 'giảm sát -> giám sát'),
    (r'\bmô\s+phòng\b', 'mô phòng -> mô phỏng'),
    (r'\bthư\s+điện\s+từ\b', 'điện từ -> điện tử'),
    (r'\bmiến\s+phí\b', 'miến phí -> miễn phí'),
    (r'\btrứng\s+thường\b', 'trứng thường -> trúng thưởng'),
    (r'\bnguồn\s+gừi\b', 'nguồn gừi -> nguồn gửi'),
    (r'\bbước\s+tiền\b', 'bước tiền -> bước tiến'),
    (r'\bhòi\s+thời\s+tiết\b', 'hòi -> hỏi'),
    (r'\bsờ\s+thích\b', 'sờ thích -> sở thích'),
    (r'\bphù\s+hợp\s+nhật\b', 'nhật -> nhất'),
    (r'\btrước\s+đỏ\b', 'trước đỏ -> trước đó'),
    (r'\byếu\s+tổ\b', 'yếu tổ -> yếu tố'),
    (r'\bgial\s+điệu\b', 'gial điệu -> giai điệu'),
    (r'\btâm\s+bạng\b', 'tâm bạng -> tâm trạng'),
    (r'\bbài\s+hảt\b', 'bài hảt -> bài hát'),
    (r'\bcây\s+gia\s+phá\b', 'gia phá -> gia phả'),
    (r'\bchúng\s+ta\s+tháy\b', 'tháy -> thấy'),
    (r'\bxu\s+hưởng\b', 'xu hưởng -> xu hướng'),
    (r'\bgiới\s+tinh\b', 'giới tinh -> giới tính'),
    (r'\bchinh\s+những\b', 'chinh -> chính'),
    (r'\btử\s+vựng\b', 'tử vựng -> từ vựng'),
    (r'\bcài\s+thiện\b', 'cài thiện -> cải thiện'),
    (r'\bquý\s+đạo\b', 'quý đạo -> quỹ đạo'),
    (r'\bquỳ\s+đạo\b', 'quỳ đạo -> quỹ đạo'),
    (r'\bsao\s+chỗi\b', 'sao chỗi -> sao chổi'),
    (r'\bnhấn\s+tổ\s+hợp\s+phim\b', 'phim -> phím'),
    (r'\bbên\s+dười\b', 'dười -> dưới'),
    (r'\blì\s+độ\b', 'lì độ -> li độ'),
    (r'\bkhông\s+tiếng\s+ổn\b', 'ổn -> ồn'),
    (r'\bvào\s+ở\s+prompt\b', 'ở prompt -> ô prompt'),
    (r'\bkhám\s+phá\s+tri\s+thức\b', 'tri thức -> tri thức'),
    (r'\bthông\s+tin\s+điện\s+từ\b', 'điện từ -> điện tử'),
    (r'\bbảo\s+cáo\b', 'bảo cáo -> báo cáo'),
    (r'\bhiểu\s+sàu\b', 'hiểu sàu -> hiểu sâu'),
    (r'\bdầu\s+ấn\b', 'dầu ấn -> dấu ấn'),
    (r'\btrực\s+tuyển\b', 'trực tuyển -> trực tuyến'),
    (r'\bchúngta\b', 'chúngta -> chúng ta'),
    (r'\bđòng\s+hò\b', 'đòng hò -> đồng hồ'),
    (r'\btừ1\b', 'từ1 -> từ 1'),
    (r'\bmỗn\b', 'mỗn -> mỗi'),
    (r'\btưy\b', 'tưy -> tùy'),
    (r'\bluàn\b', 'luàn -> luận'),
    (r'\bnhan\s+dạng\b', 'nhan -> nhận'),
    (r'\bđòng\b', 'đòng -> đồng'),
    (r'\bgiài\b', 'giài -> giải'),
    (r'\bbải\b', 'bải -> bài'),
    (r'\bcành\b', 'cành -> cảnh'),
    (r'\bthém\b', 'thém -> thêm'),
    (r'\bđoan\b', 'đoan -> đoạn'),
    (r'\bhòi\b', 'hòi -> hỏi'),
    (r'\btôm\b', 'tôm -> tóm'),
    (r'\bmỏ\b', 'mỏ -> mô'),
    (r'\bmò\b', 'mò -> mô'),
    (r'\bsô\b', 'sô -> số'),
    (r'\blăn\b', 'lăn -> lần'),
    (r'\bgáp\b', 'gáp -> gấp'),
    (r'\blạp\b', 'lạp -> tạp/lập'),
    (r'\bcàn\b', 'càn -> cần'),
    (r'\bthào\b', 'thào -> thảo'),
    (r'\bgiái\b', 'giái -> giải'),
    (r'\bphù\s+định\b', 'phù -> phủ'),
    (r'\btừ\s+khoa\b', 'khoa -> khóa'),
    (r'\bmỗi\s+làn\b', 'làn -> lần'),
    (r'\bphai\s+đọc\b', 'phai -> phải'),
    (r'\bchâu\s+lục\b', 'châu lục'),
    (r'\bnghin\b', 'nghin -> nghìn'),
    (r'\bchíp\b', 'chíp -> chip'),
    (r'\bchịp\b', 'chịp -> chip')
]

plain_dir = ROOT / "scripts" / "lop11_plain"
files = sorted(plain_dir.glob("*.txt"))

findings = []

for f in files:
    if f.name == "all_lop11.txt":
        continue
    content = f.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    for l_idx, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("==="):
            continue
            
        # 1. Check regex patterns
        for pat, desc in CONTEXT_TYPO_PATTERNS:
            matches = re.findall(pat, line_clean, re.IGNORECASE)
            if matches:
                findings.append({
                    "file": f.name,
                    "line_no": l_idx + 1,
                    "type": "CONTEXT_TYPO",
                    "desc": desc,
                    "match": matches,
                    "text": line_clean
                })
                
        # 2. Check conjoined words (like wordNumber or lowercase glued with uppercase)
        conjoined = re.findall(r'([a-zA-Zà-ỹÀ-Ỹ]+[0-9]+|[0-9]+[a-zA-Zà-ỹÀ-Ỹ]+)', line_clean)
        for c in conjoined:
            if not re.match(r'^(x[1-9]|y[1-9]|w[1-9]|b[1-9]|h[1-6]|gpt[34]|v[0-9]|d[0-9]|3d|2d|4k|mp[34]|f[1-9]|000đ|1a|1b|1c|5a|5b|5c|cos2|ax|bx|cx|dx)$', c.lower()):
                findings.append({
                    "file": f.name,
                    "line_no": l_idx + 1,
                    "type": "CONJOINED",
                    "desc": f"conjoined: {c}",
                    "match": [c],
                    "text": line_clean
                })
                
        # 3. Check unknown words
        words = re.findall(r'[a-zA-Zà-ỹÀ-Ỹ_]+', line_clean)
        for w in words:
            wl = w.lower()
            if wl in valid_words or len(wl) <= 1:
                continue
            parts = wl.split('_')
            if all(p in valid_words for p in parts if p):
                continue
            # If word is capitalized and looks like foreign name
            if re.match(r'^[A-Z][a-z]+$', w) and wl in {'john', 'alan', 'turing', 'geoffrey', 'hinton', 'lecun', 'bengio', 'vaswani', 'attention', 'google', 'openai', 'anthropic', 'microsoft', 'meta'}:
                continue
            findings.append({
                "file": f.name,
                "line_no": l_idx + 1,
                "type": "UNKNOWN_WORD",
                "desc": f"unknown word: {w}",
                "match": [w],
                "text": line_clean
            })

print(f"Total scan findings in lop-11: {len(findings)}")

with open(ROOT / "scripts" / "lop11_scan_findings.json", "w", encoding="utf-8") as out:
    json.dump(findings, out, ensure_ascii=False, indent=2)

# Print summary
types = {}
for item in findings:
    t = item["desc"]
    types[t] = types.get(t, 0) + 1

for k, v in sorted(types.items(), key=lambda x: -x[1])[:30]:
    print(f"  {k}: {v}")
