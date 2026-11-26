import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons" / "lop-12"


def make_code_block(code: str) -> str:
    return (
        '\n                    <div class="code-block-wrapper">\n'
        '                        <div class="code-header"><span>Python / Code</span>'
        '<button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>\n'
        f'                        <pre><code class="language-python">{code}</code></pre>\n'
        '                    </div>\n                    '
    )


def make_figure_box(caption: str) -> str:
    return (
        '\n                    <figure class="lesson-figure-box">\n'
        '                        <div class="figure-placeholder">\n'
        '                            <span class="fig-badge">🖼️ Minh họa trong sách</span>\n'
        f'                            <figcaption class="figure-caption">{caption}</figcaption>\n'
        '                        </div>\n'
        '                    </figure>\n                    '
    )


BAI5_CODE_PART1 = make_code_block(
"""import logging
import sys

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

# --- Cấu hình chung ---
# Bật logging để xem quá trình xử lí của LlamaIndex
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# --- a) Tải thông tin sản phẩm và chương trình khuyến mãi từ các tệp khác nhau ---
print("Đang tải dữ liệu từ các tệp...")
# Tải tất cả các tệp từ thư mục hiện tại
documents = SimpleDirectoryReader("./").load_data()
print(f"Đã tải {len(documents)} tài liệu.")

# --- b) Tạo một chỉ mục dữ liệu bằng LlamaIndex ---
print("Đang tạo chỉ mục dữ liệu...")

# 1. Cấu hình mô hình nhúng (Embedding Model)
# Sử dụng mô hình nhúng của Hugging Face để tạo vector biểu diễn ngữ nghĩa cho văn bản.
# Mô hình "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" hỗ trợ đa ngôn ngữ.
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    # Sử dụng CPU để đảm bảo chạy được trên mọi máy tính không có GPU mạnh
    device="cpu"
)

# 2. Cấu hình mô hình ngôn ngữ lớn (LLM)
# Sử dụng Ollama với mô hình "llama2" chạy cục bộ.
# Đảm bảo bạn đã cài đặt Ollama và kéo mô hình llama2:
# - Tải Ollama từ https://ollama.com/
# - Chạy lệnh: ollama run llama2
Settings.llm = Ollama(model="llama2", request_timeout=360.0)  # Tăng timeout cho các câu trả lời dài

# 3. Xây dựng chỉ mục vector
# Chỉ mục này sẽ giúp chúng ta tìm kiếm thông tin nhanh chóng và hiệu quả.
index = VectorStoreIndex.from_documents(documents)
print("Đã tạo chỉ mục dữ liệu thành công.")"""
)

BAI5_CODE_PART2 = make_code_block(
"""# --- c) Xây dựng một Agent LangChain có khả năng sử dụng chỉ mục của LlamaIndex như một công cụ ---
print("Đang xây dựng Agent LangChain...")

# 1. Tạo Query Engine từ chỉ mục
# Query Engine giúp chúng ta hỏi các câu hỏi về chỉ mục.
query_engine = index.as_query_engine(similarity_top_k=3)  # Lấy 3 kết quả tương đồng nhất

# 2. Định nghĩa công cụ (Tool) cho Agent
# Công cụ này cho phép Agent sử dụng Query Engine để tìm kiếm thông tin sản phẩm và khuyến mãi.
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="thong_tin_san_pham_va_khuyen_mai",
        description=\"\"\"Sử dụng công cụ này khi người dùng hỏi về:
- Giá cả của sản phẩm (ví dụ: "Giá sữa Vinamilk là bao nhiêu?")
- Thông tin chi tiết về sản phẩm (ví dụ: "Bánh quy Kinh Đô Marie có gì đặc biệt?")
- Các chương trình khuyến mãi, ưu đãi (ví dụ: "Mì tôm Hảo Hảo có khuyến mãi gì không?", "Khuyến mãi tháng 6 là gì?").
Bạn PHẢI sử dụng công cụ này để truy xuất thông tin trước khi trả lời các câu hỏi liên quan đến sản phẩm và khuyến mãi.\"\"\"
    )
)

# 3. Khởi tạo Agent
# Chúng ta sẽ sử dụng ReActAgent của LlamaIndex vì nó tích hợp tốt với các công cụ của LlamaIndex
# và có khả năng suy luận để chọn công cụ phù hợp.
system_prompt_vi = \"\"\"Bạn là một trợ lí ảo thông minh, thân thiện và hữu ích, chuyên cung cấp thông tin về sản phẩm và các chương trình khuyến mãi.
Nhiệm vụ của bạn là trả lời các câu hỏi của người dùng một cách chính xác và đầy đủ, dựa trên các thông tin bạn có.
Bạn có khả năng sử dụng các CÔNG CỤ (tools) để tìm kiếm thông tin.
Khi người dùng hỏi về sản phẩm, giá cả, hoặc các chương trình khuyến mãi, bạn PHẢI SỬ DỤNG công cụ 'thong_tin_san_pham_va_khuyen_mai' để lấy dữ liệu.
Luôn trả lời bằng TIẾNG VIỆT.\"\"\"

agent = ReActAgent.from_tools(
    tools=[query_engine_tool],
    llm=Settings.llm,
    verbose=True,
    system_prompt=system_prompt_vi  # Thêm system prompt tiếng Việt
)
print("Đã xây dựng Agent LangChain thành công.")

# --- Phần tương tác với người dùng ---
print("\\n--- Sẵn sàng trả lời câu hỏi của bạn! ---")
print("Bạn có thể hỏi về thông tin sản phẩm, giá cả, hoặc các chương trình khuyến mãi.")
print("Gõ 'thoát' để thoát.")

while True:
    question = input("\\nBạn hỏi: ")
    if question.lower() == 'thoát':
        print("Cảm ơn bạn đã sử dụng!")
        break
    try:
        response = agent.chat(question)
        print(f"Agent trả lời: {response}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}. Vui lòng thử lại hoặc kiểm tra lại cài đặt Ollama.")"""
)

BAI11_CODE_BLOCK1 = make_code_block(
"""import pandas as pd  # Nhập thư viện pandas để làm việc với dữ liệu dạng bảng

csv_txt = \"\"\"hours,score
2,4
3,5
4,6
5,7
6,8
7,9
8,10\"\"\"

open("study_data.csv", "w").write(csv_txt)  # Tạo và ghi nội dung vào file study_data.csv"""
)

BAI11_CODE_BLOCK2 = make_code_block(
"""import matplotlib.pyplot as plt  # Nhập thư viện matplotlib để vẽ biểu đồ
import pandas as pd  # Nhập thư viện pandas để làm việc với dữ liệu dạng bảng

data = pd.read_csv("study_data.csv")  # Đọc dữ liệu từ file CSV vào DataFrame
X = data["hours"].values  # Lấy cột "hours" (số giờ học) làm dữ liệu đầu vào X (dạng mảng numpy)
y = data["score"].values  # Lấy cột "score" (điểm thi) làm dữ liệu đầu ra y (dạng mảng numpy)

plt.scatter(X, y, s=60)  # Vẽ biểu đồ phân tán (scatter plot) với X (trục hoành) và y (trục tung), s=60 là kích thước điểm
plt.xlabel("Số giờ học")  # Đặt tên cho trục hoành
plt.ylabel("Điểm thi")  # Đặt tên cho trục tung
plt.title("Phân bố dữ liệu")
plt.show()  # Hiển thị biểu đồ"""
)

BAI11_CODE_BLOCK3 = make_code_block(
"""import numpy as np

def gradient_descent(X, y, lr=0.01, epochs=1_000, verbose=False):
    \"\"\"Trả về (w, b, loss_hist). X, y đều là 1-D numpy array.\"\"\"
    w, b = 0.0, 0.0  # Khởi tạo ban đầu cho w và b
    n = len(X)
    loss_hist = []  # Lưu lại giá trị mất mát sau mỗi lần học

    for epoch in range(epochs):
        y_pred = w * X + b  # AI đưa ra dự đoán điểm thi
        error = y_pred - y  # Tính sự sai lệch giữa dự đoán và thực tế
        loss = (error ** 2).mean()  # Tính hàm mất mát (MSE)
        loss_hist.append(loss)

        # Tính toán hướng cần điều chỉnh (Gradient) để giảm mất mát
        w_grad = (2 / n) * np.dot(X, error)
        b_grad = (2 / n) * error.sum()

        # Cập nhật tham số w và b để giảm hàm mất mát
        w -= lr * w_grad
        b -= lr * b_grad

        if verbose and epoch % 100 == 0:  # In ra để xem tiến trình học của AI
            print(f"epoch {epoch:>4}: loss = {loss:.4f}")

    return w, b, loss_hist"""
)

BAI11_CODE_BLOCK4 = make_code_block(
"""w, b, loss_hist = gradient_descent(X, y, lr=0.01, epochs=1_000, verbose=True)
print(f"Đường hồi quy tối ưu: y = {w:.2f}*x + {b:.2f}")"""
)

BAI11_CODE_BLOCK5 = make_code_block(
"""plt.scatter(X, y, s=60, label="Dữ liệu thực")
plt.plot(X, w * X + b, color="red", label="Đường hồi quy")  # Vẽ đường dự đoán của AI
plt.xlabel("Số giờ học")
plt.ylabel("Điểm thi")
plt.title("Dự đoán điểm thi theo số giờ học")
plt.legend()
plt.show()"""
)

GLOSSARY_CLEAN_BODY = """
<p class="lesson-p"><strong>BẢNG GIẢI THÍCH THUẬT NGỮ</strong></p>
<p class="lesson-p"><strong>AI Agent (Tác nhân thông minh):</strong> Hệ thống trí tuệ nhân tạo có thể quan sát, xử lí thông tin, ra quyết định và hành động để đạt mục tiêu.</p>
<p class="lesson-p"><strong>AI tạo sinh (Generative AI):</strong> Loại trí tuệ nhân tạo có khả năng tạo ra nội dung mới (văn bản, hình ảnh, âm thanh, video...) dựa trên dữ liệu đã được học.</p>
<p class="lesson-p"><strong>API (Application Programming Interface):</strong> Bộ quy tắc cho phép các lập trình viên có thể sử dụng để gửi yêu cầu và nhận lại dữ liệu từ một hệ thống khác. API thường xuất hiện dưới dạng URL, mã hàm hoặc thư viện,...</p>
<p class="lesson-p"><strong>Bias (Thiên vị):</strong> Xu hướng mô hình học thiên lệch do dữ liệu không cân bằng, có thể dẫn đến kết quả không công bằng.</p>
<p class="lesson-p"><strong>Cửa sổ ngữ cảnh (Context Window):</strong> Lượng thông tin (ví dụ: số từ, token) mà một mô hình AI có thể "ghi nhớ" hoặc xem xét tại một thời điểm khi xử lí prompt và tạo phản hồi. Giới hạn này ảnh hưởng đến khả năng hiểu và duy trì mạch lạc của AI trong các cuộc hội thoại dài.</p>
<p class="lesson-p"><strong>Định dạng JSON (JavaScript Object Notation):</strong> Cách thức chuẩn để tổ chức và trao đổi dữ liệu dưới dạng văn bản.</p>
<p class="lesson-p"><strong>Framework (Khung làm việc):</strong> Bộ công cụ và quy tắc sẵn có giúp lập trình viên xây dựng phần mềm nhanh và hiệu quả.</p>
<p class="lesson-p"><strong>Index (Chỉ mục):</strong> Cách tổ chức và lưu trữ dữ liệu để có thể tìm kiếm nhanh chóng và hiệu quả.</p>
<p class="lesson-p"><strong>Mô hình Embedding:</strong> Mô hình AI chuyên dùng để chuyển đổi dữ liệu (văn bản, hình ảnh,...) thành các vector số (một chuỗi số). Các vector này mã hoá ý nghĩa của dữ liệu, giúp AI dễ dàng so sánh, tìm kiếm và hiểu mối quan hệ giữa các dữ liệu khác nhau.</p>
<p class="lesson-p"><strong>Overfitting (Quá khớp):</strong> Xảy ra khi mô hình học quá kĩ dữ liệu cũ, dẫn đến kém hiệu quả khi gặp dữ liệu mới.</p>
<p class="lesson-p"><strong>Prompt:</strong> Lệnh hoặc câu hỏi đầu vào mà người dùng cung cấp cho một mô hình AI để hướng dẫn nó tạo ra nội dung mong muốn.</p>
<p class="lesson-p"><strong>Tác vụ (Task):</strong> Một công việc cụ thể, có mục tiêu rõ ràng mà một hệ thống, chương trình, hoặc mô hình AI được thiết kế để thực hiện. Một tác vụ thường bao gồm các yêu cầu đầu vào nhất định và mong đợi một kết quả đầu ra cụ thể.</p>
<p class="lesson-p"><strong>Thư viện nguồn mở:</strong> Thư viện lập trình có mã nguồn công khai, miễn phí sử dụng và tuỳ chỉnh.</p>
<p class="lesson-p"><strong>Top_k (trong cấu hình LLM):</strong> Số lượng từ/token có xác suất cao nhất mà mô hình LLM sẽ xem xét khi chọn từ tiếp theo để tạo ra câu trả lời.</p>
<p class="lesson-p"><strong>Vector Store Index (Chỉ mục kho lưu trữ vector):</strong> Cấu trúc dữ liệu lưu trữ và tổ chức các vector nhúng (embeddings) để có thể tìm kiếm nhanh chóng các vector tương tự (có ý nghĩa gần giống nhau).</p>"""


REPLACEMENTS = {
    "bia-sach": [
        ("VŨ TRUNG CHÍNH- NGUYỄN QUANG ĐỨC- NGUYỄN CHÍ THANH", "VŨ TRUNG CHÍNH - NGUYỄN QUANG ĐỨC - NGUYỄN CHÍ THANH"),
        ("NGUYỄN THỊ VẬN ANH - ĐỖ ĐỨC LÂN", "NGUYỄN THỊ VÂN ANH - ĐỖ ĐỨC LÂN"),
    ],
    "bia-lot": [
        ("LÊ ANH VINH. (ĐÓNG CHÚ BIÊN)</p>", "LÊ ANH VINH (ĐỒNG CHỦ BIÊN)</p>"),
        ("NGUYỄN THỊ VÁN ANH - ĐÕ ĐỨC LÀN - LÊ QUANG QUẢN", "NGUYỄN THỊ VÂN ANH - ĐỖ ĐỨC LÂN - LÊ QUANG QUÂN"),
        ("<p class=\"lesson-p\"></p>\n", ""),
    ],
    "huong-dan-su-dung-sach": [
        ("<p class=\"lesson-p\">VẠN DỤNG</p>", "<p class=\"lesson-p\">VẬN DỤNG</p>"),
    ],
    "loi-noi-dau": [
        ("Các em học sinh thân mền!</p>", "Các em học sinh thân mến!</p>"),
        ("về tranh, Trí tuệ nhân tạo (Al) đang thay đổi", "vẽ tranh, Trí tuệ nhân tạo (AI) đang thay đổi"),
        ("tiếp cận kho dữ liệu không</p>", "tiếp cận kho dữ liệu khổng</p>"),
        ("<p class=\"lesson-p\">CÁC TÁC GIÁ</p>", "<p class=\"lesson-p\">CÁC TÁC GIẢ</p>"),
    ],
    "muc-luc": [
        ("CHỦ ĐẾ 1. AI AGENTS - HƯỚNG TỚI AI TỰ HOẠT ĐỘNG", "CHỦ ĐỀ 1. AI AGENTS - HƯỚNG TỚI AI TỰ HOẠT ĐỘNG"),
        ("Bài 2 Cấu trúc AI Agent đon giản", "Bài 2 Cấu trúc AI Agent đơn giản"),
        ("CHỦ ĐỀ 2. RAG VÀ CÔNG CỤ LÀM VIỆC VỚI LM</p>", "CHỦ ĐỀ 2. RAG VÀ CÔNG CỤ LÀM VIỆC VỚI LLM</p>"),
        ("Bài 4 Thu viện nguồn mở LLM", "Bài 4 Thư viện nguồn mở LLM"),
        ("Bài 5 Khai thác thư viện nguồn mở LIM", "Bài 5 Khai thác thư viện nguồn mở LLM"),
        ("Bài 7 AI mờ ra cơ hội và thách thức", "Bài 7 AI mở ra cơ hội và thách thức"),
        ("Bài 8 Quyền con người trong kỉ nguyên A</p>", "Bài 8 Quyền con người trong kỉ nguyên AI</p>"),
        ("Bài 11 Tối vu hóa mô hình", "Bài 11 Tối ưu hóa mô hình"),
        ("CHỦ ĐỂ 5. DỰ ÁN AI AGENT", "CHỦ ĐỀ 5. DỰ ÁN AI AGENT"),
        ("Bài 13 Xây dụng sản phẩm", "Bài 13 Xây dựng sản phẩm"),
        ("\n<p class=\"lesson-p\">CHỦ ĐỀ 1. AI AGENTS -\n\nHƯỚNG TỚI AI TỰ HOẠT ĐỘNG</p>\n<p class=\"lesson-p\">Sir</p>\n<p class=\"lesson-p\">Al nini</p>", ""),
    ],
    "bai-1-gioi-thieu-ve-ai-agents": [
        ("Tùng cảm thây mệt mỏi", "Tùng cảm thấy mệt mỏi"),
        ("từng câu hỏi cụ thế. Trợ lí ảo đó", "từng câu hỏi cụ thể. Trợ lí ảo đó"),
        ("chính là một Agent.\n\n6</p>", "chính là một Agent.</p>"),
        (
"""<p class="lesson-p">O</p>
<p class="lesson-p">LLMs</p>
<p class="lesson-p">Chatbot</p>
<p class="lesson-p">AI Agents</p>
<p class="lesson-p">Mô hình ngôn ngô lên có khô rông sinh</p>
<p class="lesson-p">Hệ thống tương tác Hội thoại Chatbot</p>
<p class="lesson-p">Hệ thống AI tự động có khế nắng thực</p>
<p class="lesson-p">và hiểu văn bản dựa trên dữ liệu huấn</p>
<p class="lesson-p">tuyện không 1</p>
<p class="lesson-p">Hệ thống giao tiếp trực tiếp với người dùng</p>
<p class="lesson-p">Hiện nhiệm vụ phút tạp và tương tác với</p>
<p class="lesson-p">mội trường</p>
<ul class="lesson-bullet-list">
<li></li>
</ul>
<p class="lesson-p">Sinh và hiểu văn bản tự nhiên</p>
<ul class="lesson-bullet-list">
<li>Thực hiện nhiệm vụ tự động</li>
</ul>
<p class="lesson-p">Xử lí đe ngôn ngô</p>
<ul class="lesson-bullet-list">
<li>Ra quyết định thông minh</li>
</ul>
<p class="lesson-p">Trà lới câu nội mô</p>
<ul class="lesson-bullet-list">
<li>Tes lori eDu Ach thường gặp</li>
<li>Tương tác với hệ thống khác</li>
</ul>
<p class="lesson-p">Dịch thuật và tóm tắt</p>
<ul class="lesson-bullet-list">
<li>Hỏ trợ khách rông cơ băn</li>
<li>Học nói từ kính nghiệm</li>
<li>Giao điện thên thiện</li>
</ul>
<p class="lesson-p">Sảng tạo nội dụng</p>
<ul class="lesson-bullet-list">
<li>Tích hơp đa nên táng</li>
<li>Sử dung công cu bên ngoài</li>
</ul>
<p class="lesson-p">Phân tích ngữ nghĩa</p>
<ul class="lesson-bullet-list">
<li>Xử lí quy trình phức tạp</li>
</ul>""",
            ""
        ),
        ("vòng lập suy nghĩ-hành động.</p>", "vòng lặp suy nghĩ-hành động.</p>"),
        ("<p class=\"lesson-p\">cụ thế.</p>", "<p class=\"lesson-p\">cụ thể.</p>"),
        (
            "<p class=\"lesson-p\">2. Vòng lặp hoạt động và các thành phần chính của AI Agents a) Vòng lập hoạt động</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Vòng lặp hoạt động và các thành phần chính của AI Agents</h3>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Vòng lặp hoạt động</h4>"
        ),
        ("vòng lặp liên tục, phản án</p>", "vòng lặp liên tục, phản ánh</p>"),
        (
"""<p class="lesson-p">Nhận mục tiêu</p>
<p class="lesson-p">AI Agents được cung cấp nhiệm vụ hoặc mục tiêu cần thực hiện</p>
<p class="lesson-p">LLM - Mô-đun Lập luận/Lập kế hoạch</p>
<p class="lesson-p">Sử dụng mô hình ngôn ngữ lớn để phân tích, suy nghĩ và đưa ra quyết</p>
<p class="lesson-p">định</p>
<p class="lesson-p">Chọn công cụ</p>
<p class="lesson-p">Quyết định công cụ hoặc phương pháp phù hợp nhất để thực hiện nhiệm vụ</p>
<p class="lesson-p">Thực thi công cụ</p>
<p class="lesson-p">Sử dụng công cụ đã chọn để thực thi hành động cụ thể</p>
<p class="lesson-p">Quan sát kết quả</p>
<p class="lesson-p">Đánh giá và phân tích kết quả từ việc thực thi công cụ</p>
<p class="lesson-p">Cập nhật bộ nhớ</p>
<p class="lesson-p">Lưu trữ kinh nghiệm và kiến thức mới để cái thiện hiệu suất tương lai</p>
<p class="lesson-p">auay lai bước 2 để tiếp tực chu trinh</p>""",
            ""
        ),
        (
"""<p class="lesson-p">AI AGENT</p>
<p class="lesson-p">Lập kế hoạch</p>
<p class="lesson-p">Lập luận - GENAI</p>
<p class="lesson-p">Bộ nhớ Sử dụng công cụ</p>""",
            ""
        ),
        ("tiếp tục lập lại.</li>", "tiếp tục lặp lại.</li>"),
        ("Mô-đun Lập kể hoạch,", "Mô-đun Lập kế hoạch,"),
        (
            "<p class=\"lesson-p\">3. Tiềm năng ứng dụng và thách thức của AI Agents a) Tiêm năng ứng dụng Khả năng tự chủ và tương tác với môi trường bên ngoài mang lại cho AI Agents tiềm năng cách mạng hoá nhiều lĩnh vực:</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">3.</span> Tiềm năng ứng dụng và thách thức của AI Agents</h3>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Tiềm năng ứng dụng</h4>\n<p class=\"lesson-p\">Khả năng tự chủ và tương tác với môi trường bên ngoài mang lại cho AI Agents tiềm năng cách mạng hoá nhiều lĩnh vực:</p>"
        ),
        ("đặt một chuyên du lịch trọn gói,", "đặt một chuyến du lịch trọn gói,"),
        (
            "tìm kiếm địa điểm tham quan va nha hang phú hợp với sở thích cá nhân hay xứ li các công việc trong doanh nghiệp như: duyệt tài liệu, tông hợp báo cáo tài chính từ nhiêu nguôn.",
            "tìm kiếm địa điểm tham quan và nhà hàng phù hợp với sở thích cá nhân hay xử lí các công việc trong doanh nghiệp như: duyệt tài liệu, tổng hợp báo cáo tài chính từ nhiều nguồn."
        ),
        ("để các nhà khoa học xem xét</p>", "để các nhà khoa học xem xét.</p>"),
        (
            "biện pháp khắc phục sự cố, giảm thiểu Hình 1.4. Kịch bản ứng dụng AI Age trong thực tế thời gian ngừng hoạt động.</p>",
            "biện pháp khắc phục sự cố, giảm thiểu thời gian ngừng hoạt động.</p>" + make_figure_box("Hình 1.4. Kịch bản ứng dụng AI Agent trong thực tế")
        ),
        ("nhiều thách thức đáng kế:</p>", "nhiều thách thức đáng kể:</p>"),
        ("có thể dẫn đến hậu quả nghiêm trọng</p>", "có thể dẫn đến hậu quả nghiêm trọng.</p>"),
        ("Làm thế nào đế đảm bảo Agent", "Làm thế nào để đảm bảo Agent"),
        ("giám sát và dừng khấn cấp là cần thiết.", "giám sát và dừng khẩn cấp là cần thiết."),
        ("+ Hiệu quả và tộc độ:", "+ Hiệu quả và tốc độ:"),
        ("không được đê cập trong huân luyện.</p>", "không được đề cập trong huấn luyện.</p>"),
        ("+ Quyên riêng tư và bảo mật dữ liệu:", "+ Quyền riêng tư và bảo mật dữ liệu:"),
        ("+ Ánh hưởng đến việc làm:", "+ Ảnh hưởng đến việc làm:"),
        ("có thể làm thay đối cấu trúc thị trường", "có thể làm thay đổi cấu trúc thị trường"),
        (
            "<p class=\"lesson-p\">LUYÊN TẬP</p>",
            "</div></section>\n\n            <section class=\"lesson-card exercise-section\" id=\"sec-luyện-tập\">\n                <div class=\"section-badge-header\">\n                    <span class=\"sec-icon\">✏️</span>\n                    <h2 class=\"section-title\">LUYỆN TẬP</h2>\n                </div>\n                <div class=\"section-body\">"
        ),
        ("D. Mô-đun Lập kê hoạch.</p>", "D. Mô-đun Lập kế hoạch.</p>"),
        (
            "3. Giai thích tại sao việc kiểm soát và đảm bảo an toàn là một thách thức kĩ thuật quan trong khi phát triển AI Agents.",
            "3. Giải thích tại sao việc kiểm soát và đảm bảo an toàn là một thách thức kĩ thuật quan trọng khi phát triển AI Agents."
        ),
        ("Em hãy hinh dụng một dự án nghiên cứu khoa học", "Em hãy hình dung một dự án nghiên cứu khoa học"),
        ("một hệ sinh thái cụ thế.", "một hệ sinh thái cụ thể."),
        (
            "những nhiệm vụ cụ thế nào? Hãy mô tả một kịch bản mà Agent sẽ tự động thực hiện nhiêu bước để hỗ trợ nghiên cứu của em. Đồng thời, hãy chỉ ra một thách thức tiêm năng",
            "những nhiệm vụ cụ thể nào? Hãy mô tả một kịch bản mà Agent sẽ tự động thực hiện nhiều bước để hỗ trợ nghiên cứu của em. Đồng thời, hãy chỉ ra một thách thức tiềm năng"
        ),
    ],
    "bai-2-cau-truc-ai-agent-don-gian": [
        ("kháchh", "khách"),
        ("lưu trữ trong số</li>", "lưu trữ trong sổ</li>"),
        ("Sữa tươi organic nào tôt nhất hiện nay?", "Sữa tươi organic nào tốt nhất hiện nay?"),
        (
            "<p class=\"lesson-p\">1. Xây dựng AI Agent sử dụng công cụ no-code/low-code Việc xây dựng AI Agent hay các ứng dụng LLM phức tạp bằng LangChain đời, Kĩ năng lập trình Python. Điều này có thể gây khó khăn cho những ai chưa thà thạo viết mã. Sự ra đời của các công cụ no-code/low-code (không mã lệnh/ít lệnh) trong lĩnh vực AI sẽ giúp họ dễ dàng hiểu các khái niệm, thử nghiệm và trì</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Xây dựng AI Agent sử dụng công cụ no-code/low-code</h3>\n<p class=\"lesson-p\">Việc xây dựng AI Agent hay các ứng dụng LLM phức tạp bằng LangChain đòi hỏi kĩ năng lập trình Python. Điều này có thể gây khó khăn cho những ai chưa thành thạo viết mã. Sự ra đời của các công cụ no-code/low-code (không mã lệnh/ít mã lệnh) trong lĩnh vực AI sẽ giúp họ dễ dàng hiểu các khái niệm, thử nghiệm và triển</p>"
        ),
        (
"""<p class="lesson-p">No-code AI Agent flow</p>
<p class="lesson-p">AI Agent</p>
<p class="lesson-p">Input</p>
<p class="lesson-p"></p>""",
            ""
        ),
        ("Hình 2.1. minh họa xây dựng Agent", "Hình 2.1. Minh hoạ xây dựng Agent"),
        (
            "<p class=\"lesson-p\">2. MindStudio: Nền tảng trực quan cho AI Agent Hãy cùng khám phá cách một nền tảng no-code/low-code như MindStudio (một nền tảng tiêu biểu cho phép xây dựng ứng dụng AI tuy chỉnh mà không cần viết mã) hoạt động để tạo ra một AI Agent đơn giản.</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> MindStudio: Nền tảng trực quan cho AI Agent</h3>\n<p class=\"lesson-p\">Hãy cùng khám phá cách một nền tảng no-code/low-code như MindStudio (một nền tảng tiêu biểu cho phép xây dựng ứng dụng AI tuỳ chỉnh mà không cần viết mã) hoạt động để tạo ra một AI Agent đơn giản.</p>"
        ),
        (
"""<p class="lesson-p">800 *) Ví dụ Demo Sách - :</p>
<p class="lesson-p">Preview & Publish</p>
<ul class="lesson-bullet-list">
<li>M Vi do Demo Sách Automations System Prompt Model Settings Evaluations Profiler</li>
</ul>
<p class="lesson-p"></p>
<ul class="lesson-bullet-list">
<li></li>
</ul>
<p class="lesson-p">v E Data Sources</p>
<p class="lesson-p">Functions</p>
<ul class="lesson-bullet-list">
<li>l User Inputs</li>
</ul>
<p class="lesson-p">Workflows</p>
<p class="lesson-p">B Main.flow</p>
<p class="lesson-p">Overview</p>
<p class="lesson-p">→</p>
<p class="lesson-p">X Generator Agent Le Edit Overview</p>
<p class="lesson-p">Bảng điều khiến bên trái</p>
<p class="lesson-p">Bảng thiết kế</p>
<p class="lesson-p">Khu vực làm</p>
<p class="lesson-p">Khu vực</p>
<p class="lesson-p">(Canvas)</p>
<p class="lesson-p">việc chính (Workspace)</p>
<p class="lesson-p">cài đặt (Configuration)</p>
<p class="lesson-p">(Explorer)</p>""",
            ""
        ),
        ("Bảng điều khiến bên trái (Explorer):", "Bảng điều khiển bên trái (Explorer):"),
        ("giúp em dễ dàng tuy biến chức năng", "giúp em dễ dàng tuỳ biến chức năng"),
        ("Xây dựng luông xử lí trong bảng thiết kế", "Xây dựng luồng xử lí trong bảng thiết kế"),
        (
"""<p class="lesson-p">Start End</p>
<p class="lesson-p">Nút (+) để thêm</p>
<p class="lesson-p">Khối bắt đầu (Start block)</p>
<p class="lesson-p">các khối chức</p>
<p class="lesson-p">Khối kết thúc</p>
<p class="lesson-p">năng khác</p>
<p class="lesson-p">(End block)</p>""",
            ""
        ),
        ("Nháy chuột vào nút -. hoặc kéo thả", "Nháy chuột vào nút (+) hoặc kéo thả"),
        (
            "<p class=\"lesson-p\">điều khiển bên trái vào.\n\nb) Trong bảng thiết kế em có thể</p>",
            "<p class=\"lesson-p\">điều khiển bên trái vào.</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Trong bảng thiết kế em có thể</h4>"
        ),
        ("(Sticky notes) để thêm bình luận, giú</li>", "(Sticky notes) để thêm bình luận, giúp</li>"),
        (
            "<p class=\"lesson-p\">em nhớ các chi tiết quan trọng.\n\nc) Các cài đặt quan trọng cho Agent</p>",
            "<p class=\"lesson-p\">em nhớ các chi tiết quan trọng.</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Các cài đặt quan trọng cho Agent</h4>"
        ),
        ("<p class=\"lesson-p\">Automations System Prompt Model Settings Evaluations Profiler</p>", ""),
        ("(ví dụ Bạn là trợ lí tư vấn", "(ví dụ: Bạn là trợ lí tư vấn"),
        (
"""<p class="lesson-p">Choose a Block</p>
<p class="lesson-p">Generate</p>
<p class="lesson-p">Generate Text Interact with AI on behalf of user</p>
<p class="lesson-p">Generate Image Generate an image using AI</p>
<p class="lesson-p">Generate Video Generate a video using AI</p>
<p class="lesson-p">Generate Chart</p>
<p class="lesson-p">Generate Asset Generator HTML, images, or PDFS</p>
<p class="lesson-p">Analyze Image Analyze an image using A</p>
<p class="lesson-p">Generate a chart from data</p>
<p class="lesson-p">Create Podcast: Two-host podcast about a topic</p>
<p class="lesson-p">Text to Speech</p>
<p class="lesson-p">Generate speech using AI</p>
<p class="lesson-p">Transcribe Audio AI Speech-to-Text</p>
<p class="lesson-p">Get Data</p>
<p class="lesson-p">Scrape URL Scrape a web page</p>
<p class="lesson-p">User Input Collect data from the user</p>
<p class="lesson-p">User Context</p>
<p class="lesson-p">Dynamically gather information</p>
<p class="lesson-p">Query Data Source Create variable from a Data Source</p>
<p class="lesson-p">Extract Text from File Extract text content from a file URL</p>
<p class="lesson-p">HTTP Request Make an HTTP request</p>
<p class="lesson-p">Track Website Changes Detect changes to a website</p>
<p class="lesson-p">Analyze CSV Analyze CSV with code</p>
<p class="lesson-p">Deep Research Sourced information from the web</p>
<p class="lesson-p">OCR Image Extract text from an image</p>
<p class="lesson-p">Extract from URL Scrape and extract from a site</p>
<p class="lesson-p">Flow</p>
<p class="lesson-p">Checkpoint Prompt far. human review Y</p>
<p class="lesson-p">Logic Dynamically choose the next step</p>
<p class="lesson-p">Display Content Display text or media</p>
<p class="lesson-p">Menu Present branching options D</p>
<p class="lesson-p">Run Workflow Run another workflow</p>
<p class="lesson-p">Run Function Run JavaScript or Python</p>""",
            ""
        ),
        (
            "các khối đề lặp lại một hành động. Ví dụ: Nếu khách hàng hỏi về giá, chuyển đến khối Get Data. Nếu không, chuyến đến khối Generate để trả lời chung.",
            "các khối để lặp lại một hành động. Ví dụ: Nếu khách hàng hỏi về giá, chuyển đến khối Get Data. Nếu không, chuyển đến khối Generate để trả lời chung."
        ),
        ("<li>Email (Gir thư điện tú). Khối công cụ này cho phép Agent gửi the điện tú tý</li>", "<li>Email (Gửi thư điện tử): Khối công cụ này cho phép Agent gửi thư điện tử tự</li>"),
        ("động. Ví dụ. Gửi thư điện tử cảm ơn", "động. Ví dụ: Gửi thư điện tử cảm ơn"),
        ("- Text Transform (Chuyên đói văn bản): Các khối giúp xử lí, chinh sữa văn bản", "- Text Transform (Chuyển đổi văn bản): Các khối giúp xử lí, chỉnh sửa văn bản"),
        ("(ví dụ: tôm tất, trích xuất tháng sn. thay thể tùy Ví dụ: Tóm tắt kết quả tim hiền web trước khi dua cho Lil.", "(ví dụ: tóm tắt, trích xuất thông tin, thay thế từ). Ví dụ: Tóm tắt kết quả tìm kiếm web trước khi đưa cho LLM."),
        ("<li>Other Block (Các khối khác): Ngoài ra còn có nhiều khối khác phục vụ các.</li>", "<li>Other Block (Các khối khác): Ngoài ra còn có nhiều khối khác phục vụ các</li>"),
        ("<p class=\"lesson-p\">muc đich chuyên biệt hon niu.", "<p class=\"lesson-p\">mục đích chuyên biệt hơn như:"),
        ("* SMS: Để gửi tín nhắn SMS.", "+ SMS: Để gửi tin nhắn SMS."),
        ("* Extemal Automation. Để kết nối với các hệ thống tự động hoa khán.", "+ External Automation: Để kết nối với các hệ thống tự động hoá khác."),
        ("Bắng cách kéo thả và kết nỗi các khối này trên canvas, em có thể tạo ra các Ai Agent", "Bằng cách kéo thả và kết nối các khối này trên canvas, em có thể tạo ra các AI Agent"),
        ("<li>Giao điện: Bảng thiết kể (Carvas) trực quan, kéo-thả.", "<li>Giao diện: Bảng thiết kế (Canvas) trực quan, kéo-thả."),
        ("<li>Generative AI Block Tương tác với Generative AI.</li>", "<li>Generative AI Block: Tương tác với Generative AI,</li>"),
        ("<p class=\"lesson-p\">đạt prompt.</p>", "<p class=\"lesson-p\">đặt prompt.</p>"),
        ("<li>Tool Block: Kết nỗi với công cụ bên ngoài (Em kiếm, tinh", "<li>Tool Block: Kết nối với công cụ bên ngoài (tìm kiếm, tính"),
        ("<p class=\"lesson-p\">toàn, thu điện tử).", "<p class=\"lesson-p\">toán, thư điện tử)."),
        ("cửa hàng tạp hoa của gia đình bạn An.", "cửa hàng tạp hoá của gia đình bạn An."),
        (
            "<p class=\"lesson-p\">(Hướng dẫn sau đây sử dụng phần mềm Mind Studio.) a) Tiếp nhận câu hỏi tử khách hàng Bước 1. Truy cập trang web MindStudio tại địa chi https://www.mindstudio.ai vä đặng nhập vào tài khoản của em, sau đó chọn Build New Agent Bước 2. Nháy chuột vào nút (E (giữa Start và End) rồi chọn User Input đễ thêm User Input (đầu vào) như Hình 2.6.</p>\n<p class=\"lesson-p\">Start End</p>",
            "<p class=\"lesson-p\">(Hướng dẫn sau đây sử dụng phần mềm MindStudio.)</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Tiếp nhận câu hỏi từ khách hàng</h4>\n<p class=\"lesson-p\">Bước 1. Truy cập trang web MindStudio tại địa chỉ https://www.mindstudio.ai và đăng nhập vào tài khoản của em, sau đó chọn Build New Agent.</p>\n<p class=\"lesson-p\">Bước 2. Nháy chuột vào nút (+) (giữa Start và End) rồi chọn User Input để thêm User Input (đầu vào) như Hình 2.6.</p>"
        ),
        ("Cửa số xuất hiện như Hình 2.7.", "Cửa sổ xuất hiện như Hình 2.7."),
        ("cau_hoi _khach _hang", "cau_hoi_khach_hang"),
        ("cau_hoi _khach_hang", "cau_hoi_khach_hang"),
        ("{{cau_hoi_khach_hang }}", "{{cau_hoi_khach_hang}}"),
        ("{{cau_hoi_khach_hang)}", "{{cau_hoi_khach_hang}}"),
        (
"""<p class="lesson-p">Type</p>
<p class="lesson-p">Long Tex!</p>
<p class="lesson-p">cau hol khach hang</p>
<p class="lesson-p">CourtIon</p>
<p class="lesson-p">Bạn muốn hói gì về sản phẩm?</p>
<p class="lesson-p">Bạn muốn hỏi gì về sản phẩm?</p>
<p class="lesson-p">Nhập câu hỏi của bạn ở dây</p>
<p class="lesson-p">Hetp Text (Optianal)</p>""",
            ""
        ),
        (
"""<p class="lesson-p">Advanced</p>
<p class="lesson-p">Test Value (Optional)</p>
<p class="lesson-p">Sữa tươi organic nào tốt nhất hiện nay?</p>
<p class="lesson-p">Test values make it easy to pre-fill responses when previewing drafts.</p>""",
            ""
        ),
        ("Sử dụng công cụ đề truy xuất thông tin từ câu hỏi", "Sử dụng công cụ để truy xuất thông tin từ câu hỏi"),
        (
            "- Chọn nút ở giữa User Input và End, sau đó chọn View All Blocks Tìm mục Google và chọn Search Google để đưa vào Canvas. Kết quả nh</p>",
            "- Chọn nút (+) ở giữa User Input và End, sau đó chọn View All Blocks... Tìm mục Google và chọn Search Google để đưa vào Canvas. Kết quả như</p>"
        ),
        ("<p class=\"lesson-p\">→</p>\n<p class=\"lesson-p\">Start User Input Search Google End</p>\n", ""),
        ("Chọn Search Google, chọn t Configuration, trong đó:</p>", "Chọn Search Google, chọn thẻ Configuration, trong đó:</p>"),
        ("để công cụ ti</p>", "để công cụ tìm</p>"),
        ("chẳng hạ</p>", "chẳng hạn</p>"),
        ("Plain text (văn bản thuần tu</p>", "Plain text (văn bản thuần tuý)</p>"),
        ("<p class=\"lesson-p\">hoạc định dạng JSON.</p>", "<p class=\"lesson-p\">hoặc định dạng JSON.</p>"),
        (
"""<p class="lesson-p">Configuration Quick Help</p>
<p class="lesson-p">G Search Google</p>
<p class="lesson-p">Search Query ((cau hol khach hang))</p>
<p class="lesson-p">You may include ((variables)).</p>
<p class="lesson-p">Output Variable : thong_tin_tim_kiem</p>
<p class="lesson-p">Save the output as a variable.</p>
<p class="lesson-p">Format Plain text</p>
<p class="lesson-p">Select the format you want the search 'results to be exported as.</p>""",
            ""
        ),
        (
            "<p class=\"lesson-p\">c) Tóm tắt nội dung tìm được và trả lời bằng LLM Bước 1. Thêm Generate Text:\n\n- Chọn nút ở giữa Search Google và End, rồi chọn Generate Text.</p>\n<p class=\"lesson-p\">Start User Input Search Google</p>\n<p class=\"lesson-p\">Ganarate</p>\n<p class=\"lesson-p\">C End</p>\n<p class=\"lesson-p\">Text</p>",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Tóm tắt nội dung tìm được và trả lời bằng LLM</h4>\n<p class=\"lesson-p\">Bước 1. Thêm Generate Text:\n\n- Chọn nút (+) ở giữa Search Google và End, rồi chọn Generate Text.</p>"
        ),
        ("<figcaption class=\"figure-caption\">Hình 2.11. Thêm Generate Text\n20</figcaption>", "<figcaption class=\"figure-caption\">Hình 2.11. Thêm Generate Text</figcaption>"),
        (
"""<p class="lesson-p">Configuration Quick Help</p>
<p class="lesson-p">thé Configuration, trong đó:

+ Model Settings: Chọn một LLM</p>
<p class="lesson-p">Generate Text</p>
<p class="lesson-p">(Claude 3 Haiku hoặc GPT-4o Mini).</p>
<p class="lesson-p">Prompt Opens in Prafier O</p>
<p class="lesson-p">+ Prompt: Viết prompt để hướng dẫn</p>
<p class="lesson-p">Bạn là trd lý áo thân thiện và hữu ích của</p>
<p class="lesson-p">LLM tóm tắt thông tin.

Ví dụ:</p>
<p class="lesson-p">cửa hàng tạp hóa gia đình An.

Dưới đây là thông tin liên quan đến câu hỏi của khách hàng: Câu hỏi:

{[cau_hoi_khach_hang 77</p>
<p class="lesson-p">"Bạn là trợ lí ảo thân thiện và hữu ích của</p>
<p class="lesson-p">Thông tin tìm được: f[thong_tin_tim_kiem]] Hãy trả lời câu hỏi của khách hàng một cách rõ rằng, ngân gọn, thân thiện và hữu ích, chí dựa vào thông tin được cung cắp.

Nếu thông tin không đủ để trả lời, hãy nói</p>
<p class="lesson-p">cửa hàng tạp hóa gia đình An.

Dưới đây là thông tin liên quan đến câu hỏi của khách hàng: Câu hỏi:

{{cau_hoi_khach_hang}}.</p>
<p class="lesson-p">rằng bạn không tin thấy thông tin cụ thể cho câu hỏi này và có thể hói thêm thông tin khác.</p>
<p class="lesson-p">Describe what you'd like the AI to generate. You may include ((variables)).</p>
<p class="lesson-p">Thông tin tìm được: ({thong_tin_tim_kiem}}.</p>
<p class="lesson-p">Hãy trả lời câu hỏi của khách hàng một cách rõ ràng, ngắn gọn, thân thiện và hữu ích, chỉ dựa vào thông tin được cung cấp.</p>
<p class="lesson-p">Settings</p>
<p class="lesson-p">Output Behavior</p>
<p class="lesson-p">Display to user</p>
<p class="lesson-p">Output Schema</p>
<p class="lesson-p">Text (Default)</p>
<p class="lesson-p">Nếu thông tin không đủ đế trả lời, hãy nói rằng bạn không tìm thấy thông tin cụ thể</p>
<p class="lesson-p">Chat History</p>
<p class="lesson-p">Behavior</p>
<p class="lesson-p">Include (default)</p>
<p class="lesson-p">cho câu hỏi này và có thể hỏi thêm thông tin khác."</p>
<p class="lesson-p">Control whether this message is visible in the history of any chat sessions.</p>
<p class="lesson-p">Lưu ý: {{thong_tin_ tim _kiem}} là biến chứa kết quả từ Search Google.

+ Settings:</p>
<p class="lesson-p">Model Settings O</p>
<p class="lesson-p">Claude 3.5 Haiku anthrogic/claude-3-5-haiku-28241922</p>
<p class="lesson-p">4 Inherited from the Workflow's Model Settings</p>
<p class="lesson-p">Output Behavior: Display to user để hiến thị cho người dùng; Save to variable để lưu vào biến (Variable Name: Tên biến).</p>""",
"""<p class="lesson-p">thẻ Configuration, trong đó:</p>
<p class="lesson-p">+ Model Settings: Chọn một LLM (Claude 3 Haiku hoặc GPT-4o Mini).</p>
<p class="lesson-p">+ Prompt: Viết prompt để hướng dẫn LLM tóm tắt thông tin. Ví dụ:</p>
<p class="lesson-p">"Bạn là trợ lí ảo thân thiện và hữu ích của cửa hàng tạp hóa gia đình An.</p>
<p class="lesson-p">Dưới đây là thông tin liên quan đến câu hỏi của khách hàng: Câu hỏi: {{cau_hoi_khach_hang}}.</p>
<p class="lesson-p">Thông tin tìm được: {{thong_tin_tim_kiem}}.</p>
<p class="lesson-p">Hãy trả lời câu hỏi của khách hàng một cách rõ ràng, ngắn gọn, thân thiện và hữu ích, chỉ dựa vào thông tin được cung cấp.</p>
<p class="lesson-p">Nếu thông tin không đủ để trả lời, hãy nói rằng bạn không tìm thấy thông tin cụ thể cho câu hỏi này và có thể hỏi thêm thông tin khác."</p>
<p class="lesson-p">Lưu ý: {{thong_tin_tim_kiem}} là biến chứa kết quả từ Search Google.</p>
<p class="lesson-p">+ Settings:</p>
<p class="lesson-p">Output Behavior: Display to user để hiển thị cho người dùng; Save to variable để lưu vào biến (Variable Name: Tên biến).</p>"""
        ),
        ("<figcaption class=\"figure-caption\">Hình 2.12. Thiết lập tham số cho</figcaption>", "<figcaption class=\"figure-caption\">Hình 2.12. Thiết lập tham số cho Generate Text</figcaption>"),
        ("<p class=\"lesson-p\">Generate Text</p>\n", ""),
        ("<li>O MAAMVOI E</li>\n", ""),
        ("dưới cùng của cửa số) để kiểm tra", "dưới cùng của cửa sổ) để kiểm tra"),
        ("<p class=\"lesson-p\">Bạn muốn hỏi gì về sản phẩm?</p>\n", ""),
        ("<figcaption class=\"figure-caption\">Hình 2.13. Giao diện ô trò chuyện</figcaption>", "<figcaption class=\"figure-caption\">Hình 2.13. Giao diện ô trò chuyện của Agent</figcaption>"),
        ("<p class=\"lesson-p\">của Agent</p>\n", ""),
        ("hiển thị bản tóm tắt kết quả</li>", "hiển thị bản tóm tắt kết quả.</li>"),
        (
"""<p class="lesson-p">AL AI Agent VD1</p>
<p class="lesson-p">Dua trên các nguồn thông tin, lỗi kin giai tribu 3 lasi sita tues orpanic dusc dann gia cao nhất hiện nay.</p>
<h3 class="subheading-h3"><span class="h3-num">1.</span> Sữa tươi Vinamilk 100% Organic</h3>
<ul class="lesson-bullet-list">
<li>La sês orgaric đầu tên đạt chung nhận têu chuấn châu du tại Việt Nam • Ser rudl du nhong con do chan ire tu neido • Panto vor uike vi ngues lint</li>
</ul>
<h3 class="subheading-h3"><span class="h3-num">2.</span> Sdo res TH True Mila Organic:</h3>
<ul class="lesson-bullet-list">
<li>Gia đình chuộng • Raay Wong: e0,0 kcal • Crua canai, protein o cet reamin cân eriét</li>
</ul>
<p class="lesson-p">) Dua tuer Orgaric CS ONl Ha Larc</p>
<ul class="lesson-bullet-list">
<li>Thương hiệu uy tín • Chất lượng đảm bảo</li>
</ul>
<p class="lesson-p">Quý khách có thể cân nhắc 3 loại sữa này để lựa chọn phù hợp với nhu cầu.</p>
<p class="lesson-p">D cary d star</p>""",
            ""
        ),
        ("<figcaption class=\"figure-caption\">Hình 2.14. Kết quả trả về sau khi tìm kiếm Google và sử dụng mô hình LLM</figcaption>", "<figcaption class=\"figure-caption\">Hình 2.14. Kết quả trả về sau khi tìm kiếm Google và sử dụng mô hình LLM để trả lời kết quả</figcaption>"),
        ("<p class=\"lesson-p\">để trả lời kết quả</p>\n", ""),
        ("quan trọng là em hiêu được nguyên lí hoạt động", "quan trọng là em hiểu được nguyên lí hoạt động"),
        (
            "<p class=\"lesson-p\">1. Mục đích chính của việc sử dụng công cụ no-code để xây dựng AI Agent là gì A. Để tạo ra các LLM mới từ đầu.</p>",
            "<p class=\"lesson-p\">1. Mục đích chính của việc sử dụng công cụ no-code để xây dựng AI Agent là gì?</p>\n<p class=\"lesson-p\">A. Để tạo ra các LLM mới từ đầu.</p>"
        ),
        ("các ứng dụng AI rất đơn giàn.</p>", "các ứng dụng AI rất đơn giản.</p>"),
        (
            "khối nào sẽ chịu trách nhiện cho việc truy cập và sử dụng một công cụ bên ngoài như Google Search API</p>",
            "khối nào sẽ chịu trách nhiệm cho việc truy cập và sử dụng một công cụ bên ngoài như Google Search API?</p>"
        ),
        ("<p class=\"lesson-p\">C. Tool Block.\n\nD. Input Block</p>", "<p class=\"lesson-p\">C. Tool Block.</p>\n<p class=\"lesson-p\">D. Input Block.</p>"),
        ("Ví dụ: Cảm ơn (Tên khách hàng), chúc bạn</li>", "Ví dụ: Cảm ơn [Tên khách hàng], chúc bạn</li>"),
        (
            "<p class=\"lesson-p\">Gọi ý: Hãy nghĩ về các bước từ khi giao dịch được ghi nhận cho đến khi thư điện tứ được gửi đi.</p>",
            "<p class=\"lesson-p\">Gợi ý: Hãy nghĩ về các bước từ khi giao dịch được ghi nhận cho đến khi thư điện tử được gửi đi.</p>"
        ),
        ("\n<p class=\"lesson-p\">CHỦ ĐỀ 2. RAG VÀ CÔNG CỤ</p>\n<p class=\"lesson-p\">LÀM VIỆC VỚI LLM</p>\n<p class=\"lesson-p\">AI</p>\n<p class=\"lesson-p\">RAG LLM</p>", ""),
    ],
    "bai-3-rag-nang-cao": [
        ("<p class=\"lesson-p\">Cam Scanner</p>\n", ""),
        ("<p class=\"lesson-p\">BAI 3. RAG NÂNG CAO</p>\n", ""),
        ("gặp câu hỏi: Nguyễn Du sinh năm nào?. Thay vì đọc", "gặp câu hỏi: \"Nguyễn Du sinh năm nào?\". Thay vì đọc"),
        ("thay vi để nguyên văn bản dài?", "thay vì để nguyên văn bản dài?"),
        (
            "<p class=\"lesson-p\">1. Các thành phần kĩ thuật trong bước truy xuất Các mô hình ngôn ngữ lớn (Large Language Model, viết tắt là LLM) như ChatGPT không thế ghi nhớ mọi chi tiết từ hàng trăm trang tài liệu.",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Các thành phần kĩ thuật trong bước truy xuất</h3>\n<p class=\"lesson-p\">Các mô hình ngôn ngữ lớn (Large Language Model, viết tắt là LLM) như ChatGPT không thể ghi nhớ mọi chi tiết từ hàng trăm trang tài liệu."
        ),
        ("Cụ thế, khi có câu hỏi", "Cụ thể, khi có câu hỏi"),
        ("cửa số ngữ cảnh", "cửa sổ ngữ cảnh"),
        ("ví dụ theo từng cập</p>", "ví dụ theo từng cặp</p>"),
        ("Nhớ cách làm này, khi bạn Minh Châu hỏi về năm sinh của Nguyễn Du, AI có thể tim đúng đoạn thơ", "Nhờ cách làm này, khi bạn Minh Châu hỏi về năm sinh của Nguyễn Du, AI có thể tìm đúng đoạn thơ"),
        ("<p class=\"lesson-p\">RAG</p>\n<p class=\"lesson-p\">RAG</p>\n<p class=\"lesson-p\">RAC</p>\n", ""),
        ("dùng RAG đề truy xuất dữ liệu", "dùng RAG để truy xuất dữ liệu"),
        (
            "<p class=\"lesson-p\">a) Kĩ thuật chia nhỏ nội dung Trước tiên, để LLM",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Kĩ thuật chia nhỏ nội dung</h4>\n<p class=\"lesson-p\">Trước tiên, để LLM"
        ),
        ("LLM tìm kiểm chính xác và nhanh hơn", "LLM tìm kiếm chính xác và nhanh hơn"),
        ("của tài liệu (như tiêu đẻ, mỤc lục).", "của tài liệu (như tiêu đề, mục lục)."),
        ("bán có ý nghĩa hoàn chỉnh.\n\nHình 3.2. Hinh ảnh một văn bản được chia thành các đoạn nhỏ bằng thuật toán</p>", "bản có ý nghĩa hoàn chỉnh.</p>\n" + make_figure_box("Hình 3.2. Hình ảnh một văn bản được chia thành các đoạn nhỏ bằng thuật toán")),
        ("giảm nhiều.</p>", "giảm nhiễu.</p>"),
        ("dãy sô (gọi là vector). Dãy sô này giông như", "dãy số (gọi là vector). Dãy số này giống như"),
        ("giúp máy tính hiêu được ý nghĩa của nó.", "giúp máy tính hiểu được ý nghĩa của nó."),
        ("trong không gian này - Nguyên lí hoạt động:", "trong không gian này. - Nguyên lí hoạt động:"),
        ("để máy tính hiếu và xử lí được ý nghĩa", "để máy tính hiểu và xử lí được ý nghĩa"),
        (
            "<p class=\"lesson-p\">c) Kĩ thuật lưu trữ vector Sau khi các đoạn văn bản đã được mã hóa thành vector",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Kĩ thuật lưu trữ vector</h4>\n<p class=\"lesson-p\">Sau khi các đoạn văn bản đã được mã hóa thành vector"
        ),
        ("được má hóa thành vector,", "được mã hoá thành vector,"),
        ("như một \"thư viện lớn\".\", nơi các \"tọa độ\"", "như một \"thư viện lớn\", nơi các \"tọa độ\""),
        ("thông lin được sắp xếp khoa học", "thông tin được sắp xếp khoa học"),
        (
            "sử dụng các thuật toán tìm kiếm hiệu</p>\n<p class=\"lesson-p\">lựa để nhanh chóng tìm ra các vector \" dùng.",
            "sử dụng các thuật toán tìm kiếm hiệu quả</p>\n<p class=\"lesson-p\">để nhanh chóng tìm ra các vector \"gần nhất\" với vector câu hỏi của người dùng."
        ),
        ("Khi em tìm ào ấm mùa đông", "Khi em tìm áo ấm mùa đông"),
        ("được mã hoa thành vector.", "được mã hoá thành vector."),
        ("kho lưu trữ vector để lầy các sản phẩm", "kho lưu trữ vector để lấy các sản phẩm"),
        ("là việc trở các đoạn văn bản", "là việc trữ các đoạn văn bản"),
        ("truy xuất nhanh chóng cáo thông tin liên quan", "truy xuất nhanh chóng các thông tin liên quan"),
        (
"""<p class="lesson-p">Documents Embedding</p>
<p class="lesson-p">Model Vectorstore</p>
<p class="lesson-p">Query Context/</p>
<p class="lesson-p">LLM</p>
<p class="lesson-p">Prompt</p>
<p class="lesson-p">User</p>
<p class="lesson-p">Output</p>""",
            ""
        ),
        ("<figcaption class=\"figure-caption\">Hình 3.3. Sơ đồ quy trình từ khi người dùng gửi câu hỏi đến khi truy xuất thông tin từ</figcaption>", "<figcaption class=\"figure-caption\">Hình 3.3. Sơ đồ quy trình từ khi người dùng gửi câu hỏi đến khi truy xuất thông tin từ kho lưu trữ vector và tạo phản hồi bằng LLM</figcaption>"),
        ("<p class=\"lesson-p\">kho lưu trữ vector và tạo phản hồi bằng LLM</p>\n", ""),
        (
"""<p class="lesson-p">Tãi liệu góc</p>
<p class="lesson-p">(Chia nhỏ nội dung) →</p>
<p class="lesson-p">Chunking</p>
<p class="lesson-p">Embedding</p>
<p class="lesson-p">Vector Store</p>
<p class="lesson-p">(Văn bản đầu vào)</p>
<p class="lesson-p">(Biểu diễn vector)</p>
<p class="lesson-p">(Lưu trữ vecto</p>""",
            ""
        ),
        (
            "<p class=\"lesson-p\">2. Tâm quan trọng của chất lượng truy xuất thông tin Bước truy xuất đóng vai trò",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Tầm quan trọng của chất lượng truy xuất thông tin</h3>\n<p class=\"lesson-p\">Bước truy xuất đóng vai trò"
        ),
        (
            "a) Hậu quả khi truy xuất kém chất lượng Nếu bước truy xuất không chính xác,",
            "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Hậu quả khi truy xuất kém chất lượng</h4>\n<p class=\"lesson-p\">Nếu bước truy xuất không chính xác,"
        ),
        ("đầu vào đã bị lối.</p>", "đầu vào đã bị lỗi.</p>"),
        (
            "<p class=\"lesson-p\">b) Yếu tố quyết định chất lượng truy xuất - Chia nhỏ nội dung hợp lí:",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Yếu tố quyết định chất lượng truy xuất</h4>\n<p class=\"lesson-p\">- Chia nhỏ nội dung hợp lí:"
        ),
        ("chứa nhiều thông tin nhiều.", "chứa nhiều thông tin nhiễu."),
        ("Biểu diễn vector không chuấn sẽ làm giảm", "Biểu diễn vector không chuẩn sẽ làm giảm"),
        ("thuật toán tim kiêm hiệu quả. Nếu các bước này kém, LLM nhận thông tin không đầy đúng/sai, dẫn đến câu trả lời thiêu chính xác.", "thuật toán tìm kiếm hiệu quả. Nếu các bước này kém, LLM nhận thông tin không đầy đủ/sai, dẫn đến câu trả lời thiếu chính xác."),
        ("C. Tìm kiểm thông tin liên quan", "C. Tìm kiếm thông tin liên quan"),
        ("Mục đích chinh của kĩ thuật", "Mục đích chính của kĩ thuật"),
        ("A. Câu trả lời sẽ dai hơn.</p>", "A. Câu trả lời sẽ dài hơn.</p>"),
        ("phản ứng như thê nào?</p>", "phản ứng như thế nào?</p>"),
        ("\n<p class=\"lesson-p\">AF</p>\n<p class=\"lesson-p\">D</p>", ""),
    ],
    "bai-4-thu-vien-nguon-mo-llm": [
        ("<p class=\"lesson-p\">BAI 4! THƯ VIÊN</p>\n<p class=\"lesson-p\">NGUỒN MỞ LLM</p>\n", ""),
        ("<li>Tính tống giá tiền", "<li>Tính tổng giá tiền"),
        ("món ăn đơn giàn</li>", "món ăn đơn giản</li>"),
        ("tra cứu công thức và kiếm tra</p>\n<p class=\"lesson-p\">nguyen liệu", "tra cứu công thức và kiểm tra</p>\n<p class=\"lesson-p\">nguyên liệu"),
        ("<p class=\"lesson-p\">Đế giải quyết các yêu cầu phức tạp này,", "<p class=\"lesson-p\">Để giải quyết các yêu cầu phức tạp này,"),
        ("<p class=\"lesson-p\">hiêu ý định, chọn công cụ", "<p class=\"lesson-p\">hiểu ý định, chọn công cụ"),
        ("cho đên khi đưa ra", "cho đến khi đưa ra"),
        ("thực hiện điêu này?</p>", "thực hiện điều này?</p>"),
        ("truy cập và hiếu thông tin", "truy cập và hiểu thông tin"),
        ("(ví dự: giá sản phẩm", "(ví dụ: giá sản phẩm"),
        ("<p class=\"lesson-p\">được nhiêu trong thực tế</p>", "<p class=\"lesson-p\">được nhiều trong thực tế.</p>"),
        (
"""<p class="lesson-p">Agents</p>
<p class="lesson-p">Prompt Templates</p>
<p class="lesson-p">Retrieval Modules</p>
<p class="lesson-p">+</p>
<p class="lesson-p">Memory Callbacks</p>""",
            ""
        ),
        ("các thành phần cốt lợi sau:</p>", "các thành phần cốt lõi sau:</p>"),
        ("Cho phép kết nối vá truy vấn", "Cho phép kết nối và truy vấn"),
        ("Đây là cầu nói giúp ứng dụng của em \"nói chuyện\" được với bát ki LLM nào.", "Đây là cầu nối giúp ứng dụng của em \"nói chuyện\" được với bất kì LLM nào."),
        ("Các cấu trúc sản có giúp định dạng truy vắn</li>", "Các cấu trúc sẵn có giúp định dạng truy vấn</li>"),
        ("Giá của sản phẩm (Tên sản phẩm] là bao nhiêu?.</p>", "Giá của sản phẩm [Tên sản phẩm] là bao nhiêu?</p>"),
        ("Là bộ não điều khiến giúp LLM lự lên kế hoạch", "Là bộ não điều khiển giúp LLM tự lên kế hoạch"),
        ("<li>Mô-dun truy xuất", "<li>Mô-đun truy xuất"),
        ("nhúng vào ứng dụng để ghĩ</li>", "nhúng vào ứng dụng để ghi</li>"),
        ("<p class=\"lesson-p\">nhật ki, giám sát", "<p class=\"lesson-p\">nhật kí, giám sát"),
        (
            "<p class=\"lesson-p\">LangChain, ngôi nhà thông minh làm việc dựa vào quy trình làm việc hay còn</p>\n<p class=\"lesson-p\">thành một nhiệm vụ. Mỗi hành động nhỏ trong một chuối được gọi là một liên kết (Link).",
            "<p class=\"lesson-p\">LangChain, ngôi nhà thông minh làm việc dựa vào quy trình làm việc hay còn gọi là chuỗi (Chain) các hành động tự động, được sắp xếp theo trình tự để hoàn thành một nhiệm vụ. Mỗi hành động nhỏ trong một chuỗi được gọi là một liên kết (Link)."
        ),
        (
"""<p class="lesson-p">Chuỗi hành động (Chain)</p>
<p class="lesson-p">Quy trinh hoàn chỉnh giái quyét bài toán</p>
<p class="lesson-p">Phần tích đề bài Tìm kiếm kiến thức liên</p>
<p class="lesson-p">Lập luận và giải Trình bày lời giải</p>
<p class="lesson-p">quan</p>
<p class="lesson-p">Liên kết (Link)</p>""",
            ""
        ),
        ("giúp xây dựng cac ứng dụng dùng LLM hiệu quả hơn. Mục đich chính", "giúp xây dựng các ứng dụng dùng LLM hiệu quả hơn. Mục đích chính"),
        ("cửa hàng, môn học) vào đề LLM xử lí.\n\n• Hồ trợ hành động phức tạp:", "cửa hàng, môn học) vào để LLM xử lí.</li>\n<li>Hỗ trợ hành động phức tạp:"),
        ("thông qua việc tố chức các quy trình", "thông qua việc tổ chức các quy trình"),
        ("LlamaIndex - Thù kho chuyên nghiệp", "LlamaIndex - Thủ kho chuyên nghiệp"),
        (
            "Để trợ lí ào của An trả lời được câu hỏi 2 kg gạo ST25 có giá bao nhiêu?, LLM cần có thông tin về giá gạo. Các LLM lớn thường chỉ được huần luyện trên dữ liệu công khai và không có kiên thức cụ thể về giá trong cừa hàng của gia đình An.",
            "Để trợ lí ảo của An trả lời được câu hỏi 2 kg gạo ST25 có giá bao nhiêu?, LLM cần có thông tin về giá gạo. Các LLM lớn thường chỉ được huấn luyện trên dữ liệu công khai và không có kiến thức cụ thể về giá trong cửa hàng của gia đình An."
        ),
        ("chuyên biệt đề kết nối LLM", "chuyên biệt để kết nối LLM"),
        (
            "<p class=\"lesson-p\">Vai trò của LlamaIndex trong truy xuất và xử lí dữ liệu cho RAG LlamaIndex tập trung sâu",
            "<h4 class=\"subheading-h4\">Vai trò của LlamaIndex trong truy xuất và xử lí dữ liệu cho RAG</h4>\n<p class=\"lesson-p\">LlamaIndex tập trung sâu"
        ),
        (
"""<p class="lesson-p">E Thành phán LlamaIndex gồm có:</p>
<ul class="lesson-bullet-list">
<li>Data Connectors</li>
</ul>
<p class="lesson-p">Data Indexes</p>
<p class="lesson-p">Thu thập dữ liệu từ nhiêu nguồn khác nhau một cách Tinh hoạt và hiệu quả</p>
<p class="lesson-p">Tổ chức dữ liệu để thy kiểm hibu quả vì dy Vedlor Stoce inded</p>
<p class="lesson-p">Retrieval</p>
<p class="lesson-p">Query Engines</p>
<p class="lesson-p">Tìm kiếm thông tin liên quan từ trước một cách chính xác và nhanh chóng</p>
<ul class="lesson-bullet-list">
<li>Giao điện để truy vẫn dữ tiêu, kết háp tm kiếm và:</li>
</ul>""",
            ""
        ),
        ("chính sách khuyên mãi,", "chính sách khuyến mãi,"),
        ("ghi chú viết tay mà An đã sô hoá.", "ghi chú viết tay mà An đã số hoá."),
        ("thu thập thông tin tử một trang web", "thu thập thông tin từ một trang web"),
        ("để LLM đọc cà một tệp PDF dài,", "để LLM đọc cả một tệp PDF dài,"),
        ("đọc lại cả cuốn số tay sản phẩm", "đọc lại cả cuốn sổ tay sản phẩm"),
        ("có ý nghĩa gân nhất với câu hỏi này", "có ý nghĩa gần nhất với câu hỏi này"),
        ("người dùng và chuyến giao cho LLM. LLM sau đó sẽ sử dụng cà câu hỏi", "người dùng và chuyển giao cho LLM. LLM sau đó sẽ sử dụng cả câu hỏi"),
        ("có giá 120 000 VNĐ ạ.\n\n36</p>", "có giá 120 000 VNĐ ạ.</p>"),
        (
            "Như vày. LlamaIndex chinh là cầu nổi vững chắc giữa LLM và kho kiến thức riêng của em, giúp LLM có thể trả lời các câu hỏi cụ thế, chính xác và cập nhật mà bân thân LLM chưa được huân luyện.",
            "Như vậy, LlamaIndex chính là cầu nối vững chắc giữa LLM và kho kiến thức riêng của em, giúp LLM có thể trả lời các câu hỏi cụ thể, chính xác và cập nhật mà bản thân LLM chưa được huấn luyện."
        ),
        ("• Data Connectors: Tài dữ liệu từ nhiều nguồn.</p>\n<p class=\"lesson-p\">CANNO</p>", "• Data Connectors: Tải dữ liệu từ nhiều nguồn.</p>"),
        ("Mục địch chinh của LangChain là gì?", "Mục đích chính của LangChain là gì?"),
        ("B. Cung câp một khung làm việc", "B. Cung cấp một khung làm việc"),
        ("chịu trách nhiệm chính trong việc \"tài\" dữ liệu từ các tệp PDF, trang web hay cơ số dữ liệu?", "chịu trách nhiệm chính trong việc \"tải\" dữ liệu từ các tệp PDF, trang web hay cơ sở dữ liệu?"),
        (
            "<p class=\"lesson-p\">COSSRT VẬN DỤNG</p>",
            "</div></section>\n\n            <section class=\"lesson-card apply-section\" id=\"sec-vận-dụng\">\n                <div class=\"section-badge-header\">\n                    <span class=\"sec-icon\">🚀</span>\n                    <h2 class=\"section-title\">VẬN DỤNG</h2>\n                </div>\n                <div class=\"section-body\">"
        ),
        ("nếu bố mẹ An muốn trợ lí ào có thê:</p>", "nếu bố mẹ An muốn trợ lí ảo có thể:</p>"),
        ("của kháchh", "của khách"),
        ("<p class=\"lesson-p\">H</p>\n", ""),
    ],
    "bai-5-khai-thac-thu-vien-nguon-mo-llm": [
        ("<p class=\"lesson-p\">BÀI 5. KHAI THÁC THƯ VIỆN</p>\n<p class=\"lesson-p\">NGUỒN MỞ LLM</p>\n", ""),
        ("Với câu hội thứ nhất:", "Với câu hỏi thứ nhất:"),
        ("của kháchh", "của khách"),
        (
            "<p class=\"lesson-p\">1. LangChain và LlamaIndex: Hai chuyên gia, một mục tiêu Trọng tình huống của An, chỉ dùng một công cụ là chưa đủ vị mỗi câu hỏi",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> LangChain và LlamaIndex: Hai chuyên gia, một mục tiêu</h3>\n<p class=\"lesson-p\">Trong tình huống của An, chỉ dùng một công cụ là chưa đủ vì mỗi câu hỏi"
        ),
        ("vừa tìm đúng dữ liệu tù nhiêu nguồn.</p>", "vừa tìm đúng dữ liệu từ nhiều nguồn.</p>"),
        ("giúp điều phối quá trình xữ lí:", "giúp điều phối quá trình xử lí:"),
        ("LangChain điều khiến dòng xử lí, LlamaIndex tập trung tim thông tin", "LangChain điều khiển dòng xử lí, LlamaIndex tập trung tìm thông tin"),
        ("thu thập thông tin tôn kho, sắp xép chúng và tìm kiêm chính xác", "thu thập thông tin tồn kho, sắp xếp chúng và tìm kiếm chính xác"),
        ("đóng vai trò người tố chức thông minh,", "đóng vai trò người tổ chức thông minh,"),
        (
"""<p class="lesson-p">LangChain logic LlamaIndex data</p>
<p class="lesson-p">Lang Chain</p>
<p class="lesson-p">Chain</p>
<p class="lesson-p">Build full LLM apps</p>
<p class="lesson-p">Agents Indera</p>
<p class="lesson-p">Prompts Structured data</p>
<p class="lesson-p">sources</p>
<p class="lesson-p">Deployment</p>""",
            ""
        ),
        ("kiến trúc sư xây dựng tổng thế.</li>", "kiến trúc sư xây dựng tổng thể.</li>"),
        ("Khả năng bố trợ nhau", "Khả năng bổ trợ nhau"),
        ("là hai công cụ bố trợ đắc lực", "là hai công cụ bổ trợ đắc lực"),
        ("<p class=\"lesson-p\">Đề trợ lí ảo của An", "<p class=\"lesson-p\">Để trợ lí ảo của An"),
        ("(được điều khiến bởi LangChain)", "(được điều khiển bởi LangChain)"),
        (
"""<p class="lesson-p">Load</p>
<p class="lesson-p">Nạp dữ liệu Chia nhỏ</p>
<p class="lesson-p">Biêu diễn</p>
<p class="lesson-p">Tác nhân quyết định</p>
<p class="lesson-p">Lập luận Trả lời</p>
<p class="lesson-p">nội dung</p>
<p class="lesson-p">vector</p>
<p class="lesson-p">Lamaindex Lang Chain</p>""",
            ""
        ),
        ("LangChain và LlamaIndex bố trợ lẫn nhau. LlamaIndex chuyên về dữ liệu: tài, lập chỉ mục,", "LangChain và LlamaIndex bổ trợ lẫn nhau. LlamaIndex chuyên về dữ liệu: tải, lập chỉ mục,"),
        ("Em có thể kết hợp cà hai trong một dự án", "Em có thể kết hợp cả hai trong một dự án"),
        ("<p class=\"lesson-p\">(Hướng dân sau đây", "<p class=\"lesson-p\">(Hướng dẫn sau đây"),
        ("<p class=\"lesson-p\">Chuẩn bị môi trường Trước khi cài đặt thư viện,", "<h4 class=\"subheading-h4\">Chuẩn bị môi trường</h4>\n<p class=\"lesson-p\">Trước khi cài đặt thư viện,"),
        ("Hãy tìm kiêm</p>", "Hãy tìm kiếm</p>"),
        (
"""                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">pip install -U llama-index llama-index-embeddings-huggingface llama-</code></pre>
                    </div>
                    
<p class="lesson-p">index-LLMs-ollama langchain langchain-community pypdf transformers sentence-transformers bitsandbytes accelerate openai</p>""",
            make_code_block("pip install -U llama-index llama-index-embeddings-huggingface llama-index-llms-ollama langchain langchain-community pypdf transformers sentence-transformers bitsandbytes accelerate openai")
        ),
        (
            "<p class=\"lesson-p\">a) Tâi thông tin và tạo chỉ mục Llamalndox Tạo hai tệp văn bản trong cúng thư mục với đoạn mã Python và điên thông tin sản phẩm vào đó.</p>",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Tải thông tin và tạo chỉ mục LlamaIndex</h4>\n<p class=\"lesson-p\">Tạo hai tệp văn bản trong cùng thư mục với đoạn mã Python và điền thông tin sản phẩm vào đó.</p>"
        ),
        ("<p class=\"lesson-p\">file: pan phom. l.x!</p>", "<p class=\"lesson-p\">File: san_pham.txt</p>"),
        ("Bánh quy Kinh Dộ Marie:", "Bánh quy Kinh Đô Marie:"),
        ("Gạo ST25: 120 000 VND/3kg.\n\nFllo: khuyon mal.txt</p>", "Gạo ST25: 120 000 VNĐ/3kg.</p>\n<p class=\"lesson-p\">File: khuyen_mai.txt</p>"),
        ("mì tôm Háo Háo tặng 1 gói cúng loại.", "mì tôm Hảo Hảo tặng 1 gói cùng loại."),
        ("Giảm giá 10% cho tất cá các sán phâm sữa", "Giảm giá 10% cho tất cả các sản phẩm sữa"),
        ("Tạo một tệp main py có nội dung như sau:", "Tạo một tệp main.py có nội dung như sau:"),
        (
"""<p class="lesson-p">trong Ilona _Indox, enbeddingo hugglogface lapore Huggingtosenbsdasng</p>

                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">trong lama _index. licr. illane import Ollams
trum lans Index.:uir.100% Import QueryEngineTool, ToolMetadata
trong lama_index. :orn. agone Import ReActhgens
tram langcholn. agore» loport igentezecutot, creste_tesct_ayent</code></pre>
                    </div>
                    

                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">trong langshain_cors, pecspie import Prompttemplate
from langchain_core. ensaoyes Import AIhersage, Hunaskessage</code></pre>
                    </div>
                    
<p class="lesson-p">1 --- Câu hinh chung -..

• Bat Logging dé xem que trinh xù 1y cûs bllamaindex logging.basscconfig(stream-oyo.acdout,level-logging.INkD) 10ggtmg.getlogger1).addlandler(logging.GcreanHandiez(syg.otdool))</p>

                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">1 -- a) Tál thông tin sân phẩn và chuơng trính khuyến nếi từ cáờ tập khác
nhoa ---
print/"Dang tái do lifu tú các tép...")
1 Tái tát có cáo tếp từ thu mc hiện ta1
documento -gimpledirectoxyReader/"./").Jond_doca()
print(["Dó tás (Ien(documents)) tái lifu..")</code></pre>
                    </div>
                    
<p class="lesson-p">( --- b) Tạo một chi muc dữ liệu bäng Ilamaindex print/"Dang too chi muc dü 11eu..")</p>
<ul class="lesson-bullet-list">
<li>1. Cau hinh ms hinh nhung (Embedding Model) • Sử dụng mô hình nhúng của Hugging face dé tạo vector biểu diễn agü sghle cho vẫn bán.

8 Mo hinh "sentence-tranaforner:/paraphrose-mult111ngua1-M201141-112-72" 65 tro da ngôn ngõ.</li>
</ul>
<p class="lesson-p">settings.ented_n0del - Huggingfacelmbedd1ng(</p>
<p class="lesson-p">model_sane-"sentence-tranaforners/poraphrose-mult1i1nqu»?-Mın: IM-LI2-</p>
<ul class="lesson-bullet-list">
<li>Sủ dung CPU dể dam bdo chay duoc trên s01 say tinh khöng co GFU mash devicen"cpu" )</li>
<li>2. Câu hình mô hình ngôn ngữ lớn (1121) • sử dụng Ollama với mô hình "llama2" chạy cục bộ.

• Đảm bảo bon 1ã cà1 dất O11ara và kéo mo hinh 11ams2:

• Tåt Ollana tu httpt://ol1ans.com/ • Chay lenh: ol1ama run 11ama2 Settingo. I2i = O11an0 (model-"Ilana2", reguest_timeout-360.0) d I62g 12000u= cho các câu trẻ 101 dài</li>
</ul>
<p class="lesson-p">* 3. Xây dụng chi muc vector • Chỉ mục nảy sẽ giúp chúng ca tin kiên thống cin nhanh chóng và hiệu quả.

index - VectorStoreIndex.fzom documents (docunenca) print("Đã tạo chỉ mục dữ liệu thành công")g.") 42</p>""",
            BAI5_CODE_PART1
        ),
        (
            "<p class=\"lesson-p\">b) Xây dựng Agent LangChain sử dụng LlamaIndex làm công cụ Chúng ta sẽ tạo một công cụ",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Xây dựng Agent LangChain sử dụng LlamaIndex làm công cụ</h4>\n<p class=\"lesson-p\">Chúng ta sẽ tạo một công cụ"
        ),
        (
"""<p class="lesson-p">1 --- c) Xây dựng một Agent LangChain có khả năng sử dụng chỉ muo của LlamaIndex nhu một công cụ ---

print ("Dang xáy dựng Agent LangChain...")</p>
<p class="lesson-p">* 1. Ipo Query Engine từ chi muo 7 Query Engine giúp chúng ta hỏi các câu hỏi về chỉ mục.</p>
<p class="lesson-p">tương đồng nhất guezy_engine-index.os_query_engine(s1m/larity_ top kol) o lidy 3 ket qud</p>
<ul class="lesson-bullet-list">
<li>2. Đinh nghia công cụ (Iool) cho Agent • Công cụ này cho phép Agent sử dụng Query Engine để tìm kiêm thông tin aản</li>
</ul>

<p class="lesson-p">Sử dụng công cụ này khi người dùng hỏi về:</p>
<ul class="lesson-bullet-list">
<li>Giá cả của sản phẩm (ví dụ: "Giá sữa Vinamilk là bao nhiêu?") - Thông tin chi trết về sản phẩm(ví dụ: "Bánh quy Rinh Đô Marie có gì đăc biệt?")</li>
<li>Các chương trình khuyến mãi, ưu đãi (ví dụ: "M1 tôm Hảo lào có khuyến mái gì không?", "Khuyến mãi tháng 6 là gì?").</li>
</ul>
<p class="lesson-p">Bạn PHẢI sử dụng công cụ này để truy xuất vẫn thông tin trước khi trà lài các câu hỏi liên quan đến sản phẩn và khuyến mài.</p>
<p class="lesson-p">3. Khỏi tạo Agent 7 Chúng ta sẽ sử dụng ReActagent của LlamaIndex vì nó tích hợp tốt với các công cụ của LlamaIndex 1 và có khả năng suy luận để chọn công cụ phù hạp.

systen prompt_v1 = \"\"\" tra lý ảo thông minh, thân thiện và hữu Ich, chuyên cụng cấp thông tin rẽ sản phẩn và cức chuong trình khuyên mãi.

Nhiệm vụ của bạn là trả lời các câu hỏi của người dùng một cách chính xác và</p>
<p class="lesson-p">đáy dủ, dựa trên các thông tin bạn có.

Bạn có khẻ năng sử dụng các CÔNG CỤ (tools) đế tìm kiêm thông Khi người dùng hỏi về gản phẩm, giá cà, hoặc các chương trình khuyện mãi, bạn PHẢI SỬ DỤNG công cụ "thong_ tin _sản pham vo _khuyen mai' để láy dữ liệu.</p>
<p class="lesson-p">Luôn trẻ lời bằng TIÊNG VIỆT.</p>
<p class="lesson-p">agent = ReActAgent. Iron_10015(</p>
<p class="lesson-p">toolg=[query_engine_tooll, 11m=Settings.11n, verbose-True, system _prompt-system _prompt_vi, 4 Thêm system prompt tiêng Vięt</p>
<p class="lesson-p">print ("Đã xây dụng Agent LangChain thành công. ")</p>
<p class="lesson-p">* --- Phần tương tác với người dùng ---

print ("\\n--- Sẵn sàng trẻ lời câu hỏi của bạn! ---") print ("Bạn có thể hỏi về thông tin sản phẩm, giá cà, hoặc các chương trình khuyên mãi. ") print ("Gö 'thoát" đế thoát. ")</p>
<p class="lesson-p">while True:</p>
<p class="lesson-p">question = input (")nBan hỏi: ") if question. lover() = 'thoát':</p>

                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">print("Cám on bạn đã sử dụng!")
break</code></pre>
                    </div>
                    
<p class="lesson-p">response = agent.chat (question) print (f"Agent trà lờ1: (response)") except Exception as e:</p>
<p class="lesson-p">print (f"Có lỗi xây rai (e). Vui lông thủ 1ọ1 hoặc kiển tra lại cài đật o11ama. ")</p>""",
            BAI5_CODE_PART2
        ),
        ("- Hôm nay là thứ mây?", "- Hôm nay là thứ mấy?"),
        (
"""<p class="lesson-p">Đã xây đựng Agent LangChain thánh công.</p>
<ul class="lesson-bullet-list">
<li>-- sản sàng crả lời câu hỏi của ban! -

Bạn có thể hỏi về thông tin sản phẩm, giá cá, hoặc các chương trính khuyến mãi.

Gõ "thoát" để thoát.</li>
</ul>
<p class="lesson-p">Bạn hỏi: Sữa tươi Vinamilk có đường giả bao nhiêu > Running step Bcb88656-Sde9-482f-a012-814cb405083d. Step input: Sữa tươi VinamiLk có đường giá bao nhiêu</p>""",
            ""
        ),
        (
"""<p class="lesson-p">Bạn hỏi: Sữa tươi Vinamilk có đưỡng giá bao nhiều S Running step 8cb88656-5de9-482f-a012-814cb405083d. Step input: Sữa tươi Vinamilk có đường giả bao nhiêu INFO:httpx:HTTP Request: POST http://localhost:11434/ap1/chat "HTTP/1.1 200 OK"</p>
<p class="lesson-p">Action Input: ('input": Sữa tươi Vinamilk gid bao nhiều?" nun beans': 5) INFO: httpx:HTTP Request: POST http://localhost:11434/api/chat *HTTP/1.1 200 ОК" HTTP Request: POST http://localhost:11434/api/chat "HПTP/1.1 200 OK" Observation: Based on the provided context the price of Vinamilk's fresh mith ts 25,000 WAD per liter > Running step 56c10474-9b6d-47cf-a889-1ca052c39d67. Step Input: None INFO: httpx:HTTP. Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 ОК" HTTP Request: POST http://ocalhost:11434/api/chat "HTTP/1.1 200 ОК™ Thought: I can answer without using any aore tools, I'IZ use the aser's language to answer Answer: Giá sữa tươi Vinamilk Là 25, 000 VND/Lit.

Agent trả lời: Giá sữa tươi Vinamilk là 25,000 VND/Lit.</p>""",
            ""
        ),
        (
            "2. Việc Lamalndez lố chúc dữ liệu sản phâm thành một chỉ mục (index) so với cái nào là quan trong nhất trong quá trình BAG!",
            "2. Việc LlamaIndex tổ chức dữ liệu sản phẩm thành một chỉ mục (index) có vai trò nào là quan trọng nhất trong quá trình RAG?"
        ),
        ("A. Giúp LLM ghi nhỏ lịch sử hội thoái.", "A. Giúp LLM ghi nhớ lịch sử hội thoại."),
        ("C. Đám bảo thông tin được truy xuất nhanh chóng và chính vác; khi cần.", "C. Đảm bảo thông tin được truy xuất nhanh chóng và chính xác khi cần."),
        ("D. Định dạng lại dâu ra của LLM thành JSON.", "D. Định dạng lại đầu ra của LLM thành JSON."),
        (
            "kết hợp LangChain và Lamalndey lại hiệu quả hơn sọ với việc chí sử dụng một trong hai cho một cng dung tra li ào phúc lap nhu của An.",
            "kết hợp LangChain và LlamaIndex lại hiệu quả hơn so với việc chỉ sử dụng một trong hai cho một ứng dụng trợ lí ảo phức tạp như của An."
        ),
        ("An muốn nâng cáp đế trợ lí ảo của minh có khá năng:", "An muốn nâng cấp để trợ lí ảo của mình có khả năng:"),
        ("Tóm tất một báo cáo doanh thu dài (tệp PDF) thành các gạch đâu dòng chính.", "Tóm tắt một báo cáo doanh thu dài (tệp PDF) thành các gạch đầu dòng chính."),
        ("giá trung bình trên thị trướng (bắng cách tìm kiếm trên mạng).", "giá trung bình trên thị trường (bằng cách tìm kiếm trên mạng)."),
        (
            "Lang Chain và LlamaIndex sẽ cúng nhau đóng vai trò như thể náo? Em hãy hinh dung luồng xử lí và các thành phần chinh được sử dụng.",
            "LangChain và LlamaIndex sẽ cùng nhau đóng vai trò như thế nào? Em hãy hình dung luồng xử lí và các thành phần chính được sử dụng."
        ),
        ("\n<p class=\"lesson-p\">CHỦ ĐỂ 3. ĐẠO ĐỨC, TRÁCH NHIỆM</p>\n<p class=\"lesson-p\">VÀ TÁC ĐỘNG XÃ HỘI TRONG AI</p>\n<p class=\"lesson-p\">TẠO SINH</p>\n<p class=\"lesson-p\">Al</p>", ""),
    ],
    "bai-6-tac-dong-cua-ai-den-doi-song-con-nguoi": [
        ("trong việc huần luyện và vận hành", "trong việc huấn luyện và vận hành"),
        ("tạo ảnh bằng AI đã mỏ ra nhiều hướng đi mới,", "tạo ảnh bằng AI đã mở ra nhiều hướng đi mới,"),
        ("về AI tạo sinh cần tiêu thự lượng điện năng lớn,", "về AI tạo sinh cần tiêu thụ lượng điện năng lớn,"),
        ("AI tạo sinh có khá năng tạo ra nội dung mới", "AI tạo sinh có khả năng tạo ra nội dung mới"),
        ("Nhóm vấn đề vê an toàn thông tin cá nhân", "Nhóm vấn đề về an toàn thông tin cá nhân"),
        ("Đây là những yêu tố mỗi cá nhân cần chủ động", "Đây là những yếu tố mỗi cá nhân cần chủ động"),
        ("hoặc địa chỉ từ dữ liệu huân luyện.</p>", "hoặc địa chỉ từ dữ liệu huấn luyện.</p>"),
        ("và làm suy giảm niêm tin của</p>", "và làm suy giảm niềm tin của</p>"),
        ("b) Nhóm vấn đề về trách nhiệm pháp lí và minh bạch", "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Nhóm vấn đề về trách nhiệm pháp lí và minh bạch</h4>\n<p class=\"lesson-p\" style=\"display:none\">"),
        ("<p class=\"lesson-p\" style=\"display:none\"></p>\n", ""),
        ("trách nhiệm giai trình và tính minh bạch", "trách nhiệm giải trình và tính minh bạch"),
        ("<p class=\"lesson-p\">BÁC SI AI</p>\n", ""),
        ("thường hoạt động như một \"hộp đen\".</p>\n<p class=\"lesson-p\">Ahiển chùng la không rô vì sao chùng lại làm như vậy. Ví dụ, nêu một ứng dụng</p>", "thường hoạt động như một \"hộp đen\", khiến chúng ta không rõ vì sao chúng lại làm như vậy. Ví dụ, nếu một ứng dụng</p>"),
        (
            "không hiểu vì sao minh lại Arư điểm đo hay vì sao một câu trẻ lời cụ thể bị đành giá là sai. Diều này gây Nho khân trong việc kiểm tra tinh công bằng, phát hiện sai sót và xây dựng niềm In Vào hệ thống AI.",
            "không hiểu vì sao mình lại được điểm đó hay vì sao một câu trả lời cụ thể bị đánh giá là sai. Điều này gây khó khăn trong việc kiểm tra tính công bằng, phát hiện sai sót và xây dựng niềm tin vào hệ thống AI."
        ),
        (
            "c) Nhòm vấn đề về tác động đến xã hội và con người Gồm các vấn đề như thiên vị, ảnh hương việc làm, giá mạo (deepfake) ve quyền lựr chủ - thể hiện những ảnh hưởng rộng lớn của AI đến các giá trị xã hội và phảm gia con người.",
            "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Nhóm vấn đề về tác động đến xã hội và con người</h4>\n<p class=\"lesson-p\">Gồm các vấn đề như thiên vị, ảnh hưởng việc làm, giả mạo (deepfake) và quyền tự chủ - thể hiện những ảnh hưởng rộng lớn của AI đến các giá trị xã hội và phẩm giá con người."
        ),
        ("học từ dữ liệu chúng dược</p>\n<p class=\"lesson-p\">huân luyện.", "học từ dữ liệu chúng được</p>\n<p class=\"lesson-p\">huấn luyện."),
        ("(vi du chi chừa ảnh báo sĩ nam và y tá nữ). AI sẽ vô tinh tải tạo lại những thiên vị đó.", "(ví dụ chỉ chứa ảnh bác sĩ nam và y tá nữ), AI sẽ vô tình tái tạo lại những thiên vị đó."),
        ("gợi y việc làm thiên về một giới tính/chùng tộc nhật định.", "gợi ý việc làm thiên về một giới tính/chủng tộc nhất định."),
        ("phân biệt đôi xử dưa trên giới tính, chúng tộc, tôn giáo và cùng cố các thiên vị xã hội.", "phân biệt đối xử dựa trên giới tính, chủng tộc, tôn giáo và củng cố các thiên vị xã hội."),
        ("Hình 6.2. Thiên vị dữ liệu trong A/\n(mô lá bác sĩ luôn là nam và y tá lưôn là nữ)", "Hình 6.2. Thiên vị dữ liệu trong AI\n(mô tả bác sĩ luôn là nam và y tá luôn là nữ)"),
        ("giòng như</li>", "giống như</li>"),
        (
            "nhưng thực chát là giả mạo, khiến việc phân biệt thật - giả rât khó. Ví dụ, có thể xuất hiện video người nói tiếng phát ngôn điêu chưa từng nói, hoặc ghi ảm giả mạo giong người thân đề lừa đảo. Điều này dẫn đến lan truyền thông tin sai lệch, tồn hại danh dự và mát niềm tin vào thông tin trực tuyến.",
            "nhưng thực chất là giả mạo, khiến việc phân biệt thật - giả rất khó. Ví dụ, có thể xuất hiện video người nổi tiếng phát ngôn điều chưa từng nói, hoặc ghi âm giả mạo giọng người thân để lừa đảo. Điều này dẫn đến lan truyền thông tin sai lệch, tổn hại danh dự và mất niềm tin vào thông tin trực tuyến."
        ),
        ("Hình 6.3. Hình ảnh người nồi tiếng bị ghép", "Hình 6.3. Hình ảnh người nổi tiếng bị ghép"),
        (
            "AI hoặc đề AI đưa ra mọi quyết định thay thể con người có thể làm suy yếu khả năng suy nghĩ độc lập và giá trị bàn thân. Ví dụ, nếu em hoàn toàn dựa vào AI để làm bài tập về nhà, chọn ngành học, hay thậm chí đưa ra lời khuyên về các mỗi quan hệ cá nhân, em có thể dần mất đi khà năng tư duy phân biện và giải quyết vấn đề. Hậu quả là chúng ta có thể trờ nên quá phụ thuộc vào công nghệ, làm giảm đi kĩ năng và quyền tự chủ của chinh mình.",
            "AI hoặc để AI đưa ra mọi quyết định thay thế con người có thể làm suy yếu khả năng suy nghĩ độc lập và giá trị bản thân. Ví dụ, nếu em hoàn toàn dựa vào AI để làm bài tập về nhà, chọn ngành học, hay thậm chí đưa ra lời khuyên về các mối quan hệ cá nhân, em có thể dần mất đi khả năng tư duy phản biện và giải quyết vấn đề. Hậu quả là chúng ta có thể trở nên quá phụ thuộc vào công nghệ, làm giảm đi kĩ năng và quyền tự chủ của chính mình."
        ),
        (
            "\n\nd) Sự liên kết và tính phức tạp giữa các vấn đề đạo đức</p>",
            "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">d)</span> Sự liên kết và tính phức tạp giữa các vấn đề đạo đức</h4>"
        ),
        ("liên kết chặt chế với nhau,", "liên kết chặt chẽ với nhau,"),
        ("sự thiếu mình bạch", "sự thiếu minh bạch"),
        ("thông tin già mạo", "thông tin giả mạo"),
        ("làm tồn hại đến danh dự", "làm tổn hại đến danh dự"),
        ("quyền riêng tư của cả nhân.", "quyền riêng tư của cá nhân."),
        (
            "1: tạo sinh đặt ra những vấn đề đạo đức quan trọng trên ba i hia canh: an toàn thông tin cá nhân (như quyền riêng tư và ràc mật), trách nhiệm pháp lí và minh bạch (như bản quyền và giải trình), cùng với tác động xã hội và con người (như thiên vị hay thay thế việc làm). Việc phát triển và sử dụng Ai tạo sinh càn được định hướng rõ ràng để bào vệ con người và phục vụ en ron chung.",
            "AI tạo sinh đặt ra những vấn đề đạo đức quan trọng trên ba khía cạnh: an toàn thông tin cá nhân (như quyền riêng tư và bảo mật), trách nhiệm pháp lí và minh bạch (như bản quyền và giải trình), cùng với tác động xã hội và con người (như thiên vị hay thay thế việc làm). Việc phát triển và sử dụng AI tạo sinh cần được định hướng rõ ràng để bảo vệ con người và phục vụ lợi ích chung."
        ),
        (
            "<p class=\"lesson-p\">2. Vản đề môi trường và các giải pháp trong việc huấn luyện, vận hành cac mô hình lớn về AI tạo sinh a) Văn đề môi trường trong AI tạo sinh Việc phát triển và vận hành</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Vấn đề môi trường và các giải pháp trong việc huấn luyện, vận hành các mô hình lớn về AI tạo sinh</h3>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Vấn đề môi trường trong AI tạo sinh</h4>\n<p class=\"lesson-p\">Việc phát triển và vận hành</p>"
        ),
        (
            "Các mô hình AI tạo sinh tiêu tôn lượng lớn điện năng cho</p>\n<p class=\"lesson-p\">quả trình huản luyện và duy trì máy chủ, góp phần làm gìa tàng phát thải carbon. Ngoài</p>\n<p class=\"lesson-p\">ra. hệ thống làm mát trung tàm dữ liệu sử dụng nhiều</p>\n<p class=\"lesson-p\">nước và tạo ra rác thải điện từ.",
            "Các mô hình AI tạo sinh tiêu tốn lượng lớn điện năng cho quá trình huấn luyện và duy trì máy chủ, góp phần làm gia tăng phát thải carbon. Ngoài ra, hệ thống làm mát trung tâm dữ liệu sử dụng nhiều nước và tạo ra rác thải điện tử."
        ),
        (
            "<figcaption class=\"figure-caption\">Hình 6.4. Một trung tàm dữ liệu lòn tỏa nhiệt\ntiêu tốn điện và nước, tạo ra khí thải làm thiên nhiên</figcaption>\n                        </div>\n                    </figure>\n                    \n<p class=\"lesson-p\">Dị anh hướng</p>",
            "<figcaption class=\"figure-caption\">Hình 6.4. Một trung tâm dữ liệu lớn tỏa nhiệt, tiêu tốn điện và nước, tạo ra khí thải làm thiên nhiên bị ảnh hưởng</figcaption>\n                        </div>\n                    </figure>"
        ),
        (
            "<p class=\"lesson-p\">b) Một số giải pháp cho vấn đề môi trường trong AI tạo sinh Đề giảm thiểu",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Một số giải pháp cho vấn đề môi trường trong AI tạo sinh</h4>\n<p class=\"lesson-p\">Để giảm thiểu"
        ),
        ("lượng tinh toán cần thiết.", "lượng tính toán cần thiết."),
        ("Chuyến đổi các trung tâm dữ liệu", "Chuyển đổi các trung tâm dữ liệu"),
        ("năng lượng mặt trời, gió, thuỳ điện.", "năng lượng mặt trời, gió, thuỷ điện."),
        ("<li>Nghiên cửu AI xanh:", "<li>Nghiên cứu AI xanh:"),
        ("đỏi hòi nhiều nước", "đòi hỏi nhiều nước"),
        ("giảm thiếu những tác động náy,", "giảm thiểu những tác động này,"),
        ("hoạt động hiệu quả họn,", "hoạt động hiệu quả hơn,"),
        ("đảy mạnh nghiên cứu", "đẩy mạnh nghiên cứu"),
        ("2. Việc AI tai tạo thiên vị", "2. Việc AI tái tạo thiên vị"),
        (
            "<p class=\"lesson-p\">: VẬN DỤNG</p>",
            "</div></section>\n\n            <section class=\"lesson-card apply-section\" id=\"sec-vận-dụng\">\n                <div class=\"section-badge-header\">\n                    <span class=\"sec-icon\">🚀</span>\n                    <h2 class=\"section-title\">VẬN DỤNG</h2>\n                </div>\n                <div class=\"section-body\">"
        ),
        (
            "Em hãy tường tượng minh là một nhà phát triển AI. Khi tạo ra một công cụ AI tạo Sinh mới (ví dụ: cộng cụ tạo truyện ngắn tự động), em sẽ làm gì đề đảm bảo các vấn đề đạo đức về thiên vị và công bằng, về thông tin sai lệch được giảm thiêu?",
            "Em hãy tưởng tượng mình là một nhà phát triển AI. Khi tạo ra một công cụ AI tạo sinh mới (ví dụ: công cụ tạo truyện ngắn tự động), em sẽ làm gì để đảm bảo các vấn đề đạo đức về thiên vị và công bằng, về thông tin sai lệch được giảm thiểu?"
        ),
    ],
    "bai-7-ai-mo-ra-co-hoi-va-thach-thuc-cho-cac-nganh-nghe": [
        (
"""<p class="lesson-p">BÀI 7: AI MƠ RA CƠ HỘI VÀ</p>
<p class="lesson-p">HÁCH THỰC CHO CÁC NGÀNH NGHỀ</p>
<p class="lesson-p">MUC TIEU</p>
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<p class="lesson-p">• Chi ra được ảnh hưởng hai một của AI tạo sinh đến việc làm.</p>
<p class="lesson-p">• Trình bày được các kĩ năng cần có để thích ứng với thời đại A1.</p>""",
"""            <section class="lesson-card target-section" id="sec-mục-tiêu">
                <div class="section-badge-header">
                    <span class="sec-icon">🎯</span>
                    <h2 class="section-title">MỤC TIÊU</h2>
                </div>
                <div class="section-body">
            
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<ul class="lesson-bullet-list">
<li>Chỉ ra được ảnh hưởng hai mặt của AI tạo sinh đến việc làm.</li>
<li>Trình bày được các kĩ năng cần có để thích ứng với thời đại AI.</li>
</ul>
</div></section>"""
        ),
        (
            "<p class=\"lesson-p\">Ở vp 9. cứt em đã tìm hiểu vỏ các nhóm nghề trong lĩnh vực Tin học như Khoa học máy tính. Tìn học ứng dụng, cũng như những công việc cụ thể như phát triển phần mềm hay quản trị hệ thống. Giờ đây khi em đùng tròc nguồng aa chun</p>\n<p class=\"lesson-p\">ngành chọn nghé, các câu hỏi đặt ra là:</p>",
            "<p class=\"lesson-p\">Ở lớp 9, các em đã tìm hiểu về các nhóm nghề trong lĩnh vực Tin học như Khoa học máy tính, Tin học ứng dụng, cũng như những công việc cụ thể như phát triển phần mềm hay quản trị hệ thống. Giờ đây khi em đứng trước ngưỡng cửa chọn ngành, chọn nghề, các câu hỏi đặt ra là:</p>"
        ),
        ("1. Sự phat triển vượt bác của AI,", "1. Sự phát triển vượt bậc của AI,"),
        ("những kĩ nàng em đang có đã đù để thich nghi với thế giui nghe nghitp dó chura?", "những kĩ năng em đang có đã đủ để thích nghi với thế giới nghề nghiệp đó chưa?"),
        ("<p class=\"lesson-p\">AI Bồ tg AI tha</p>\n", ""),
        ("<p class=\"lesson-p\">1. Anh hưởng hai mặt của AI đến việc làm</p>", "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Ảnh hưởng hai mặt của AI đến việc làm</h3>"),
        ("tự động hoa các</p>\n<p class=\"lesson-p\">tác vụ lặp lại và mở ra những cơ hội mỏi, tàng cường khả năng làm việc của con người.\n\nđồng thời tạo ra những ngành nghề hoàn toàn mới.\n\nHình 7.1. H sin dt KANd KN</p>\n<p class=\"lesson-p\">chọn ngành trong thời (ại AI</p>", "tự động hoá các tác vụ lặp lại và mở ra những cơ hội mới, tăng cường khả năng làm việc của con người, đồng thời tạo ra những ngành nghề hoàn toàn mới.</p>" + make_figure_box("Hình 7.1. Học sinh băn khoăn khi chọn ngành trong thời đại AI")),
        ("li đắc lực\" giúp con người làm việc hiệu quá,", "lí đắc lực\" giúp con người làm việc hiệu quả,"),
        ("giúp chần đoán nhanh và chính xác, để họ có nhiều thời gian hơn cho việc tư vân, chăm sóc bệnh nhân.", "giúp chẩn đoán nhanh và chính xác, để họ có nhiều thời gian hơn cho việc tư vấn, chăm sóc bệnh nhân."),
        ("tạo ra hàng trăm ý tưởng pháo</p>\n<p class=\"lesson-p\">thảo trong phút chốc, cho phép nhà thiết kê", "tạo ra hàng trăm ý tưởng phác</p>\n<p class=\"lesson-p\">thảo trong phút chốc, cho phép nhà thiết kế"),
        ("trực tiếp tạo rạ những vai trò,", "trực tiếp tạo ra những vai trò,"),
        ("trên thị trương lao động. Những công việc này đỏi hỏi sự hiểu biết sâu sắc về cả công nghệ và con người, mở ra một thể giới đầy tiềm năng.", "trên thị trường lao động. Những công việc này đòi hỏi sự hiểu biết sâu sắc về cả công nghệ và con người, mở ra một thế giới đầy tiềm năng."),
        ("+ Ki sư prompt", "+ Kĩ sư prompt"),
        ("(Al-Powered Content", "(AI-Powered Content"),
        ("học hiệu qua hơn", "học hiệu quả hơn"),
        (
            "+ Phát triển khả năng sáng tạo: Với sự hỗ try dua AI, em co thé lu Gong hoa</p>\n<p class=\"lesson-p\">các lác vụ lập lại vá tập trung vào việc đưa ra các ý tưởng đột phá, sáng sạo.\n\ngiái quyết những vẫn để phức lập hơn.",
            "+ Phát triển khả năng sáng tạo: Với sự hỗ trợ của AI, em có thể tự động hoá</p>\n<p class=\"lesson-p\">các tác vụ lặp lại và tập trung vào việc đưa ra các ý tưởng đột phá, sáng tạo, giải quyết những vấn đề phức tạp hơn."
        ),
        (
            "+ Yêu cầu kì năng mới: Nhiêu ngánh nghê sả đôi hói kì nóng AI và cùng ngồ!</p>\n<p class=\"lesson-p\">số, buộc em phải chủ động học hói để thich nghi.</p>\n<p class=\"lesson-p\">+ Ap lưc học hói liên tuc: AI thay đổi rất nhanh, soi hỏi sm shản kon càp rinh</p>\n<p class=\"lesson-p\">kiến thức và kì náng mới.</p>\n<p class=\"lesson-p\">!</p>\n<p class=\"lesson-p\">Thách thức Cohei</p>",
            "+ Yêu cầu kĩ năng mới: Nhiều ngành nghề sẽ đòi hỏi kĩ năng AI và công nghệ</p>\n<p class=\"lesson-p\">số, buộc em phải chủ động học hỏi để thích nghi.</p>\n<p class=\"lesson-p\">+ Áp lực học hỏi liên tục: AI thay đổi rất nhanh, đòi hỏi em phải luôn cập nhật</p>\n<p class=\"lesson-p\">kiến thức và kĩ năng mới.</p>"
        ),
        ("thách thức và co hội đối với học sinh", "thách thức và cơ hội đối với học sinh"),
        ("<p class=\"lesson-p\">Tư duy linh hoạt Cộng đồng</p>\n<p class=\"lesson-p\">AI</p>\n<p class=\"lesson-p\">Học AI Dự án ngoại khoá</p>\n", ""),
        ("Hình 7.3: Lộ trình chuẩn bị với bồn cột mốc chính", "Hình 7.3. Lộ trình chuẩn bị với bốn cột mốc chính"),
        ("Để tên u co ht vit veroe gua thách thưc của thời đại AI, em cần chủ động chen di cho minh kieh thur: vit ki nàng về AI", "Để tận dụng cơ hội và vượt qua thách thức của thời đại AI, em cần chủ động chuẩn bị cho mình kiến thức và kĩ năng về AI:"),
        ("<li>• ", "<li>"),
        ("<p class=\"lesson-p\">Công việc mới</p>\n<p class=\"lesson-p\">Tự động hoa</p>\n<p class=\"lesson-p\">Tàng cường</p>\n", ""),
        ("Hình 7.4, AI và nghề nghiệp", "Hình 7.4. AI và nghề nghiệp"),
        (
            "tự động hóa công việc lập lại. tàng cường khả năng của con người và tạo việc làm mới, điều nảy mang lại thách thức về kĩ năng, nguy có tụt hậu nhưng cùng là Cơ hội nắng cao hiệu suất và mờ ra nghề nghiệp mới. Em cần đầu tự học tập và phát triển bản thân đề thích ứng.",
            "tự động hóa công việc lặp lại, tăng cường khả năng của con người và tạo việc làm mới, điều này mang lại thách thức về kĩ năng, nguy cơ tụt hậu nhưng cũng là cơ hội nâng cao hiệu suất và mở ra nghề nghiệp mới. Em cần đầu tư học tập và phát triển bản thân để thích ứng."
        ),
        ("<p class=\"lesson-p\">Camscaner 56</p>\n", ""),
        (
            "<p class=\"lesson-p\">2. Kĩ năng thích ứng trong thời đại AI Trong bổi cảnh AI phát triển không ngừng, việc trang bị những kĩ năng phù hợp là chia khoá đề mỗi cá nhân",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Kĩ năng thích ứng trong thời đại AI</h3>\n<p class=\"lesson-p\">Trong bối cảnh AI phát triển không ngừng, việc trang bị những kĩ năng phù hợp là chìa khoá để mỗi cá nhân"
        ),
        (
"""<p class="lesson-p">Prompt</p>
<p class="lesson-p">Al</p>
<p class="lesson-p">Al Tư duy phản biện Kĩ năng Thời đại Ai</p>
<p class="lesson-p">Trí tuệ cảm xúc Sáng tạo</p>
<p class="lesson-p">Giao tiếp</p>""",
            ""
        ),
        ("* Sử dụng công cụ AI:", "+ Sử dụng công cụ AI:"),
        ("AI tóm tắt bài giàng,", "AI tóm tắt bài giảng,"),
        ("Đây là kĩ năng cục kì quan trọng. Nó giùp", "Đây là kĩ năng cực kì quan trọng. Nó giúp"),
        ("Những kĩ năng này khỏ bị AI thay thể", "Những kĩ năng này khó bị AI thay thế"),
        ("đánh giá thông tin, đặt cầu hòi cho</p>\n<p class=\"lesson-p\">những gì AI tạo ra, không tin tuyệt đổi", "đánh giá thông tin, đặt câu hỏi cho</p>\n<p class=\"lesson-p\">những gì AI tạo ra, không tin tuyệt đối"),
        ("+ Sáng tạo: Khả nặng đưa ra", "+ Sáng tạo: Khả năng đưa ra"),
        (
            "* Giao tiếp và hợp tác: Khả năng làm việc nhỏm, trao đổi thông tín hiệu quả với đồng nghiệp, bạn bè và thậm chi cả việc giao tiếp với các hệ thống AI.\n\n+ Tri tuệ cảm xúc:",
            "+ Giao tiếp và hợp tác: Khả năng làm việc nhóm, trao đổi thông tin hiệu quả với đồng nghiệp, bạn bè và thậm chí cả việc giao tiếp với các hệ thống AI.</p>\n<p class=\"lesson-p\">+ Trí tuệ cảm xúc:"
        ),
        ("liên quan đền con người.", "liên quan đến con người."),
        ("Khả năng đổi mặt và tìm ra giải pháp", "Khả năng đối mặt và tìm ra giải pháp"),
        ("chưa thể tự xứ lí.", "chưa thể tự xử lí."),
        (
            "Đế thích nghi với thời đại AI, các kĩ năng thiết yêu bao gồm: Ki năng AI (biết sử dụng và giao tiếp hiệu quả qua prompt) và các kĩ năng mềm (tư duy phản biện, sáng tạo, giao tiếp, trí tuệ cảm xúc, giải quyết vấn đề). Đây là những lợi thế cạnh tranh mà AI khó thay thể.",
            "Để thích nghi với thời đại AI, các kĩ năng thiết yếu bao gồm: Kĩ năng AI (biết sử dụng và giao tiếp hiệu quả qua prompt) và các kĩ năng mềm (tư duy phản biện, sáng tạo, giao tiếp, trí tuệ cảm xúc, giải quyết vấn đề). Đây là những lợi thế cạnh tranh mà AI khó thay thế."
        ),
        ("A. Ki nang sao chép dữ liệu nhanh.", "A. Kĩ năng sao chép dữ liệu nhanh."),
        ("ngày càng quan trong khi làm việc với AI?", "ngày càng quan trọng khi làm việc với AI?"),
    ],
    "bai-8-quyen-con-nguoi-trong-ki-nguyen-ai": [
        (
"""<p class="lesson-p">BÃI 8: QUYỀN CON NGƯỜI</p>
<p class="lesson-p">TRONG KÌ NGUYÊN AI</p>
<p class="lesson-p">MỤC TIEU</p>
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<p class="lesson-p">• Giải thích được vì sao sự phát triễn của AI có khả năng ảnh hưởng đến các quyền cơ bản của con người.</p>
<p class="lesson-p">• Trình bày được một số hành động và giải pháp cụ thể để bảo vệ quyền con người trong kỉ nguyên AI.</p>""",
"""            <section class="lesson-card target-section" id="sec-mục-tiêu">
                <div class="section-badge-header">
                    <span class="sec-icon">🎯</span>
                    <h2 class="section-title">MỤC TIÊU</h2>
                </div>
                <div class="section-body">
            
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<ul class="lesson-bullet-list">
<li>Giải thích được vì sao sự phát triển của AI có khả năng ảnh hưởng đến các quyền cơ bản của con người.</li>
<li>Trình bày được một số hành động và giải pháp cụ thể để bảo vệ quyền con người trong kỉ nguyên AI.</li>
</ul>
</div></section>"""
        ),
        ("hiểu rõ hơn về sức khoẻ của minh.", "hiểu rõ hơn về sức khoẻ của mình."),
        ("Họ sử dụng AI đế phân tích", "Họ sử dụng AI để phân tích"),
        ("Khi AI \"chạm\" đên Quyền con người", "Khi AI \"chạm\" đến Quyền con người"),
        ("hiện diện trong lừng khía cạnh", "hiện diện trong từng khía cạnh"),
        ("Quyên riêng tư và bảo mật dữ liệu", "Quyền riêng tư và bảo mật dữ liệu"),
        ("thông tin cá nhân của chính minh,", "thông tin cá nhân của chính mình,"),
        ("Nguyên nhân cốt lõi đến tử việc AI", "Nguyên nhân cốt lõi đến từ việc AI"),
        ("cả các môi quan hệ của em.", "cả các mối quan hệ của em."),
        ("bắt nạt, bội nhọ danh dự", "bắt nạt, bôi nhọ danh dự"),
        (
            "<p class=\"lesson-p\">c) Quyền được hiểu biết thông tin đầy đủ, minh bạch Đây là quyền được tiếp cận",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Quyền được hiểu biết thông tin đầy đủ, minh bạch</h4>\n<p class=\"lesson-p\">Đây là quyền được tiếp cận"
        ),
        ("xem các nội dung ùng hộ quan điếm nào đó,", "xem các nội dung ủng hộ quan điểm nào đó,"),
        ("đông thời hạ thấp", "đồng thời hạ thấp"),
        ("mất đi khả năng đổi thoại một cách", "mất đi khả năng đối thoại một cách"),
        ("dựa trên các đặc điếm cá nhân", "dựa trên các đặc điểm cá nhân"),
        ("Lí do là vì AI học hồi từ dữ liệu", "Lí do là vì AI học hỏi từ dữ liệu"),
        ("Nếu dữ liệu lịch sử cho thây các vị trí", "Nếu dữ liệu lịch sử cho thấy các vị trí"),
        ("giới hạn Quyền được hiếu biết thông tin", "giới hạn Quyền được hiểu biết thông tin"),
        ("bảo vệ quyền con người trong kì nguyên AI", "bảo vệ quyền con người trong kỉ nguyên AI"),
        ("AI có thể ành hưởng đến các quyền", "AI có thể ảnh hưởng đến các quyền"),
        ("Bảo vệ quyền con người trong kì nguyên A</h3>", "Bảo vệ quyền con người trong kỉ nguyên AI</h3>"),
        ("Một ứng dụng chỉnh sửa ành có thực sự", "Một ứng dụng chỉnh sửa ảnh có thực sự"),
        ("vào danh bạ và vị trí của minh không?", "vào danh bạ và vị trí của mình không?"),
        ("+ Hãy rèn luyện tự duy phản biện", "+ Hãy rèn luyện tư duy phản biện"),
        ("+ Hãy cô gắng theo dõi", "+ Hãy cố gắng theo dõi"),
        ("<li>Bào vệ Quyền được đối xử công bằng:", "<li>Bảo vệ Quyền được đối xử công bằng:"),
        ("bảo vệ Quyền được đàm bảo an toán:", "bảo vệ Quyền được đảm bảo an toàn:"),
        ("về các vấn đề như tn giả</p>\n<p class=\"lesson-p\">hay bắt nạt trên mạng. Việc củng nhau nâng cao nhận thức và chia sẻ cách phòng tránh chính là hành động để bảo vệ lắn nhau.", "về các vấn đề như tin giả</p>\n<p class=\"lesson-p\">hay bắt nạt trên mạng. Việc cùng nhau nâng cao nhận thức và chia sẻ cách phòng tránh chính là hành động để bảo vệ lẫn nhau."),
        ("để thúc đấy Quyền riêng tư", "để thúc đẩy Quyền riêng tư"),
        ("như xày dụng một bộ quy tắc úng xử trên mạng xã hội cho cả lớp hoặc thiết kế ấn phẩm truyền thông để giải thích về rúi ro.\n\nnhững mặt trái của AI", "như xây dựng một bộ quy tắc ứng xử trên mạng xã hội cho cả lớp hoặc thiết kế ấn phẩm truyền thông để giải thích về rủi ro, những mặt trái của AI"),
        ("cho ra kết quả rập khôn).\n\ncác nhà phát triển", "cho ra kết quả rập khuôn), các nhà phát triển"),
        ("hay đề gặp gỡ, trao đối công việc", "hay để gặp gỡ, trao đổi công việc"),
        ("Hệ thống AI này đã vì phạm Quyền", "Hệ thống AI này đã vi phạm Quyền"),
    ],
    "bai-9-phat-trien-ai-co-trach-nhiem": [
        ("<p class=\"lesson-p\">BÃI 9. PHÁT TRIỂN AI</p>\n<p class=\"lesson-p\">CÓ TRÁCH NHIÊM</p>\n", ""),
        ("Các công cụ A| ngày càng thế hiện", "Các công cụ AI ngày càng thể hiện"),
        ("chính sức mạnh này cũng tiềm ấn nhiều rủi ro.", "chính sức mạnh này cũng tiềm ẩn nhiều rủi ro."),
        ("những phiên bản không mong muốn X hoặc gây hại?", "những phiên bản không mong muốn hoặc gây hại?"),
        ("<figcaption class=\"figure-caption\">Hình 9.1. Cảnh báo sự thiên Vị trong việc</figcaption>", "<figcaption class=\"figure-caption\">Hình 9.1. Cảnh báo sự thiên vị trong việc đưa ra quyết định của AI</figcaption>"),
        ("<p class=\"lesson-p\">đưa ra quyết định của AI</p>\n", ""),
        (
            "<p class=\"lesson-p\">1. Các nguyên tắc phát triển AI có trách nhiệm Để đảm bảo AI phục vụ con người một cách tốt đẹp và giảm thiếu rủi ro, các chuyên gia",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Các nguyên tắc phát triển AI có trách nhiệm</h3>\n<p class=\"lesson-p\">Để đảm bảo AI phục vụ con người một cách tốt đẹp và giảm thiểu rủi ro, các chuyên gia"
        ),
        (
"""<p class="lesson-p">Công báng</p>
<p class="lesson-p">Trách nhiệm</p>
<p class="lesson-p">AI CÓ TRÁCH</p>
<p class="lesson-p">Giám sát</p>
<p class="lesson-p">An toàn</p>
<p class="lesson-p">NHIỆM</p>
<p class="lesson-p">Minh bạch Riêng tư</p>
<p class="lesson-p">Đáng tin</p>
<p class="lesson-p">cạy</p>""",
            ""
        ),
        (
            "<p class=\"lesson-p\">Có thể chia các nguyên tắc phát triển AI có trách nhiệm thành hai nhóm chính:\n\na) Nhóm 1. Nguyên tắc liên quan đến kĩ thuật và hệ thống</p>",
            "<p class=\"lesson-p\">Có thể chia các nguyên tắc phát triển AI có trách nhiệm thành hai nhóm chính:</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Nhóm 1. Nguyên tắc liên quan đến kĩ thuật và hệ thống</h4>"
        ),
        ("được thiết kế, vận hành và kiếm tra,", "được thiết kế, vận hành và kiểm tra,"),
        ("phải đảm bảo an toàn tuyệt đôi,", "phải đảm bảo an toàn tuyệt đối,"),
        (
            "<p class=\"lesson-p\">Bao vệ quyền riêng tư: AI thường xử lí rất nhiều dữ liệu cá nhân. Do đỏ, việc thu thập, lưu trữ và sử dụng dữ liệu này phải được thực hiện một cách cần trọng tôn trọng quyền riêng tư của người dùng. Ví dụ, một ứng dụng AI phân tích thói quen học tập của em không được chia sẻ thông tin cá nhân của em cho bên thư ba mà không có sự đồng ý.",
            "<p class=\"lesson-p\">- Bảo vệ quyền riêng tư: AI thường xử lí rất nhiều dữ liệu cá nhân. Do đó, việc thu thập, lưu trữ và sử dụng dữ liệu này phải được thực hiện một cách cẩn trọng, tôn trọng quyền riêng tư của người dùng. Ví dụ, một ứng dụng AI phân tích thói quen học tập của em không được chia sẻ thông tin cá nhân của em cho bên thứ ba mà không có sự đồng ý."
        ),
        ("thông tin rõ ràng vê cách AI hoạt động", "thông tin rõ ràng về cách AI hoạt động"),
        ("lại gợi ý những khoa học đó", "lại gợi ý những khóa học đó"),
        ("không thiên vị dựa trên chùng tộc,", "không thiên vị dựa trên chủng tộc,"),
        ("cơ chế để người bị ảnh hướng có thể khiếu nại", "cơ chế để người bị ảnh hưởng có thể khiếu nại"),
        ("phải luôn giữ vai trò kiếm soát cuối", "phải luôn giữ vai trò kiểm soát cuối"),
        ("(công bằng; trách nhiệm giái trình; giám sát của con người).", "(công bằng; trách nhiệm giải trình; giám sát của con người)."),
        (
            "<p class=\"lesson-p\">2. Khó khăn khi áp dụng các nguyên tắc phát triển AI có trách nhiệm vào thực tê Việc đưa các nguyên tắc",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Khó khăn khi áp dụng các nguyên tắc phát triển AI có trách nhiệm vào thực tế</h3>\n<p class=\"lesson-p\">Việc đưa các nguyên tắc"
        ),
        ("Ví dụ: \"Công băng\" nghĩa là gì", "Ví dụ: \"Công bằng\" nghĩa là gì"),
        ("<p class=\"lesson-p\">CÔNG BẮNG</p>\n", ""),
        ("<p class=\"lesson-p\">Al</p>\n<p class=\"lesson-p\">MINH BẠCH BẢO MẬT</p>\n", ""),
        ("<p class=\"lesson-p\">Hình 9.4. Cân bằng trong nguyên tắc 68</p>", "<p class=\"lesson-p\">Hình 9.4. Cân bằng trong nguyên tắc</p>"),
        ("xác định trách nhiệm giai trình</h4>", "xác định trách nhiệm giải trình</h4>"),
        ("thời gian, nguôn lực và chuyên môn.", "thời gian, nguồn lực và chuyên môn."),
        (
"""<p class="lesson-p">Cập nhật hên lục</p>
<p class="lesson-p">Thứ nghiệm</p>
<ul class="lesson-bullet-list">
<li>thực tế</li>
</ul>
<p class="lesson-p">Cộng đông</p>
<p class="lesson-p">học tập</p>
<p class="lesson-p">Sách và bảo chi</p>
<p class="lesson-p">Khóa học trực tuyến</p>""",
            ""
        ),
        ("Học lập liên tục là cần thiết vì công nghệ AI không ngừng phát triển, các thách thức đạo đức ngày càng phức tạp và đế xây", "Học tập liên tục là cần thiết vì công nghệ AI không ngừng phát triển, các thách thức đạo đức ngày càng phức tạp và để xây"),
        ("C. Minh bạch và giái trình được.", "C. Minh bạch và giải trình được."),
        ("<p class=\"lesson-p\">¿ Hãy giai thích tại sao việc cân bằng giữa nguyên tắc \"minh bạch\" và \"bào mật\"", "<p class=\"lesson-p\">3. Hãy giải thích tại sao việc cân bằng giữa nguyên tắc \"minh bạch\" và \"bảo mật\""),
        ("<p class=\"lesson-p\">1 Tại sao việc học tập liên tục lại quan trọng đối với các em khi AI đang phát triển nhanh chöng?</p>", "<p class=\"lesson-p\">4. Tại sao việc học tập liên tục lại quan trọng đối với các em khi AI đang phát triển nhanh chóng?</p>"),
        ("Em hãy tìm kiêm một ví dụ thực tế", "Em hãy tìm kiếm một ví dụ thực tế"),
        ("của người phát triển A1 có trách nhiệm.", "của người phát triển AI có trách nhiệm."),
        ("<p class=\"lesson-p\">TE TÚ HỌC MÀY</p>\n", ""),
    ],
    "bai-10-nguyen-li-co-ban-cua-hoc-may": [
        ("<p class=\"lesson-p\">BÃI 105 NGUYÊN LÍ CƠ BẢN</p>\n<p class=\"lesson-p\">CỦA HỌC MÁY</p>\n", ""),
        ("Minh An băn khoăn.</p>", "Minh An băn khoăn:</p>"),
        ("để dự đoán điểm thì</p>\n<p class=\"lesson-p\">THPT Quốc gia chính là một sản phẩm của Học máy. Vậy ứng dụng này đã học tử những dữ liệu nào", "để dự đoán điểm thi</p>\n<p class=\"lesson-p\">THPT Quốc gia chính là một sản phẩm của Học máy. Vậy ứng dụng này đã học từ những dữ liệu nào"),
        ("một tập dữ liệu lớn từ hăng</li>", "một tập dữ liệu lớn từ hàng</li>"),
        ("Điểm trung binh học ki", "Điểm trung bình học kì"),
        ("+ Điểm các bài thi thứ hoặc", "+ Điểm các bài thi thử hoặc"),
        ("<p class=\"lesson-p\">+ Điểm thi THPT Quốc gia thực tế của những học sinh đó</p>", "<p class=\"lesson-p\">+ Điểm thi THPT Quốc gia thực tế của những học sinh đó.</p>"),
        ("<li>Qua trinh học:", "<li>Quá trình học:"),
        ("các yêu tô đầu vào (như điểm trung bình học ki)", "các yếu tố đầu vào (như điểm trung bình học kì)"),
        ("từ</p>\n<p class=\"lesson-p\">8,0 trờ lên", "từ</p>\n<p class=\"lesson-p\">8,0 trở lên"),
        ("<li>Dự đoán cho dữ liệu mới.", "<li>Dự đoán cho dữ liệu mới:"),
        ("dự đoán điểm thì của bạn ấy", "dự đoán điểm thi của bạn ấy"),
        ("Ví dụ: Già sử dữ liệu", "Ví dụ: Giả sử dữ liệu"),
        ("thì ứng dụng sẽ dự đoàn điểm thi", "thì ứng dụng sẽ dự đoán điểm thi"),
        ("xem xét nhiều yếu tố khác (nhũ</p>", "xem xét nhiều yếu tố khác (như</p>"),
        (
"""<p class="lesson-p">Machine Learning</p>
<p class="lesson-p">Trediecte Exam scort</p>
<p class="lesson-p">6.5-</p>""",
            ""
        ),
        (
            "<p class=\"lesson-p\">2. Hai dạng bài toán Học máy cơ bản\n\na) Hồi quy (Regression)</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Hai dạng bài toán Học máy cơ bản</h3>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Hồi quy (Regression)</h4>"
        ),
        ("dựa lên vên giá trị đậu vào đã biết, như việc về một đường thắng hoặc đường", "dựa trên các giá trị đầu vào đã biết, như việc vẽ một đường thẳng hoặc đường"),
        ("<p class=\"lesson-p\">Ví dụ</p>\n<p class=\"lesson-p\">Ưng dụng</p>\n<p class=\"lesson-p\">Giải thich</p>", "<p class=\"lesson-p\">Ví dụ:</p>\n<p class=\"lesson-p\">Ứng dụng</p>\n<p class=\"lesson-p\">Giải thích</p>"),
        ("Phân tích điểm trung binh môn Toán, Lí, Hóa -+ Du đoán điểm thì THPT Quốc gia (Ví dụ: 8,26 là số cụ thể),", "Phân tích điểm trung bình môn Toán, Lí, Hóa → Dự đoán điểm thi THPT Quốc gia (Ví dụ: 8,26 là số cụ thể)."),
        ("Từ lượng mưa, địa hình sông Hông Dự đoán mực nước tũ tại Hà Nội.</p>\n<p class=\"lesson-p\">Dự bào 10 lụl</p>", "Từ lượng mưa, địa hình sông Hồng → Dự đoán mực nước lũ tại Hà Nội.</p>\n<p class=\"lesson-p\">Dự báo lũ lụt</p>"),
        (
"""<p class="lesson-p">Hồi quy: Dự đoán điểm thi dựa trên số giờ học</p>
<p class="lesson-p">Du liệu tlice</p>
<p class="lesson-p">Đường hồi quy 100</p>
<p class="lesson-p">Б 80</p>
<p class="lesson-p">Số giờ học</p>""",
            ""
        ),
        ("Hình 10.2, Hình ảnh bài toán Hồi quý: Dự đoán điểm thi dựa trên có giờ học", "Hình 10.2. Hình ảnh bài toán Hồi quy: Dự đoán điểm thi dựa trên số giờ học"),
        ("<p class=\"lesson-p\">Dụ đoàn trượt</p>", "<p class=\"lesson-p\">Dự đoán trượt</p>"),
        (
"""<p class="lesson-p">Phân loại: Đỗ và Trượt dựa trên điểm thi</p>
<p class="lesson-p">100 Trot Đó</p>
<p class="lesson-p">Ngưỡng đo = 60</p>
<p class="lesson-p">Điểm thì</p>
<p class="lesson-p">50 -</p>
<p class="lesson-p">2 4 8 Số giờ học</p>""",
            ""
        ),
        ("trong mô hình học và dy đoán</h3>", "trong mô hình học và dự đoán</h3>"),
        ("<p class=\"lesson-p\">2) Các yếu tố quyết định chất lượng dữ liệu</p>", "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Các yếu tố quyết định chất lượng dữ liệu</h4>"),
        ("Ba yếu tố chinh quyết định chất lượng dữ liệu là số lượng, sự đa dạng và tinh chính xác", "Ba yếu tố chính quyết định chất lượng dữ liệu là số lượng, sự đa dạng và tính chính xác"),
        ("dùng để huấn luyện mô hình A1.</p>", "dùng để huấn luyện mô hình AI.</p>"),
        ("+ Ảnh hường: Dữ liệu ít", "+ Ảnh hưởng: Dữ liệu ít"),
        ("dự đoán kém chính xác trên dữ liệu mới</p>", "dự đoán kém chính xác trên dữ liệu mới.</p>"),
        ("do thiêu dữ liệu bao quát - Sự đa dạng dữ liệu:</p>", "do thiếu dữ liệu bao quát.</p>\n<ul class=\"lesson-bullet-list\"><li>Sự đa dạng dữ liệu:</li></ul>"),
        ("+ Ánh hưởng: Dữ liệu thiếu đa dạng làm mô hình bị \"thiên vị theo dữ liệu", "+ Ảnh hưởng: Dữ liệu thiếu đa dạng làm mô hình bị \"thiên vị\" theo dữ liệu"),
        ("+ Ành hưởng: Dữ liệu lỗi", "+ Ảnh hưởng: Dữ liệu lỗi"),
        ("nhập nhằm (8 thành 80) hoặc thiểu</p>\n<p class=\"lesson-p\">30% điềm Tiếng Anh sẽ khiến mô hình học sai hoặc bò qua", "nhập nhầm (8 thành 80) hoặc thiếu</p>\n<p class=\"lesson-p\">30% điểm Tiếng Anh sẽ khiến mô hình học sai hoặc bỏ qua"),
        ("Quy trình xứ lí dữ liệu", "Quy trình xử lí dữ liệu"),
        ("Điểm HK//HKII,", "Điểm HKI/HKII,"),
        ("dùng để xây dụng mô hình dự</li>\n</ul>\n<p class=\"lesson-p\">đoán, tập kiếm tra (20%)", "dùng để xây dựng mô hình dự</li>\n</ul>\n<p class=\"lesson-p\">đoán, tập kiểm tra (20%)"),
        (
"""<p class="lesson-p">1. Thu thập dữ liệu</p>
<p class="lesson-p">2. Tiền xử lí dữ liệu</p>
<p class="lesson-p">3. Chia tập dữ liệu</p>
<p class="lesson-p">4. Huấn luyện mô hình</p>
<h3 class="subheading-h3"><span class="h3-num">5.</span> Đánh giá sai số</h3>
<p class="lesson-p">Kiếm tra hiệu suất va độ</p>
<p class="lesson-p">Gom nhạ! và lổng hợp da</p>
<p class="lesson-p">Làm sạch, chuyển đổi và</p>
<p class="lesson-p">Phan chia train halldation/test theo d</p>
<p class="lesson-p">Training mo hinh voi de</p>
<p class="lesson-p">liệu đã chuẩn bị</p>
<p class="lesson-p">chính xác của mô hình</p>
<p class="lesson-p">liệu từ nhiêu nguồn khác</p>
<p class="lesson-p">nhau</p>
<p class="lesson-p">chuẩn hoa do Bêu</p>
<p class="lesson-p">lộ phu hợp</p>
<p class="lesson-p">A Cánh béo:</p>
<p class="lesson-p">A Cánh báo:</p>
<p class="lesson-p">A Cánh bào:</p>
<p class="lesson-p">fl Motnc sai</p>
<p class="lesson-p">A Cánh báo:</p>
<ul class="lesson-bullet-list">
<li>Giá tr nuội</li>
</ul>
<p class="lesson-p">A Cảnh báo:</p>
<p class="lesson-p">E Overfitting</p>
<ul class="lesson-bullet-list">
<li>Bias cao</li>
</ul>
<p class="lesson-p">© Dữ liệu thiếu</p>
<p class="lesson-p">C] Outliers</p>
<p class="lesson-p">I2 Data leakage</p>
<p class="lesson-p">E Underfitting</p>
<p class="lesson-p">B Bảo mặt</p>
<ul class="lesson-bullet-list">
<li>) Định đang sai</li>
</ul>
<p class="lesson-p">4P 7T0 з0l</p>
<p class="lesson-p">C/ Chậm hội tụ</p>
<p class="lesson-p">E Kém tổng quát</p>
<ul class="lesson-bullet-list">
<li>Bản quyền</li>
</ul>
<p class="lesson-p">* Không cân bằng</p>
<p class="lesson-p">E3 Thiếu random</p>
<ul class="lesson-bullet-list">
<li>Thiếu RAM</li>
</ul>
<p class="lesson-p">4 Không ổn định</p>
<p class="lesson-p">G Chất lượng kóm</p>
<p class="lesson-p">E Qué it test</p>""",
            ""
        ),
        ("những trường hợp chưa từng thây.</p>", "những trường hợp chưa từng thấy.</p>"),
        ("không đủ để xây.\n\ndựng ứng dụng dự đoán điểm", "không đủ để xây dựng ứng dụng dự đoán điểm"),
        ("về vùng miên, môi trường học,", "về vùng miền, môi trường học,"),
    ],
    "bai-11-toi-uu-hoa-mo-hinh": [
        ("cách dự đoán của minh như thế nào?", "cách dự đoán của mình như thế nào?"),
        ("<p class=\"lesson-p\">Một thước đổ\" để biết dự đoán của AI \"lệch\" so với thực tế bao nhiêu. Thước</p>\n<p class=\"lesson-p\">áo này chinh là Hàm mất mát (Loss Function).</p>", "<ul class=\"lesson-bullet-list\"><li>Một \"thước đo\" để biết dự đoán của AI \"lệch\" so với thực tế bao nhiêu. Thước đo này chính là Hàm mất mát (Loss Function).</li></ul>"),
        ("Kĩ thuật giảm dân độ dốc", "Kĩ thuật giảm dần độ dốc"),
        ("AI dự đoàn (gọi là y.a) và điều thực sự xảy ra (gọi là yre).", "AI dự đoán (gọi là y_pred) và điều thực sự xảy ra (gọi là y_true)."),
        ("+ Ym.: Giá trị dự đoán", "+ y_pred: Giá trị dự đoán"),
        ("+ Yre: Giá trị thực tế", "+ y_true: Giá trị thực tế"),
        ("giá trị hàm mât mát cảng cao.</li>", "giá trị hàm mất mát càng cao.</li>"),
        ("+ Y nghĩa:", "+ Ý nghĩa:"),
        ("Nêu AI dự đoán 55 kg", "Nếu AI dự đoán 55 kg"),
        ("dự đoán điểm thi (y _pred và y lần lượt là kí hiệu điềm</p>\n<p class=\"lesson-p\">dự đoán và điểm thực) dựa trên số giờ ôn tập (hay giờ học) X theo công thức Y _pred = w * X + b", "dự đoán điểm thi (y_pred và y lần lượt là kí hiệu điểm</p>\n<p class=\"lesson-p\">dự đoán và điểm thực) dựa trên số giờ ôn tập (hay giờ học) X theo công thức y_pred = w * X + b"),
        (
            "<p class=\"lesson-p\">y_pred = w*X +b # AI đưa ra dự đoàn điểm thi</p>\n<p class=\"lesson-p\">error = Y_pred -y #Tinh sự sai lệch giữa dự đoán và thực tê loss = (error * 2). mean() # Tinh hàm mất màt (MSE)</p>\n<p class=\"lesson-p\">S1</p>",
            make_code_block("y_pred = w * X + b  # AI đưa ra dự đoán điểm thi\nerror = y_pred - y  # Tính sự sai lệch giữa dự đoán và thực tế\nloss = (error ** 2).mean()  # Tính hàm mất mát (MSE)")
        ),
        ("\n\nc) Mất mát trung bình</p>", "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Mất mát trung bình</h4>"),
        ("chúng ta không chỉ lính hàm mất mát", "chúng ta không chỉ tính hàm mất mát"),
        ("tính mất mát trung binh", "tính mất mát trung bình"),
        ("<span class=\"h3-num\">2.</span> Kì thuật giảm dân độ dốc</h3>", "<span class=\"h3-num\">2.</span> Kĩ thuật giảm dần độ dốc</h3>"),
        ("<span class=\"h4-letter\">a)</span> Y nghĩa</h4>", "<span class=\"h4-letter\">a)</span> Ý nghĩa</h4>"),
        ("từng bước nhỏ (biến Ir),", "từng bước nhỏ (biến lr),"),
        ("tham số Learning Rate (biến Ir trong công thức", "tham số Learning Rate (biến lr trong công thức"),
        ("Bước nhảy quá dải, có thể", "Bước nhảy quá dài, có thể"),
        ("dao động, không ốn định.</p>", "dao động, không ổn định.</p>"),
        ("số giờ học và điểm thị của</h4>", "số giờ học và điểm thi của</h4>"),
        (
            "<p class=\"lesson-p\">D) Xay dựng AI dự đoán: Sử dụng thuật toán giảm dân độ dồc đề tìm ra \"đường</p>\n<p class=\"lesson-p\">thằng\" dự đoán điểm thi tốt nhất.</p>",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Xây dựng AI dự đoán: Sử dụng thuật toán giảm dần độ dốc để tìm ra \"đường thẳng\" dự đoán điểm thi tốt nhất.</h4>"
        ),
        ("chạy đoạn mã sau đề tạo dữ liệu", "chạy đoạn mã sau để tạo dữ liệu"),
        (
"""                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">import pandas as pd. # Nhập thư viện pandas để làm việc với dữ liệu dạng bảng</code></pre>
                    </div>
                    
<p class="lesson-p">CSV_txt = "'"'hours, score 2,4 3,5 4,6 5,7 6,8 7,9 8,10" •.

open("study_data. csv", "w") .write(csv_txt) # Tạo và ghi nội dung vào file study_data.csv</p>""",
            BAI11_CODE_BLOCK1
        ),
        (
"""                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">import matplotlib. pyplot as plt # Nhập thư viện matplotlíb dé vẽ biểu đồ</code></pre>
                    </div>
                    

                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">import pandas as pd " Nhập thư viện pandas để làm việc với dữ liệu dạng bảng</code></pre>
                    </div>
                    
<p class="lesson-p">data • pd. read_csv("study_dato. (sv") # Dọc dữ liệu từ file CSV vào Dataframe X = data["hours"] values " lãy rột "lours" (số giở lọc) làm dừ liện đàu vào X (dạng mang</p>
<p class="lesson-p">питру) y = datal"scoro") values 1 Lãy cột "score" (điếm thí) làm dữ liệu đầu ra y (dạng máng numpy)</p>
<p class="lesson-p">plt.scatter(X, y, s-60) " Vẽ biểu đồ phân tán (scatter plot) với X (trục hoành) và y (trục</p>
<p class="lesson-p">(ung), 3.60 là kich lhor điểm plt-xlabel("Số giờ học") 4 Dặt tên cho trục hoành</p>
<p class="lesson-p">plt, ylabel("Điềm thi") 4 Đật tên cho trục tung plt-title( "Phân bố dữ liệu" ) # Hiển thị biểu đồ</p>
<p class="lesson-p">plt.show()</p>""",
            BAI11_CODE_BLOCK2
        ),
        (
"""<p class="lesson-p">Phân bố dữ liệu</p>
<p class="lesson-p">10 •</p>
<ul class="lesson-bullet-list">
<li></li>
</ul>
<p class="lesson-p">6-</p>
<ul class="lesson-bullet-list">
<li></li>
</ul>
<p class="lesson-p">4 .

•</p>
<p class="lesson-p">5 Số giờ học</p>""",
            ""
        ),
        ("<figcaption class=\"figure-caption\">Hình 11.1. Biều đồ phân tán (scatter plot),</figcaption>", "<figcaption class=\"figure-caption\">Hình 11.1. Biểu đồ phân tán (scatter plot), cho thấy điểm thi tăng theo số giờ học</figcaption>"),
        ("<p class=\"lesson-p\">cho thấy điểm thi tăng theo số giờ học</p>\n", ""),
        ("giảm dần độ dốc đề tìm đường", "giảm dần độ dốc để tìm đường"),
        ("điểm_dự_đoán = w* số_giờ_học + b.", "điểm_dự_đoán = w * số_giờ_học + b."),
        ("là các tham số má AI cần", "là các tham số mà AI cần"),
        ("(chạy thuật toán giảm dần độ dóc).", "(chạy thuật toán giảm dần độ dốc)."),
        ("bằng cách điều chinh w và b", "bằng cách điều chỉnh w và b"),
        ("<p class=\"lesson-p\">Python</p>\n", ""),
        (
"""                    <div class="code-block-wrapper">
                        <div class="code-header"><span>Python / Code</span><button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>
                        <pre><code class="language-python">import numpy as np</code></pre>
                    </div>
                    
<p class="lesson-p">det gradient_descent(X, y, Ir=0.01, epochs=1_000, verbose=False):</p>
<ul class="lesson-bullet-list">
<li>'"Trá vè (w, D, history_loss). X, y dêu là 1-D numpy array."..

v, b = 0.0, 0.0 = Khởi tạo ban Sau cho v và b n = len (X) loss _hist = [] = lu lại giá trị mát mát sau nôi làn học</li>
</ul>
<p class="lesson-p">for epoch in range (epochs):</p>
<p class="lesson-p">y_pred= W * X + b $ AI dua ra dự doán điểm thi</p>
<p class="lesson-p">loss = (error ** 2). mean () loss_hist.append(loss)</p>
<p class="lesson-p"># Tính hăn mất mát (PSE)</p>
<p class="lesson-p"># Tính toán hướng cần điều chinh (Gradient) để giảm mất mát » grad = (2 / n) * np.dot(X, error) b_ grad= (2 / n) * error-sum()</p>
<p class="lesson-p"># Cập nhật tham số w và b để giám hàm mát mát w -= Ir * w grad</p>
<p class="lesson-p">b -= Ir = b_grad</p>
<p class="lesson-p">if verbose and epoch % 100 = 0: # In ra để xem tiến trình học của AI</p>
<p class="lesson-p">print (f"epoch {epoch: >4}: loss = {loss: 4f}") return w, b, loss_hist</p>""",
            BAI11_CODE_BLOCK3
        ),
        (
"""<p class="lesson-p">w, b, loss_hist = gradient_descent(X, y, Ir=0.01, epochs=1_000, verbose=True) print (f"Đường hồi quy tối ưu: y = {w:.2f}*x + {b:.2f}")</p>""",
            BAI11_CODE_BLOCK4
        ),
        (
"""<p class="lesson-p">Python | plt. scatter (X, y, 9-60, label- "Dữ liệu thực" )</p>
<p class="lesson-p">plt.plot(X, w " X +b, color="red", label» "Dường hòi quy" ) " Vẽ đường dụ đoán của AI</p>
<p class="lesson-p">plt. xlabel( "Số giờ học" ) plt.ylabel( "Dlém thi" ) plt. title( "Dy đoán điền thi theo số giờ học" ) plt.legend() plt.show()</p>""",
            BAI11_CODE_BLOCK5
        ),
        (
            "<p class=\"lesson-p\">Các em sã thấy một biểu đề giống như Hình 11.2 (tã du nó sẽ đi gần qua các điểm Đường hôi quy màu đó chính là đường dự doan cua AI dữ liệu, cho thấy AI đã học được mối quan hệ giữa số giờ học và điểm thi.</p>\n<p class=\"lesson-p\">Dự đoán điểm thì theo số giờ học</p>\n<p class=\"lesson-p\">10 Dữ liệu thực</p>\n<p class=\"lesson-p\">Đường hồi quy</p>\n<p class=\"lesson-p\">Điểm thi</p>\n<p class=\"lesson-p\">2 3 4 5 , 6 7 8 Số giờ học</p>",
            "<p class=\"lesson-p\">Các em sẽ thấy một biểu đồ giống như Hình 11.2. Đường hồi quy màu đỏ chính là đường dự đoán của AI; nó sẽ đi gần qua các điểm dữ liệu, cho thấy AI đã học được mối quan hệ giữa số giờ học và điểm thi.</p>"
        ),
        ("giá trị tốc độ học Ir trong hàm", "giá trị tốc độ học lr trong hàm"),
        ("Thử Ir =", "Thử lr ="),
        ("Nếu Ir quá", "Nếu lr quá"),
        ("thế \"nhảy qua\"", "thể \"nhảy qua\""),
        (", Việc chọn một Ir phù hợp", "Việc chọn một lr phù hợp"),
        ("1.</span> Mục địch chính của hàm mất mát", "1.</span> Mục đích chính của hàm mất mát"),
        ("\n<p class=\"lesson-p\">CHỦ ĐẾ 5. DỰ ÂN AI AGENT</p>\n<p class=\"lesson-p\">Input</p>\n<p class=\"lesson-p\">AI Model</p>\n<p class=\"lesson-p\">AI Model</p>\n<p class=\"lesson-p\">API Tool</p>\n<p class=\"lesson-p\">Output</p>", ""),
    ],
    "bai-12-hinh-thanh-y-tuong-va-lap-ke-hoach": [
        ("<p class=\"lesson-p\">VÀ LẬP KÊ HOẠCH</p>\n", ""),
        ("đến việc tìm hiếu các công cụ AI", "đến việc tìm hiểu các công cụ AI"),
        ("em có nhận thấy vấn đề nào mả một ứng dụng AI", "em có nhận thấy vấn đề nào mà một ứng dụng AI"),
        (
            "<p class=\"lesson-p\">KHÁM PHẢ</p>",
            "</div></section>\n\n            <section class=\"lesson-card discovery-section\" id=\"sec-khám-phá\">\n                <div class=\"section-badge-header\">\n                    <span class=\"sec-icon\">🔍</span>\n                    <h2 class=\"section-title\">KHÁM PHÁ</h2>\n                </div>\n                <div class=\"section-body\">"
        ),
        (
            "<p class=\"lesson-p\">1. Xác định vấn đề và phạm vi a) Phát hiện vấn đề từ thực tiễn</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Xác định vấn đề và phạm vi</h3>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Phát hiện vấn đề từ thực tiễn</h4>"
        ),
        ("những thao tác mát thời gian", "những thao tác mất thời gian"),
        ("do họ không thế xử lí khối lượng dữ liệu", "do họ không thể xử lí khối lượng dữ liệu"),
        ("xác định một vấn đề thực tiễn má em có thể cải thiện", "xác định một vấn đề thực tiễn mà em có thể cải thiện"),
        ("vấn đề cụ thế, làm nền tảng", "vấn đề cụ thể, làm nền tảng"),
        ("sinh cò thể là lựa chọn phù hợp.</p>", "sinh có thể là lựa chọn phù hợp.</p>"),
        (
            "\n\nc) Xác định loại bài toán và phạm vi giải pháp AI</p>",
            "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Xác định loại bài toán và phạm vi giải pháp AI</h4>"
        ),
        ("đây là loại bài toán Ai nao:", "đây là loại bài toán AI nào:"),
        (
            "Đây là cơ sở đầu tiên để xác định vấn đề cần giải quyết.\n\n• Phân tích nguyên nhân giúp em hiểu rõ vì sao vấn đề tồn tại và AI có thể hỗ trợ ở điểm nào. Từ đó, em có thể tìm ra ý tưởng sản phẩm phù hợp.</li>",
            "Đây là cơ sở đầu tiên để xác định vấn đề cần giải quyết.</li>\n<li>Phân tích nguyên nhân giúp em hiểu rõ vì sao vấn đề tồn tại và AI có thể hỗ trợ ở điểm nào. Từ đó, em có thể tìm ra ý tưởng sản phẩm phù hợp.</li>"
        ),
        (
            "<p class=\"lesson-p\">2. Phân tích và thiết kế giải pháp Khi đã có vấn đề",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">2.</span> Phân tích và thiết kế giải pháp</h3>\n<p class=\"lesson-p\">Khi đã có vấn đề"
        ),
        (
"""<p class="lesson-p">Input</p>
<p class="lesson-p">AI model</p>
<p class="lesson-p">Công cụ/API</p>
<p class="lesson-p">Exported</p>
<p class="lesson-p">Oulput</p>""",
            ""
        ),
        ("các chức năng chính của sản phẩm A/</h4>", "các chức năng chính của sản phẩm AI</h4>"),
        ("<li>Nêu là trợ lí môn học:", "<li>Nếu là trợ lí môn học:"),
        ("để hoạt động hiệu quá.</p>", "để hoạt động hiệu quả.</p>"),
        ("<li>RAG (Tạo sinh có hồ trợ truy xuất):", "<li>RAG (Tạo sinh có hỗ trợ truy xuất):"),
        ("giao tiếp với người dùng như thể nào?", "giao tiếp với người dùng như thế nào?"),
        ("Sản phẩm sẽ hiến thị câu trả lời,", "Sản phẩm sẽ hiển thị câu trả lời,"),
        ("\n\na) Phân công công việc</p>", "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">a)</span> Phân công công việc</h4>"),
        ("\n\nb) Lập lịch</p>", "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Lập lịch</h4>"),
        ("\n\nc) Chuẩn bị</p>", "</p>\n<h4 class=\"subheading-h4\"><span class=\"h4-letter\">c)</span> Chuẩn bị</h4>"),
        (
            "<p class=\"lesson-p\">d) Lập kế hoạch kiểm thử và gỡ lỗi Dù chi tiết sẽ được học ở Bài 13,",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">d)</span> Lập kế hoạch kiểm thử và gỡ lỗi</h4>\n<p class=\"lesson-p\">Dù chi tiết sẽ được học ở Bài 13,"
        ),
        ("phát hiện và sửa lồi.</p>", "phát hiện và sửa lỗi.</p>"),
        ("<span class=\"h4-letter\">b)</span> Để xuất giải pháp AI</h4>", "<span class=\"h4-letter\">b)</span> Đề xuất giải pháp AI</h4>"),
        ("1. TẠi sao việc xác định phạm vi", "1. Tại sao việc xác định phạm vi"),
        ("B. Đồ đảm bảo rằng dự án khả thi", "B. Để đảm bảo rằng dự án khả thi"),
        ("C. Đế có thể bỏ qua bước kiếm thử.", "C. Để có thể bỏ qua bước kiểm thử."),
        ("D. Đồ tích hợp càng nhiều công cụ AI", "D. Để tích hợp càng nhiều công cụ AI"),
        ("lại quan trong khi thực hiện dự án AI.</p>", "lại quan trọng khi thực hiện dự án AI.</p>"),
        (
            "<ul class=\"lesson-bullet-list\">\n<li>VẬN DỤNG</li>\n</ul>",
            "</div></section>\n\n            <section class=\"lesson-card apply-section\" id=\"sec-vận-dụng\">\n                <div class=\"section-badge-header\">\n                    <span class=\"sec-icon\">🚀</span>\n                    <h2 class=\"section-title\">VẬN DỤNG</h2>\n                </div>\n                <div class=\"section-body\">"
        ),
        ("của minh mà AI Agent có tiềm năng", "của mình mà AI Agent có tiềm năng"),
        ("điểm nào là khó khăn nhât trong việc biến ý tưởng", "điểm nào là khó khăn nhất trong việc biến ý tưởng"),
        ("<p class=\"lesson-p\">D</p>\n", ""),
    ],
    "bai-13-xay-dung-san-pham": [
        (
"""<p class="lesson-p">MỤC TIEU</p>
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<p class="lesson-p">• Thực hiện được việc cài đặt môi trường và xây dựng sản phẩm.</p>""",
"""            <section class="lesson-card target-section" id="sec-mục-tiêu">
                <div class="section-badge-header">
                    <span class="sec-icon">🎯</span>
                    <h2 class="section-title">MỤC TIÊU</h2>
                </div>
                <div class="section-body">
            
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<ul class="lesson-bullet-list">
<li>Thực hiện được việc cài đặt môi trường và xây dựng sản phẩm.</li>
</ul>
</div></section>"""
        ),
        ("<p class=\"lesson-p\">Ở' Bài 12, em đã hoàn thành", "<p class=\"lesson-p\">Ở Bài 12, em đã hoàn thành"),
        ("Môi trường này bao gôm các công cụ,", "Môi trường này bao gồm các công cụ,"),
        ("một cách thuận lợi nhât.</p>", "một cách thuận lợi nhất.</p>"),
        ("Các em chỉ cần truy cập nên tảng", "Các em chỉ cần truy cập nền tảng"),
        ("như Langchain, Llama-index, Ollama (nều dùng mô hình cục bộ).", "như LangChain, LlamaIndex, Ollama (nếu dùng mô hình cục bộ)."),
        ("<li>Môi trường ào (virtual environment): Nên tạo môi trường ào riêng cho dự ản</li>", "<li>Môi trường ảo (virtual environment): Nên tạo môi trường ảo riêng cho dự án</li>"),
        ("trên nên táng no-code. Môi trường làm việc ôn định sẽ giúp", "trên nền tảng no-code. Môi trường làm việc ổn định sẽ giúp"),
        ("<p class=\"lesson-p\">Thu thập và tiên xử lí dữ liệu</p>", "<p class=\"lesson-p\">Thu thập và tiền xử lí dữ liệu</p>"),
        ("truy xuất thông tín hiệu quả.</p>", "truy xuất thông tin hiệu quả.</p>"),
        ("<p class=\"lesson-p\">Kết nối các thành phần và kiếm thử ban đầu</p>", "<p class=\"lesson-p\">Kết nối các thành phần và kiểm thử ban đầu</p>"),
        ("em cân thực hiện bước thu thập các tài liệu và sử dụng công cụ để tiên xử lí dữ liệu", "em cần thực hiện bước thu thập các tài liệu và sử dụng công cụ để tiền xử lí dữ liệu"),
        ("phương pháp phát triển. Có thế lựa chọn:</p>", "phương pháp phát triển. Có thể lựa chọn:</p>"),
        ("<p class=\"lesson-p\">+ Câu hình trên nền tảng (No-code):", "<p class=\"lesson-p\">+ Cấu hình trên nền tảng (No-code):"),
        ("Kết nối các thành phần và kiểm thừ ban đầu</h4>", "Kết nối các thành phần và kiểm thử ban đầu</h4>"),
        ("em cần kết nôi chúng lại với nhau để tạo thành một luồng hoạt động hoàn chỉnh (từ đầu vào của người dùng, qua xú lí của AI, đến đầu ra). Sau mỗi phần nhỏ được hoàn thành, hãy chạy thử và kiếm", "em cần kết nối chúng lại với nhau để tạo thành một luồng hoạt động hoàn chỉnh (từ đầu vào của người dùng, qua xử lí của AI, đến đầu ra). Sau mỗi phần nhỏ được hoàn thành, hãy chạy thử và kiểm"),
        ("Việc kiếm thử sớm giúp phát hiện", "Việc kiểm thử sớm giúp phát hiện"),
        ("(LLM, LangChain/LlamaIndex.</p>\n<p class=\"lesson-p\">hoặc các khối no-code) và kết nồi chúng.", "(LLM, LangChain/LlamaIndex,</p>\n<p class=\"lesson-p\">hoặc các khối no-code) và kết nối chúng."),
        ("AI Agent Hồ trợ học Ngữ văn 12.)</p>", "AI Agent Hỗ trợ học Ngữ văn 12.)</p>"),
        (
            "<p class=\"lesson-p\">b) Xây dựng phần cốt lõi. Tạo Agent mới trên MindStudio Bước 1.",
            "<h4 class=\"subheading-h4\"><span class=\"h4-letter\">b)</span> Xây dựng phần cốt lõi: Tạo Agent mới trên MindStudio</h4>\n<p class=\"lesson-p\">Bước 1."
        ),
        (
"""<p class="lesson-p">S Main.flow * Agent Hỗ ...Ngữ văn 12</p>
<p class="lesson-p">General</p>
<p class="lesson-p">Agent Name Metadata</p>
<p class="lesson-p">Agent Hồ trợ học Ngữ văn 12 Landing Page</p>""",
            ""
        ),
        ("<figcaption class=\"figure-caption\">Hình 13.2. Giao diện dặt tên Agent mới\n98</figcaption>", "<figcaption class=\"figure-caption\">Hình 13.2. Giao diện đặt tên Agent mới</figcaption>"),
        ("Chúng ta sẽ thêm các khói khác vào giữa.</p>\n<p class=\"lesson-p\">Start Uner Input</p>", "Chúng ta sẽ thêm các khối khác vào giữa.</p>"),
        ("<p class=\"lesson-p\">+ Tạo biến Use: Input và cấu hình biến vừa tạo.</p>", "<p class=\"lesson-p\">+ Tạo biến User Input và cấu hình biến vừa tạo.</p>"),
        (
"""<p class="lesson-p">1 : Nsr: tco % Use vor</p>
<p class="lesson-p">Tiree</p>
<p class="lesson-p">Long Ters</p>
<p class="lesson-p">Variatie</p>
<p class="lesson-p">Bạn có câu hỏi gì về môn Ngữ văn lớp 12?</p>
<p class="lesson-p">User irput.</p>
<p class="lesson-p">áp câu hỏi ở đây.</p>
<p class="lesson-p">contigeetno</p>
<p class="lesson-p">Latal Tent</p>
<p class="lesson-p">Bạn có câu hỏi gì về môn Ngữ văn lớp 12?</p>""",
            ""
        ),
        ("để AI Agent của em có thể hiếu và trả lời dựa trên dữ liệu", "để AI Agent của em có thể hiểu và trả lời dựa trên dữ liệu"),
        (
            "<p class=\"lesson-p\">* Thêm khối Generate Text vào không gian làm việc giữa khối User Input và End.</p>\n<p class=\"lesson-p\">User Input</p>\n<p class=\"lesson-p\">Generate</p>\n<p class=\"lesson-p\">Text End</p>",
            "<p class=\"lesson-p\">+ Thêm khối Generate Text vào không gian làm việc giữa khối User Input và End.</p>"
        ),
        ("theo hướng dân sau:</p>", "theo hướng dẫn sau:</p>"),
        ("<p class=\"lesson-p\">(Dân toàn bộ nội dung CSV của em vào đây]", "<p class=\"lesson-p\">[Dán toàn bộ nội dung CSV của em vào đây]"),
        ("ay tran vao Nêu câu hỏi liên quan đến một bài văn,", "Nếu câu hỏi liên quan đến một bài văn,"),
        (
            "Nếu câu hỏi là về một tác giá, hãy liệt kê các tác phẩm các dc của nhóm của họ có trong danh sách",
            "Nếu câu hỏi là về một tác giả, hãy liệt kê các tác phẩm của họ có trong danh sách"
        ),
        ("tôi không tim thấy thông tin em yêu cầu trong cơ sở dữ liệu của tôi.\" Câu hỏi của học sính: {{User input}}</p>", "tôi không tìm thấy thông tin em yêu cầu trong cơ sở dữ liệu của tôi.\" Câu hỏi của học sinh: {{User input}}</p>"),
        ("<p class=\"lesson-p\">(| User input)): Đây là một biến", "<p class=\"lesson-p\">{{User input}}: Đây là một biến"),
        ("Khối này sử dụng LLM để phận tích câu hỏi của học sinh</p>", "Khối này sử dụng LLM để phân tích câu hỏi của học sinh</p>"),
        ("<p class=\"lesson-p\">(| (User input)|) và tìm kiếm/tống hợp", "<p class=\"lesson-p\">({{User input}}) và tìm kiếm/tổng hợp"),
        ("ở góc trên bên phải đề kiểm thử AI Agent của nhóm em và chọn Open Draft Agent (Hình 13.6).</p>", "ở góc trên bên phải để kiểm thử AI Agent của nhóm em và chọn Open Draft Agent (Hình 13.6).</p>"),
        (
"""<p class="lesson-p">Preview V Publish</p>
<ul class="lesson-bullet-list">
<li>Run in Debugger</li>
</ul>
<p class="lesson-p">33R</p>
<ul class="lesson-bullet-list">
<li>Start from Selection</li>
</ul>
<p class="lesson-p">C Open Draft Agent</p>
<p class="lesson-p">C Open Published Agent</p>""",
            ""
        ),
        ("các phương án kiểm thử và gỡ lồi</figcaption>", "các phương án kiểm thử và gỡ lỗi</figcaption>"),
        ("Một hộp thoại phục vụ kiềm thử sẽ xuất hiện", "Một hộp thoại phục vụ kiểm thử sẽ xuất hiện"),
        ("<li>Tác già Nguyễn Đình Thi là ai", "<li>Tác giả Nguyễn Đình Thi là ai"),
        (
"""<p class="lesson-p">Agent Hồ trợ học Ngữ vàn 12</p>
<p class="lesson-p">Bạn có câu hỏi gì về môn Ngữ văn lớp 12?</p>
<p class="lesson-p">Mây nhập câu hoi ở lây</p>
<p class="lesson-p">Next</p>""",
            ""
        ),
        ("của Agent ở môi trường kiếm thử</figcaption>", "của Agent ở môi trường kiểm thử</figcaption>"),
        (
"""<p class="lesson-p">Agent Hỗ trợ học Ngữ văn 12</p>
<p class="lesson-p">Dựa trên thông tìn trong danh sách, tôi có thể cung cấp chi tiết về bài thơ "Dất nước" của hai tác giả:</p>
<h3 class="subheading-h3"><span class="h3-num">1.</span> Bài "Đất nước" của Nguyễn Đinh Thị:</h3>
<ul class="lesson-bullet-list">
<li>Thuộc chương: Văn học Việt Nam sau Cách mạng tháng Tám (1945-1975) • Sáng tác từ năm 19-48-1955, trong thời ki khăng chiến chống Pháp • Nội dung: Thể hiện sự gần bó sâu sắc giữa đất nước và nhân dán, sự chuyến minh của đất nước trong chiến tranh, niềm tự hào dân tộc • Phong cách: Thơ trữ tình chỉnh trị, hào hùng, suy tư • Giá trị: Góp phần định hình nến thơ ca cách mạng Việt Nam</li>
</ul>
<h3 class="subheading-h3"><span class="h3-num">2.</span> Bải "Đất nước" của Nguyễn Khoa Điểm:</h3>
<ul class="lesson-bullet-list">
<li>Thuộc chương: Văn học Việt Nam sau Cách mạng tháng Tâm (1945-1975) • Trích từ trường ca "Mặt đường khát vọng", sảng tác năm 1971, trong thời ki kháng chiến chống Mỹ • Nội dung: Định nghĩa về đất nước từ nhiều góc độ: lịch sử, văn hóa, đời sống hàng ngày, khẳng định đất nước là của nhân dân</li>
<li>Phong cách: Thơ trữ tình chính luận, tư tường sâu sắc, đậm chất triết li • Giá trị: Đem đến một cái nhìn mới mè, sâu sắc về đất nước, kháng định vai trò của nhân dân trong việc tạo dựng và bảo vệ đất nước</li>
</ul>
<p class="lesson-p">Cả hai bài thơ đều mang ý nghĩa sâu sắc về đất nước, nhưng được viết ở những giai đoạn và với góc nhìn Khác nhau</p>
<p class="lesson-p">l Copy & Share V Run Finished</p>""",
            ""
        ),
        ("<figcaption class=\"figure-caption\">Hình 13.8. Agent trả lời câu hỏi dựa vào nội dung trong tệp CSV được chuẩn bị</figcaption>", "<figcaption class=\"figure-caption\">Hình 13.8. Agent trả lời câu hỏi dựa vào nội dung trong tệp CSV được chuẩn bị và cung cấp ở mục a</figcaption>"),
        ("<p class=\"lesson-p\">và cung cấp ở mục a</p>\n", ""),
        ("<p class=\"lesson-p\">Bước 4. Tỉnh chinh và mở rộng", "<p class=\"lesson-p\">Bước 4. Tinh chỉnh và mở rộng"),
        ("Cụ thể hơn về cách AI cần hiếu và xuất thông tin.</p>", "Cụ thể hơn về cách AI cần hiểu và xuất thông tin.</p>"),
        (
            "Tên bài: (Tên bài], Tác giả: [Tên lác giả), Hoàn cảnh sáng tác: (Hoàn cảnh sáng lác], Giá trị nội dung:\n\n(Giá trị nội dung chính). Giá trị nghệ thuật: (Giá trị nghệ thuật chính].</p>",
            "Tên bài: [Tên bài], Tác giả: [Tên tác giả], Hoàn cảnh sáng tác: [Hoàn cảnh sáng tác], Giá trị nội dung: [Giá trị nội dung chính], Giá trị nghệ thuật: [Giá trị nghệ thuật chính].</p>"
        ),
        ("Generate Text chi để chào hỏi, thay vì", "Generate Text chỉ để chào hỏi, thay vì"),
        ("từ kiên thức đã cho.</p>", "từ kiến thức đã cho.</p>"),
        ("<p class=\"lesson-p\">* ((user input)) la cách chúng ta đưa dữ liệu từ khối này sang khối khác.</p>", "<p class=\"lesson-p\">+ {{User input}} là cách chúng ta đưa dữ liệu từ khối này sang khối khác.</p>"),
        ("<p class=\"lesson-p\">A. Chỉ đế xem sản phẩm có khởi động được không.</p>", "<p class=\"lesson-p\">A. Chỉ để xem sản phẩm có khởi động được không.</p>"),
        ("các thành phần đầu tiên của sản phâm.</p>", "các thành phần đầu tiên của sản phẩm.</p>"),
        ("giải quyết khó khăn đó và liếp lục công việc xây dựng?</p>", "giải quyết khó khăn đó và tiếp tục công việc xây dựng?</p>"),
    ],
    "bai-14-hoan-chinh-san-pham": [
        (
"""<p class="lesson-p">SẢN PHẬM</p>
<p class="lesson-p">MUC TIEU</p>
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<p class="lesson-p">• Thực hiện được việc kiểm thừ và gỡ lỗi cho sản phẩm.</p>
<p class="lesson-p">• Cải thiện hiệu suất và độ chính xác của sản phẩm (Tối ưu hoá).</p>""",
"""            <section class="lesson-card target-section" id="sec-mục-tiêu">
                <div class="section-badge-header">
                    <span class="sec-icon">🎯</span>
                    <h2 class="section-title">MỤC TIÊU</h2>
                </div>
                <div class="section-body">
            
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<ul class="lesson-bullet-list">
<li>Thực hiện được việc kiểm thử và gỡ lỗi cho sản phẩm.</li>
<li>Cải thiện hiệu suất và độ chính xác của sản phẩm (Tối ưu hoá).</li>
</ul>
</div></section>"""
        ),
        ("hoặc trọ lí cửa hàng tạp hoá.", "hoặc trợ lí cửa hàng tạp hoá."),
        ("sản phẩm AI của minh đã sản sàng để sử dụng hay chưa?", "sản phẩm AI của mình đã sẵn sàng để sử dụng hay chưa?"),
        (
            "<p class=\"lesson-p\">1. Kiểm thử và gỡ lỗi sản phẩm AI Agents Giống như việc kiểm tra kĩ lưỡng một chiếc xe đạp vừa được lắp ráp để đảm bảo</p>\n<p class=\"lesson-p\">nó chạy an toàn, sản phẩm AI của chúng ta cũng cần được kiểm thử (testing) Ki càng. Mục tiêu của kiêm thử là tìm ra lỗi, vấn đề và đảm bảo sản phẩm hoạ động đúng như thiết kế. Khi phát hiện lỗi, chúng ta cần gỡ lỗi (debugging) để khắi phục chúng.</p>",
            "<h3 class=\"subheading-h3\"><span class=\"h3-num\">1.</span> Kiểm thử và gỡ lỗi sản phẩm AI Agents</h3>\n<p class=\"lesson-p\">Giống như việc kiểm tra kĩ lưỡng một chiếc xe đạp vừa được lắp ráp để đảm bảo nó chạy an toàn, sản phẩm AI của chúng ta cũng cần được kiểm thử (testing) kĩ càng. Mục tiêu của kiểm thử là tìm ra lỗi, vấn đề và đảm bảo sản phẩm hoạt động đúng như thiết kế. Khi phát hiện lỗi, chúng ta cần gỡ lỗi (debugging) để khắc phục chúng.</p>"
        ),
        ("<span class=\"h4-letter\">a)</span> Tri sao phải kiểm thứ?</h4>", "<span class=\"h4-letter\">a)</span> Tại sao phải kiểm thử?</h4>"),
        ("<p>Kiềm thử là quá trình không thể thiếu để đảm bảo chất lượng. Nó giúp chúng la:</p>", "<p>Kiểm thử là quá trình không thể thiếu để đảm bảo chất lượng. Nó giúp chúng ta:</p>"),
        ("<li>Phát hiện lỗi: Tim ra những điểm", "<li>Phát hiện lỗi: Tìm ra những điểm"),
        ("<p class=\"lesson-p\">có hành vì không mong muốn.</p>", "<p class=\"lesson-p\">có hành vi không mong muốn.</p>"),
        ("mọi chức năng được thiết kế đều hoại</li>", "mọi chức năng được thiết kế đều hoạt</li>"),
        ("Ví dụ: Trợ li môn học", "Ví dụ: Trợ lí môn học"),
        ("<p class=\"lesson-p\">tối hơn cho người dùng.</p>", "<p class=\"lesson-p\">tốt hơn cho người dùng.</p>"),
        ("<span class=\"h4-letter\">b)</span> Các loại kiểm thừ cơ bản</h4>", "<span class=\"h4-letter\">b)</span> Các loại kiểm thử cơ bản</h4>"),
        ("<p class=\"lesson-p\">Kiếm thừ chức năng Kiếm thừ phản hồi Kiểm thừ trường hợp đặc biệt</p>\n", ""),
        ("mỗi tính năng của săn</li>", "mỗi tính năng của sản</li>"),
        ("Với trợ lí cửa hàng tạp hoa</p>", "Với trợ lí cửa hàng tạp hoá</p>"),
        ("hãy thứ hỏi về giá của một sản phẩm hoặc xem nó có thể tìm kiếm theo tên không</p>", "hãy thử hỏi về giá của một sản phẩm hoặc xem nó có thể tìm kiếm theo tên không.</p>"),
        ("<li>Kiểm thừ phản hồi (LLM Response Testing):", "<li>Kiểm thử phản hồi (LLM Response Testing):"),
        ("Chúng ta sẽ đánh glá chất lượng câu trả lời:</p>", "Chúng ta sẽ đánh giá chất lượng câu trả lời:</p>"),
        ("<p class=\"lesson-p\">câp không? Tránh bịa đặt (hallucination).</p>", "<p class=\"lesson-p\">cấp không? Tránh bịa đặt (hallucination).</p>"),
        ("<p class=\"lesson-p\">quảng không?</p>", "<p class=\"lesson-p\">quãng không?</p>"),
        ("<li>Kiểm thừ trường hợp đặc biệt:", "<li>Kiểm thử trường hợp đặc biệt:"),
        ("quá dài, quá ngăn, hoặc không liên quan", "quá dài, quá ngắn, hoặc không liên quan"),
        ("Ví dụ, hòi trợ lí môn học", "Ví dụ, hỏi trợ lí môn học"),
        (
"""<p class="lesson-p">Phát hiện và ghi nhận lỗi</p>
<p class="lesson-p">Tách và phân tích nguyên nhân</p>
<p class="lesson-p">Khắc phục và xóc nhận két quả</p>
<p class="lesson-p">Xem tràng bảo lỏi chi hệt và phản tích log</p>
<p class="lesson-p">Tát từng phân của hý inông độ tìm ra nguồn</p>
<p class="lesson-p">Sửa kỏi kiểm thử lại và xác nhận văn đè đi</p>
<p class="lesson-p">bệ thông</p>
<p class="lesson-p">gór ván de</p>
<p class="lesson-p">được giải quyết</p>""",
            ""
        ),
        ("Khi phát hiện lỗi, hãy binh tĩnh", "Khi phát hiện lỗi, hãy bình tĩnh"),
        ("Bước 1. Phát hiện và ghi nhận lới: Các thông báo lỗi thường cung cấp thông tin quan trọng về nguyên nhân và vị tri xảy ra lỗi. Việc đọc kĩ và hiểu nội dung của thông báo giúp xác định chính xác vần đề cần xử lí.", "Bước 1. Phát hiện và ghi nhận lỗi: Các thông báo lỗi thường cung cấp thông tin quan trọng về nguyên nhân và vị trí xảy ra lỗi. Việc đọc kĩ và hiểu nội dung của thông báo giúp xác định chính xác vấn đề cần xử lí."),
        ("kĩ thông bảo lỗi (error message).", "kĩ thông báo lỗi (error message)."),
        ("thông tin chi tiêt về lỗi", "thông tin chi tiết về lỗi"),
        ("theo từng phần riêng biệt đề khoanh vùng và xác định chính xác vị trí hoạc nguyên nhân gây lỗi.", "theo từng phần riêng biệt để khoanh vùng và xác định chính xác vị trí hoặc nguyên nhân gây lỗi."),
        ("Khi đã xác định được nguyên nhãn, cần thực hiện điều chỉnh phù hợp để khắc phục lỗi và sau đó kiểm tra lại toàn bộ hệ thống để đảm bào lỗi không tái diễn.", "Khi đã xác định được nguyên nhân, cần thực hiện điều chỉnh phù hợp để khắc phục lỗi và sau đó kiểm tra lại toàn bộ hệ thống để đảm bảo lỗi không tái diễn."),
        ("<li>Ap dụng giải pháp sửa lỗi phù hợp.</li>", "<li>Áp dụng giải pháp sửa lỗi phù hợp.</li>"),
        ("không gây ành hưởng đến các phần khác.</li>", "không gây ảnh hưởng đến các phần khác.</li>"),
        ("ghi chú lại quá trình sửa lỗi đề phục vụ", "ghi chú lại quá trình sửa lỗi để phục vụ"),
        ("<li>Kiếm thử là bước quan trọng", "<li>Kiểm thử là bước quan trọng"),
        ("phản hồi của LLM và các tình huỗng đặc biệt.</li>", "phản hồi của LLM và các tình huống đặc biệt.</li>"),
        ("Đây là quá trình tôi vu hoá.</p>", "Đây là quá trình tối ưu hoá.</p>"),
        ("giảm tài nguyên tính toán (nếu dùng AP|", "giảm tài nguyên tính toán (nếu dùng API"),
        ("<p class=\"lesson-p\">trà phí).</p>", "<p class=\"lesson-p\">trả phí).</p>"),
        ("<li>Nâng cao chất lượng: Đàm bảo sản phẩm", "<li>Nâng cao chất lượng: Đảm bảo sản phẩm"),
        (
"""<p class="lesson-p">Tối ưu Prompt</p>
<p class="lesson-p">Tối ưu hóa do liệu</p>
<p class="lesson-p">Điều chỉnh tham số mô hình</p>
<p class="lesson-p">Tối va boa ToollAgent</p>
<p class="lesson-p">Vill ctu soi es rang a tl va oo</p>
<p class="lesson-p">yo ctr dl d too cra ckcy arn cia tar</p>
<p class="lesson-p">Chíên bị da liêu sach, có chu trú và coia nhó hap 5 lố Ai có tri tin</p>
<p class="lesson-p">Thy coirh aas shang ed ad sinh of</p>
<p class="lesson-p">để AI có thể suy luận và sử dụng</p>
<p class="lesson-p">Thuốt kố qua tánh cứ 5 thông mích</p>
<p class="lesson-p">Niêm nây th cont kac.</p>
<p class="lesson-p">on dese lés ad pon lop vos rud dict ao cung</p>
<p class="lesson-p">công cụ niều mut</p>""",
            ""
        ),
        ("Lịch sử, hãy giải thích.\n\n- Tối ưu hoa dữ liệu:</p>", "Lịch sử, hãy giải thích.</p>\n<ul class=\"lesson-bullet-list\"><li>Tối ưu hoá dữ liệu:</li></ul>"),
        ("Đảm bào nguồn dữ liệu mà AI truy xuất", "Đảm bảo nguồn dữ liệu mà AI truy xuất"),
        ("Xoá bò thông tin nhiễu, trùng lặp.", "Xoá bỏ thông tin nhiễu, trùng lặp."),
        ("biểu diễn vector: Điều chình kích thước", "biểu diễn vector: Điều chỉnh kích thước"),
        ("phương pháp tạo vector để đàm bảo các đoạn liên quan", "phương pháp tạo vector để đảm bảo các đoạn liên quan"),
        ("<p class=\"lesson-p\">ngăn gọn, đi thẳng vào vấn đề hơn.</p>", "<p class=\"lesson-p\">ngắn gọn, đi thẳng vào vấn đề hơn.</p>"),
        (
"""                    <div class="callout-box knowledge-callout">
                        <div class="callout-title">📘 Hộp kiến thức cốt lõi</div>
                        <p>Tối ưu hóa là quá trình cải thiện sản phẩm AI về hiệu suất và độ chính xác. Các phương pháp chính bao gồm tối ưu prompt (cụ thể, có vai trò), cải thiện chất lượng dữ liệu RAG (sạch, liên</p>
                    </div>
                    
<p class="lesson-p">quan), điều chỉnh tham số mô hình (temperature, max_tokens) và tối ưu hóa hoạt động của công cụ/Agent.</p>""",
"""                    <div class="callout-box knowledge-callout">
                        <div class="callout-title">📘 Hộp kiến thức cốt lõi</div>
                        <p>Tối ưu hóa là quá trình cải thiện sản phẩm AI về hiệu suất và độ chính xác. Các phương pháp chính bao gồm tối ưu prompt (cụ thể, có vai trò), cải thiện chất lượng dữ liệu RAG (sạch, liên quan), điều chỉnh tham số mô hình (temperature, max_tokens) và tối ưu hóa hoạt động của công cụ/Agent.</p>
                    </div>"""
        ),
        (
"""<p class="lesson-p">8 Mẹo hữu ích</p>
<ul class="lesson-bullet-list">
<li>Mẹo Kiếm thừ</li>
</ul>
<p class="lesson-p">/ Mẹo Gờ lỏi</p>
<p class="lesson-p">B Mẹo Học tập</p>
<p class="lesson-p">/ Kiểm thứ theo ké hoạch có hệ thống</p>
<p class="lesson-p">\\ Chuẩn bị test cases trước khi bật đầu</p>
<p class="lesson-p">/ Kiên nhản - debug mất thời gian</p>
<ul class="lesson-bullet-list">
<li>Học hỏi từ mỗi lỏi gặp phải</li>
</ul>
<p class="lesson-p">1 Thứ nghiệm với dữ liệu thực té</p>
<p class="lesson-p">v Thứ từng bước một cách logic</p>
<p class="lesson-p">v Đọc kĩ thông báo lỗi</p>
<p class="lesson-p">/ Tao checklist đé không bỏ sót</p>
<p class="lesson-p">1 Thực hành thường xuyên</p>
<p class="lesson-p">1 Ghi chép kết quả chi tiét</p>
<p class="lesson-p">v Hói ý kién đồng đội khi căn</p>
<p class="lesson-p">V Chia sẻ kinh nghiệm với bạn</p>""",
            ""
        ),
        (
            "Già sử nhóm em đang xây dựng một trợ lí môn học cho mỏn Ngữ văn lớp 12, sử dụng dữ liệu là các bài học, tác phẩm, câu hỏi ôn tập có trong môn Ngữ văn lóp 12.",
            "Giả sử nhóm em đang xây dựng một trợ lí môn học cho môn Ngữ văn lớp 12, sử dụng dữ liệu là các bài học, tác phẩm, câu hỏi ôn tập có trong môn Ngữ văn lớp 12."
        ),
        ("<p class=\"lesson-p\">Cam Scanner</p>\n", ""),
        ("<p class=\"lesson-p\">Trợ lị này là một AI Agent", "<p class=\"lesson-p\">Trợ lí này là một AI Agent"),
        ("<p class=\"lesson-p\">Bươc 1. Dựa trên các chức năng", "<p class=\"lesson-p\">Bước 1. Dựa trên các chức năng"),
        ("<li>Trường hợp 2 (Tim kiểm tác già): Thông tin về tác giả Vũ Trọng Phụng (Ki</li>", "<li>Trường hợp 2 (Tìm kiếm tác giả): Thông tin về tác giả Vũ Trọng Phụng (Kì</li>"),
        ("<li>Trường hợp 4 (Kiếm tra dữ liệu ngoài phạm vi):", "<li>Trường hợp 4 (Kiểm tra dữ liệu ngoài phạm vi):"),
        ("<p class=\"lesson-p\">Bước 2. Chạy sản phầm AI của nhóm", "<p class=\"lesson-p\">Bước 2. Chạy sản phẩm AI của nhóm"),
        ("Dựa vào các phương pháp gỡ lối đã học", "Dựa vào các phương pháp gỡ lỗi đã học"),
        ("thông tin về Vũ Trọng Phụng: Kiềm tra lại dữ liệu trong cột</li>", "thông tin về Vũ Trọng Phụng: Kiểm tra lại dữ liệu trong cột</li>"),
        ("tác phẩm Số đò và prompt xem LLM", "tác phẩm Số đỏ và prompt xem LLM"),
        ("tác phẩm Số đỏ: Kiềm tra lại cách chia nhỏ</li>", "tác phẩm Số đỏ: Kiểm tra lại cách chia nhỏ</li>"),
        ("<span class=\"h4-letter\">c)</span> Tôi ưu hoá</h4>", "<span class=\"h4-letter\">c)</span> Tối ưu hoá</h4>"),
        (
"""<p class="lesson-p">Xác định mục têu rở ràng:

Biết chính xác bạn muốn AI</p>
<p class="lesson-p">Thử nghiệm và điều chỉnh:</p>
<p class="lesson-p">Cung cấp ngữ cảnh: Cho AI biết bạn là ai, đang học gì đó</p>
<p class="lesson-p">Kiểm tra kết quả: Luôn xắc</p>
<p class="lesson-p">Không ngai thay đổi cách hỏi</p>
<p class="lesson-p">nình thông tin từ AI, đác biệt</p>
<p class="lesson-p">giúp gì trước khi đặt câu hội</p>
<p class="lesson-p">nếu kết quả chưa như mong</p>
<p class="lesson-p">có cấu trả lời phù hợp muốn.</p>
<p class="lesson-p">với bài tập quan trọng.</p>""",
            ""
        ),
        ("hoạt động đúng nhưng chưa thực sự tôi ưu (ví dụ:", "hoạt động đúng nhưng chưa thực sự tối ưu (ví dụ:"),
        (
            "<p class=\"lesson-p\">tác giá Vũ Trọng Phụng\",\", hãy thử \"Hãy tóm tắt về tác giả Vũ Trọng Phụng và</p>\n<p class=\"lesson-p\">hai tác phẩm tiêu biểu nhất của ông trong danh sách dưới 50 từ\"</p>",
            "<p class=\"lesson-p\">tác giả Vũ Trọng Phụng\", hãy thử \"Hãy tóm tắt về tác giả Vũ Trọng Phụng và hai tác phẩm tiêu biểu nhất của ông trong danh sách dưới 50 từ\".</p>"
        ),
        ("<li>Điều chinh temperature:", "<li>Điều chỉnh temperature:"),
        ("Phong cách nghệ thuật chính);</p>", "Phong cách nghệ thuật chính),</p>"),
        ("<p class=\"lesson-p\">D. Kiếm tra màu sắc giao diện.</p>", "<p class=\"lesson-p\">D. Kiểm tra màu sắc giao diện.</p>"),
        ("2. Đế trợ lí môn học có câu trả lời sáng tạo và đa dạng hơn (it bị lặp lại),", "2. Để trợ lí môn học có câu trả lời sáng tạo và đa dạng hơn (ít bị lặp lại),"),
        ("A. max_tokens tang lên.", "A. max_tokens tăng lên."),
        ("D. top._k giảm xuống.</p>", "D. top_k giảm xuống.</p>"),
        ("tối ưu hoá prompt lại quan trọng đổi với độ chính xác", "tối ưu hoá prompt lại quan trọng đối với độ chính xác"),
        ("phương pháp tối ưu hoá nào để cài thiện sản phẩm", "phương pháp tối ưu hoá nào để cải thiện sản phẩm"),
    ],
    "bai-15-trinh-bay-ket-qua-du-an": [
        ("<p class=\"lesson-p\">BÃI 15. TRÌNH BÀY KÊT QUA</p>\n<p class=\"lesson-p\">DỰ AN</p>\n", ""),
        (
            "lên ý tưởng, thiết kê giải pháp (Bài 12), cho đến xây dựng (Bài 13) và hoàn chỉnh sản phâm (Bài 14).",
            "lên ý tưởng, thiết kế giải pháp (Bài 12), cho đến xây dựng (Bài 13) và hoàn chỉnh sản phẩm (Bài 14)."
        ),
        ("một bài trình bàyy vê dự án nên bao gôm các phân chính sau:", "một bài trình bày về dự án nên bao gồm các phần chính sau:"),
        (
"""<h3 class="subheading-h3"><span class="h3-num">1.</span> Vấn đề và lí do chọn đề tài</h3>
<h3 class="subheading-h3"><span class="h3-num">2.</span> Giải pháp AI và cách hoạt động</h3>
<h3 class="subheading-h3"><span class="h3-num">3.</span> Dữ liệu và xây dựng Agent</h3>
<h3 class="subheading-h3"><span class="h3-num">4.</span> Demo sản phẩm</h3>
<h3 class="subheading-h3"><span class="h3-num">5.</span> Kết quả và cải tiến</h3>
<h3 class="subheading-h3"><span class="h3-num">6.</span> Hạn chế và tiêm năng</h3>
<h3 class="subheading-h3"><span class="h3-num">7.</span> Kết luận và lời cảm ơn</h3>""",
            ""
        ),
        ("Nêu rõ vấn đề thực tiễn ẠI giải quyết", "Nêu rõ vấn đề thực tiễn AI giải quyết"),
        ("<p class=\"lesson-p\">Ngôn ngữ cơ thể và giọng nói tự tin Quản lí thời gian</p>\n<p class=\"lesson-p\">Trả lời câu hỏi Luyện tập trước</p>\n", ""),
        ("<p class=\"lesson-p\">tiêp bằng mắt.</p>", "<p class=\"lesson-p\">tiếp bằng mắt.</p>"),
        (
            "Việc xây dụng một sản phẩm AI là thành tựu kĩ thuật, nhưng khả năng giải thích ý nghĩa và tác động sâu rộng của nó mới là điêu chứng minh tàm nhìn và giá trị",
            "Việc xây dựng một sản phẩm AI là thành tựu kĩ thuật, nhưng khả năng giải thích ý nghĩa và tác động sâu rộng của nó mới là điều chứng minh tầm nhìn và giá trị"
        ),
        ("<span class=\"h4-letter\">a)</span> Y nghĩa thực tiễn của sản phẩm</h4>", "<span class=\"h4-letter\">a)</span> Ý nghĩa thực tiễn của sản phẩm</h4>"),
        ("cho một vàn đẻ có thật.</p>", "cho một vấn đề có thật.</p>"),
        ("một cách cụ thể? (vĩ dịụ:", "một cách cụ thể? (ví dụ:"),
        (
            "trợ lí môn học giúp học sinh tiêt kiệm thời gian tim kiểm tài liệu; trợ lí cửa hàng tạp hoa giúp chủ cửa hàng quản lí hàng hóa",
            "trợ lí môn học giúp học sinh tiết kiệm thời gian tìm kiếm tài liệu; trợ lí cửa hàng tạp hoá giúp chủ cửa hàng quản lí hàng hóa"
        ),
        ("chủ cửa hàng giảm thiêu sai sót).</p>", "chủ cửa hàng giảm thiểu sai sót).</p>"),
        ("So với cách làm truyền thông, sản phẩm Ai của em có điểm vượt trội nào? (vi", "So với cách làm truyền thống, sản phẩm AI của em có điểm vượt trội nào? (ví"),
        ("dụ: nhanh hơn, chính xác hơn, tự động hoa).</p>", "dụ: nhanh hơn, chính xác hơn, tự động hoá).</p>"),
        ("Hãy mở rộng tàm nhìn, không chỉ dừng lại", "Hãy mở rộng tầm nhìn, không chỉ dừng lại"),
        ("<li>Sàn phẩm của em tác động đến nhóm người dùng cụ thể nào?", "<li>Sản phẩm của em tác động đến nhóm người dùng cụ thể nào?"),
        ("một lĩnh vực cụ thế? (ví dụ:", "một lĩnh vực cụ thể? (ví dụ:"),
        ("trong tương lai đề sản phẩm của em", "trong tương lai để sản phẩm của em"),
        ("định, có kết nồi Internet nêu cần).</p>", "định, có kết nối Internet nếu cần).</p>"),
        ("về giá trị của sản phầm? Tại sao?", "về giá trị của sản phẩm? Tại sao?"),
        ("em nên phản ứng như thể nào để thể hiện", "em nên phản ứng như thế nào để thể hiện"),
        ("lập trình, kiểm thử, Kĩ năng trình bày)?</p>", "lập trình, kiểm thử, kĩ năng trình bày)?</p>"),
        ("các dự án học tập hoặc cóng việc tương lai?</p>", "các dự án học tập hoặc công việc tương lai?</p>"),
    ],
    "bang-giai-thich-thuat-ngu": [
        (
"""<p class="lesson-p">BẢNG GIẢI THÍCH THUẬT NGỮ</p>
<p class="lesson-p">Thuật ngữ</p>
<p class="lesson-p">Giải thích</p>
<p class="lesson-p">Trang</p>
<p class="lesson-p">Hệ thống trí tuệ nhân tạo có thể quan sát, xử lí thông tin, ra quyết định và hành động để đạt</p>
<p class="lesson-p">AI Agent (Tác nhân thông minh)</p>
<p class="lesson-p">mục tiêu.</p>
<p class="lesson-p">AI tạo sinh (Generative AI)</p>
<p class="lesson-p">Loại trí tuệ nhân tạo có khả năng tạo ra nội dung mới (văn bản, hình ảnh, âm thanh, video...) dựa trên dữ liệu đã được học.</p>
<p class="lesson-p">Bộ quy tắc cho phép các lập trình viên có thể sử dụng để gửi yêu cầu và nhận lại dữ liệu từ một hệ thống khác. API thường xuất hiện dưới dạng URL, mã hàm hoặc thư viện,...</p>
<p class="lesson-p">API (Application Programming Interface)</p>
<p class="lesson-p">Xu hướng mô hình học thiên lệch do dữ liệu không cân bằng, có thể dẫn đến kết quả không công bằng.</p>
<p class="lesson-p">B</p>
<p class="lesson-p">Bias (Thiên vị)</p>
<p class="lesson-p">Lượng thông tin (ví dụ: số từ, token) mà một mô hình AI có thể "ghi nhớ"' hoặc xem xét tại một thời điểm khi xử lí prompt và tạo phản hồi. Giới hạn này ảnh hưởng đến khả năng hiểu và duy trì mạch lạc của AI trong các cuộc hội thoại dài.</p>
<p class="lesson-p">Cửa số ngữ cảnh (Context Window)</p>
<p class="lesson-p">Định dạng JSON (JavaScript</p>
<p class="lesson-p">Cách thức chuẩn để tổ chức và trao đổi dữ liệu dưới dạng văn bản.</p>
<p class="lesson-p">Object Notation)</p>
<p class="lesson-p">Framework</p>
<p class="lesson-p">F</p>
<p class="lesson-p">(Khung làm việc)</p>
<p class="lesson-p">Bộ công cụ và quy tắc sẵn có giúp lập trình viên xây dựng phần mềm nhanh và hiệu quả.</p>
<p class="lesson-p">Index (Chỉ mục)</p>
<p class="lesson-p">Cách tổ chức và lưu trữ dữ liệu để có thể tìm kiếm nhanh chóng và hiệu quả.</p>
<p class="lesson-p">Mô hình Àl chuyên dùng để chuyển đổi dữ liệu (văn bản, hình ảnh,...) thành các vector số (một chuỗi số). Các vector này mã hoá ý nghĩa của dữ liệu, giúp AI dễ dàng so sánh, tìm kiếm và hiểu mỗi quan hệ giữa các dữ liệu khác nhau</p>
<p class="lesson-p">Mô hình Embedding</p>
<p class="lesson-p">Overfitting (Quá khớp)</p>
<p class="lesson-p">Xây ra khi mô hình học quá kĩ dữ liệu cũ, dẫn đến kém hiệu quả khi gặp dữ liệu mới.</p>
<p class="lesson-p">Thuật ngứ Giải thích</p>
<p class="lesson-p">Trang</p>
<p class="lesson-p">Lệnh hoặc câu hỏi đầu vào mà người dùng cung cấp cho một mô hình AI để hướng dẫn nó tạo ra nội dung mong muốn.</p>
<p class="lesson-p">Prompt</p>
<p class="lesson-p">Một công việc cụ thể, có mục tiêu rõ ràng mà một hệ thống, chương trình, hoặc mô hình AI được thiết kế để thực hiện. Một tác vụ thường bao gồm các yêu cầu đầu vào nhất định và mong đợi một kết quả đầu ra cụ thể.</p>
<p class="lesson-p">Tác vụ (Task)</p>
<p class="lesson-p">Thư viện nguồn Thư viện lập trình có mã nguồn công khai, miễn</p>
<p class="lesson-p">mở phí sử dụng và tuỳ chỉnh.</p>
<p class="lesson-p">Top_k (trong cầu hình LLM)</p>
<p class="lesson-p">Số lượng từ/token có xác suất cao nhất mà mô hình LLM sẽ xem xét khi chọn từ tiếp theo để tạo ra câu trả lời.</p>
<p class="lesson-p">Vector Store Index (Chỉ mục</p>
<p class="lesson-p">Cấu trúc dữ liệu lưu trữ và tổ chức các vector nhúng (embeddings) để có thể tìm kiếm nhanh chóng các vector tương tự (có ý nghĩa gần giống nhau).</p>
<p class="lesson-p">kho lưu trữ vector)</p>
<p class="lesson-p">72111</p>""",
            GLOSSARY_CLEAN_BODY.strip()
        ),
    ],
    "thong-tin-xuat-ban-bia-sau": [
        (
            "<p class=\"lesson-p\">Trân trọng cảm ơn các tác giả có tác phẩm,</p>\n<p class=\"lesson-p\">ơ liệu được sử dụng, trích dẫn</p>\n<p class=\"lesson-p\">trong cuốn sách này.</p>",
            "<p class=\"lesson-p\">Trân trọng cảm ơn các tác giả có tác phẩm, tư liệu được sử dụng, trích dẫn trong cuốn sách này.</p>"
        ),
        ("Tổng Giảm đốc NGUYỄN TIỀN THANH", "Tổng Giám đốc NGUYỄN TIẾN THANH"),
        ("Họa sĩ trường ĐINH GIA LÊ", "Họa sĩ trưởng ĐINH GIA LÊ"),
        (
            "ĐẶNG DUY TIẾN - NGUYỄN THẾ PHI Sửa bản in: PHẠM THỊ THANH NAM - LƯU THẾ SƠN",
            "ĐẶNG DUY TIẾN - NGUYỄN THẾ PHI</p>\n<p class=\"lesson-p\">Sửa bản in: PHẠM THỊ THANH NAM - LƯU THẾ SƠN"
        ),
        (
            "TRÍ TUỆ NHÂN TẠO LỚP 12 Mã số: TZT40P6-SED",
            "TRÍ TUỆ NHÂN TẠO LỚP 12</p>\n<p class=\"lesson-p\">Mã số: TZT40P6-SED"
        ),
        (
            "Bao Bì Kiến Á 26 Nguyễn Nghiêm, Phường Tân Phú, TP.Hồ Chí Minh, Việt Nam.",
            "Bao Bì Kiến Á – 26 Nguyễn Nghiêm, Phường Tân Phú, TP. Hồ Chí Minh, Việt Nam."
        ),
        (
            "xã Thái Mỹ, TP.Hồ Chí Minh Số ĐKXB: 416-2026/CXBIPH/38-168/GD",
            "xã Thái Mỹ, TP. Hồ Chí Minh</p>\n<p class=\"lesson-p\">Số ĐKXB: 416-2026/CXBIPH/38-168/GD"
        ),
        ("In xong và nộp lưu chiều tháng 03 năm 2026", "In xong và nộp lưu chiểu tháng 03 năm 2026"),
        ("<p class=\"lesson-p\">VAI DENDANTAO</p>\n<p class=\"lesson-p\">TaRUE HANDO</p>\n", ""),
        ("CÔNG TY CỔ PHẦN ĐÂU TƯ VÀ PHÁT TRIỂN GIÁO DỤC PHƯƠNG NAM", "CÔNG TY CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN GIÁO DỤC PHƯƠNG NAM"),
        ("\n<p class=\"lesson-p\">3411</p>", ""),
    ],
}


def compute_summary(html: str) -> str:
    body = re.sub(r"<header class=\"lesson-header\">.*?</header>", "", html, flags=re.DOTALL)
    plain = re.sub(r"<[^>]+>", " ", body)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) > 280:
        return plain[:280].rstrip() + "..."
    return plain


def main():
    lessons_path = DATA_DIR / "lessons-lop-12.json"
    lessons = json.loads(lessons_path.read_text(encoding="utf-8"))

    unmatched = []
    total_applied = 0
    summaries_by_id = {}

    for les in lessons:
        les_id = les["id"]
        html_file = LESSONS_DIR / f"{les_id}.html"
        content = html_file.read_text(encoding="utf-8").replace("\r\n", "\n")

        rules = REPLACEMENTS.get(les_id, [])
        for idx, (old, new) in enumerate(rules, 1):
            cnt = content.count(old)
            if cnt == 0:
                unmatched.append((les_id, idx, old[:80]))
            else:
                content = content.replace(old, new)
                total_applied += cnt

        # Clean excessive blank lines left after removals
        content = re.sub(r"\n{3,}", "\n\n", content)

        html_file.write_text(content, encoding="utf-8")
        les["html"] = content
        summary = compute_summary(content)
        les["summary"] = summary
        summaries_by_id[les_id] = summary

    if unmatched:
        print(f"[WARNING] Unmatched targets ({len(unmatched)}):")
        for lid, idx, snip in unmatched:
            print(f"  - {lid} #{idx}: {snip!r}")
    else:
        print("[OK] 0 unmatched targets!")

    print(f"Total exact replacements applied: {total_applied}")

    lessons_path.write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {lessons_path}")

    # Update books.json for lop-12 summaries
    books_path = DATA_DIR / "books.json"
    books_data = json.loads(books_path.read_text(encoding="utf-8"))
    books_list = books_data.get("books", books_data)
    updated_toc_items = 0
    for bk in books_list:
        if bk["id"] == "lop-12":
            for grp in bk.get("toc", []):
                for it in grp.get("items", []):
                    if it.get("id") in summaries_by_id:
                        it["summary"] = summaries_by_id[it["id"]]
                        updated_toc_items += 1
    books_path.write_text(json.dumps(books_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {updated_toc_items} summaries in {books_path}")

    # Rebuild search-lop-12.json
    search_data = []
    for item in lessons:
        html = item.get("html", "")
        clean_text = re.sub(r"<[^>]+>", " ", html)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        full_content = re.sub(r"\s+", " ", f"{item.get('group', '')} {item.get('title', '')} {clean_text}".strip())
        search_data.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "group": item.get("group"),
            "startPage": item.get("startPage", 1),
            "content": full_content,
        })
    search_path = DATA_DIR / "search-lop-12.json"
    search_path.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt {search_path} with {len(search_data)} entries.")


if __name__ == "__main__":
    main()
