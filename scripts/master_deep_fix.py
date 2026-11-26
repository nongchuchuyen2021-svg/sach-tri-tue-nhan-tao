import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons"

# Global replacements applicable to all texts
GLOBAL_REPLACEMENTS = [
    # --- Common OCR accents and typos ---
    (r'\bchúngta\b', 'chúng ta'),
    (r'\bđòng hò\b', 'đồng hồ'),
    (r'\bđòng\b', 'đồng'),
    (r'\btừ1\s+giờ\b', 'từ 1 giờ'),
    (r'\btừ1\b', 'từ 1'),
    (r'\bkhông vl dụ\b', 'không ví dụ'),
    (r'\bvl dụ\b', 'ví dụ'),
    (r'\bcông củ\b', 'công cụ'),
    (r'\btao ra\b', 'tạo ra'),
    (r'\bA/\s+lạo sinh\b', 'AI tạo sinh'),
    (r'\bA/\s+lạo\b', 'AI tạo'),
    (r'\blạo sinh\b', 'tạo sinh'),
    (r'\bAi\s+thô hệ\b', 'AI thế hệ'),
    (r'\bthô hệ\b', 'thế hệ'),
    (r'\b1\.\s+Prompt co bán\s+Trong chương trinh\b', '1. Prompt cơ bản\n\nTrong chương trình'),
    (r'\bPrompt co bán\b', 'Prompt cơ bản'),
    (r'\bprompt co bán\b', 'prompt cơ bản'),
    (r'\bPrompt co bản\b', 'Prompt cơ bản'),
    (r'\bprompt co bản\b', 'prompt cơ bản'),
    (r'\bPrompt co bàn\b', 'Prompt cơ bản'),
    (r'\bprompt co bàn\b', 'prompt cơ bản'),
    (r'\bco bán\b', 'cơ bản'),
    (r'\bco bàn\b', 'cơ bản'),
    (r'\bcơ bán\b', 'cơ bản'),
    (r'\bcơ bàn\b', 'cơ bản'),
    (r'\bprompt co\b', 'prompt cơ'),
    (r'\bPrompt co\b', 'Prompt cơ'),
    (r'\bnàng cao\b', 'nâng cao'),
    (r'\bchương trinh\b', 'chương trình'),
    (r'\bChương trinh\b', 'Chương trình'),
    (r'\bvi dự\b', 'ví dụ'),
    (r'\bVi dự\b', 'Ví dụ'),
    (r'\bVI dụ\b', 'Ví dụ'),
    (r'\bVi dụ\b', 'Ví dụ'),
    (r'\bvị dụ\b', 'ví dụ'),
    (r'\bVị dụ\b', 'Ví dụ'),
    (r'\bvi dụ\b', 'ví dụ'),
    (r'\bmỏ hình\b', 'mô hình'),
    (r'\bmò hình\b', 'mô hình'),
    (r'\bmỏ hinh\b', 'mô hình'),
    (r'\bmõ hình\b', 'mô hình'),
    (r'\bMỏ hình\b', 'Mô hình'),
    (r'\bcầu sau\b', 'câu sau'),
    (r'\bthém\b', 'thêm'),
    (r'\bngữ cành\b', 'ngữ cảnh'),
    (r'\bbối cành\b', 'bối cảnh'),
    (r'\bcành\b', 'cảnh'),
    (r'\btôm tắt\b', 'tóm tắt'),
    (r'\btóm tát\b', 'tóm tắt'),
    (r'\btơm tắt\b', 'tóm tắt'),
    (r'\bTôm tắt\b', 'Tóm tắt'),
    (r'\bbải báo\b', 'bài báo'),
    (r'\bbải toán\b', 'bài toán'),
    (r'\bbải tập\b', 'bài tập'),
    (r'\bbải học\b', 'bài học'),
    (r'\bbải nghị luận\b', 'bài nghị luận'),
    (r'\bbài nghi luận\b', 'bài nghị luận'),
    (r'\bbải viết\b', 'bài viết'),
    (r'\bbải phân tích\b', 'bài phân tích'),
    (r'\bbải thuyết trình\b', 'bài thuyết trình'),
    (r'\bbải hát\b', 'bài hát'),
    (r'\bbải\b', 'bài'),
    (r'\bgiài thích\b', 'giải thích'),
    (r'\bgiài bài\b', 'giải bài'),
    (r'\bgiái bài\b', 'giải bài'),
    (r'\bgiài toán\b', 'giải toán'),
    (r'\bgiài đúng\b', 'giải đúng'),
    (r'\bLời giài\b', 'Lời giải'),
    (r'\blời giài\b', 'lời giải'),
    (r'\bdiễn giài\b', 'diễn giải'),
    (r'\bgiài\b', 'giải'),
    (r'\bcầu giài\b', 'cầu giải'),
    (r'\bHây giài thịch\b', 'Hãy giải thích'),
    (r'\bHấy giải thích\b', 'Hãy giải thích'),
    (r'\bHấy suy luận\b', 'Hãy suy luận'),
    (r'\bHây\b', 'Hãy'),
    (r'\bHấy\b', 'Hãy'),
    (r'\bthịch\b', 'thích'),
    (r'\bvăn bán\b', 'văn bản'),
    (r'\bvắn bản\b', 'văn bản'),
    (r'\bdừ liệu\b', 'dữ liệu'),
    (r'\bmục liêu\b', 'mục tiêu'),
    (r'\bý tường\b', 'ý tưởng'),
    (r'\btừng tiêu chi\b', 'từng tiêu chí'),
    (r'\bsáu tiêu chi\b', 'sáu tiêu chí'),
    (r'\bKét quả\b', 'Kết quả'),
    (r'\bbất ki\b', 'bất kì'),
    (r'\bhọc bồng\b', 'học bổng'),
    (r'\btrài qua\b', 'trải qua'),
    (r'\btạo ành\b', 'tạo ảnh'),
    (r'\bSeli-Attention\b', 'Self-Attention'),
    (r'\bsách vờ\b', 'sách vở'),
    (r'\btuần theo\b', 'tuân theo'),
    (r'\bMáy tinh\b', 'Máy tính'),
    (r'\bchíp\b', 'chip'),
    (r'\bchịp\b', 'chip'),
    (r'\bhọc cùng cố\b', 'học củng cố'),
    (r'\bthi LLM\b', 'thì LLM'),
    (r'\bCâu hòi\b', 'Câu hỏi'),
    (r'\bHòi sau\b', 'Hỏi sau'),
    (r'\bHỗi LLM\b', 'Hỏi LLM'),
    (r'\bnhầm tài liệu\b', 'nhầm tài liệu'),
    (r'\bphù định\b', 'phủ định'),
    (r'\btừ khoa\b', 'từ khóa'),
    (r'\bmỗi làn\b', 'mỗi lần'),
    (r'\bkịch bàn\b', 'kịch bản'),
    (r'\bchuyên động\b', 'chuyển động'),
    (r'\bchât lượng\b', 'chất lượng'),
    (r'\bban bàn tán\b', 'bạn bàn tán'),
    (r'\bvê khói\b', 'về khói'),
    (r'\bbạn bé\b', 'bạn bè'),
    (r'\btim kiếm\b', 'tìm kiếm'),
    (r'\btim dược\b', 'tìm được'),
    (r'\bkiêm chứng\b', 'kiểm chứng'),
    (r'\bbố sung\b', 'bổ sung'),
    (r'\bsô liệu\b', 'số liệu'),
    (r'\bphai đọc\b', 'phải đọc'),
    (r'\bphần tích\b', 'phân tích'),
    (r'\bmô tá\b', 'mô tả'),
    (r'\bmảu\b', 'mẫu'),
    (r'\bHoa sĩ\b', 'Họa sĩ'),
    (r'\bbàn phim\b', 'bàn phím'),
    (r'\bchỉ tiết\b', 'chi tiết'),
    (r'\bphần từ\b', 'phần tử'),
    (r'\bgáp 2 lăn só trước\b', 'gấp 2 lần số trước'),
    (r'\bgáp 2 lăn\b', 'gấp 2 lần'),
    (r'\bgáp 2\b', 'gấp 2'),
    (r'\blăn só\b', 'lần số'),
    (r'\bdữ liệu đâu vào\b', 'dữ liệu đầu vào'),
    (r'\bđâu vào\b', 'đầu vào'),
    (r'\bphức lạp\b', 'phức tạp'),
    (r'\bcàn độ\b', 'cần độ'),
    (r'\bChuối tư duy\b', 'Chuỗi tư duy'),
    (r'\bTôc độ thưc hiện\b', 'Tốc độ thực hiện'),
    (r'\bTôc độ\b', 'Tốc độ'),
    (r'\bthurc hiện\b', 'thực hiện'),
    (r'\bCẦU TRÚC\b', 'CẤU TRÚC'),
    (r'\bCầu trúc\b', 'Cấu trúc'),
    (r'\bcầu trúc\b', 'cấu trúc'),
    (r'\bGiá sử\b', 'Giả sử'),
    (r'\bhằng quý\b', 'hàng quý'),
    (r'\bcà vốn lẫn lãi\b', 'cả vốn lẫn lãi'),
    (r'\bkhông ai cà\b', 'không ai cả'),
    (r'\bcà hai bên\b', 'cả hai bên'),
    (r'\btất cà các\b', 'tất cả các'),
    (r'\bsoạn thào\b', 'soạn thảo'),
    (r'\btheo A:\b', 'theo Δ:'),
    (r'x\?\s*\+\s*4x\s*\+\s*3', 'x² + 4x + 3'),
    (r'x2\s*\+\s*4x\s*\+\s*3', 'x² + 4x + 3'),
    (r'\bXác đinh\b', 'Xác định'),
    (r'\bTinh 4;\b', 'Tính Δ;'),
    (r'\bTinh 4\b', 'Tính Δ'),
    (r'\bđoan thơ\b', 'đoạn thơ'),
    (r'\bđoan văn\b', 'đoạn văn'),
    (r'\bmục đich\b', 'mục đích'),
    (r'\bLàm thể nào\b', 'Làm thế nào'),
    (r'\bchủ ý điều gì\b', 'chú ý điều gì'),
    (r'\bbản nghị luàn\b', 'bài nghị luận'),
    (r'\bLƯU THÊ SƠN\b', 'LƯU THẾ SƠN'),
    (r'\bmở rông\b', 'mở rộng'),
    (r'\bnghỉa\b', 'nghĩa'),
    (r'\bgiắc mơ\b', 'giấc mơ'),
    (r'\bô lõ\b', 'ô tô'),
    (r'\bđàng nhớ\b', 'đáng nhớ'),
    (r'\bTrí tuê\b', 'Trí tuệ'),
    (r'\bChức năng nhan dang\b', 'Chức năng nhận dạng'),
    (r'\bnhan dang\b', 'nhận dạng'),
    (r'\bthong_tin_tim kiem\b', 'thong_tin_tim_kiem'),
    (r'\brờ\b', 'rõ'),
    (r'\blôi\b', 'lỗi'),
    (r'\bdũ bậu\b', 'dữ liệu'),
    (r'\bso vai ko nao\b', 'so với cái nào'),
    (r'\bquản trong\b', 'quan trọng'),
    (r'\bphát hiên\b', 'phát hiện'),
    (r'\bhuân luyên\b', 'huấn luyện'),
    (r'\btrom\b', 'trong'),
    (r'\b1lms\b', 'LLMs'),
    (r'\bLiệt kệ:\b', 'Liệt kê:'),
    (r'\bHãy liệt kè\b', 'Hãy liệt kê'),
    (r'\bTiều chí\b', 'Tiêu chí'),
    (r'\bngân hàng trực tuyển\b', 'ngân hàng trực tuyến'),
    (r'\btuy chọn\b', 'tùy chọn'),
    (r'\btưy chọn\b', 'tùy chọn'),
    (r'\bMột hoặc một vải ví dụ\b', 'Một hoặc một vài ví dụ'),
    (r'\bvải ví dụ\b', 'vài ví dụ'),
    (r'\bPrompt không ví dự:\b', 'Prompt không ví dụ:'),
    (r'\bbao nhiêu tinh, thành\b', 'bao nhiêu tỉnh, thành'),
    (r'\btheo lừng bước\b', 'theo từng bước'),
    (r'\bChi thị:\b', 'Chỉ thị:'),
    (r'\bmô hình cần xử II\.\b', 'mô hình cần xử lí.'),
    (r'\bhàng fỉ tế bào\b', 'hàng tỉ tế bào'),
    (r'\bchẳng chịt\b', 'chằng chịt'),
    (r'\btin hiệu\b', 'tín hiệu'),
    (r'\bnhiệt độ co thể\b', 'nhiệt độ cơ thể'),
    (r'\bđiều chình\b', 'điều chỉnh'),
    (r'\bdưa ra kết quả\b', 'đưa ra kết quả'),
    (r'\bdứ liệu đầu vào\b', 'dữ liệu đầu vào'),
    (r'\bhọc lăng cường\b', 'học tăng cường'),
    (r'\bhọc có giảm sát\b', 'học có giám sát'),
    (r'\bmỏ phòng cách con người\b', 'mô phỏng cách con người'),
    (r'\bthư điện từ\b', 'thư điện tử'),
    (r'\bmiến phí\b', 'miễn phí'),
    (r'\btrứng thường\b', 'trúng thưởng'),
    (r'\bnguồn gừi\b', 'nguồn gửi'),
    (r'\bbước tiền\b', 'bước tiến'),
    (r'\bhòi thời tiết\b', 'hỏi thời tiết'),
    (r'\bsờ thích\b', 'sở thích'),
    (r'\bphù hợp nhật\b', 'phù hợp nhất'),
    (r'\btrước đỏ\b', 'trước đó'),
    (r'\byếu tổ phức lạp\b', 'yếu tố phức tạp'),
    (r'\byếu tổ không mong muốn\b', 'yếu tố không mong muốn'),
    (r'\byếu tổ\b', 'yếu tố'),
    (r'\bgial điệu và tâm bạng của bài hảt\b', 'giai điệu và tâm trạng của bài hát'),
    (r'\bkíp thời\b', 'kịp thời'),
    (r'\bcây gia phá\b', 'cây gia phả'),
    (r'\bchúng ta tháy được\b', 'chúng ta thấy được'),
    (r'\bvề đạo dúr\. pháp luật và vẫn hóa\b', 'về đạo đức, pháp luật và văn hóa'),
    (r'\bxu hưởng\b', 'xu hướng'),
    (r'\bgiới tinh\b', 'giới tính'),
    (r'"tấm bàn đồ"', '"tấm bản đồ"'),
    (r'\bGiáo dục phố thông\b', 'Giáo dục phổ thông'),
    (r'\bđể làm g1\?\b', 'để làm gì?'),
    (r'\bChinh những lựa chọn\b', 'Chính những lựa chọn'),
    (r'\bchinh những\b', 'chính những'),
    (r'\bNhà đó, Bình\b', 'Nhờ đó, Bình'),
    (r'\btử vựng mới\b', 'từ vựng mới'),
    (r'\bcài thiện khả năng\b', 'cải thiện khả năng'),
    (r'ax\'\s*\+\s*bx\s*\+\s*c\s*=\s*0', 'ax² + bx + c = 0'),
    (r'ax\?\s*\+\s*bx\s*\+\s*c\s*=\s*0', 'ax² + bx + c = 0'),
    (r'dầu ":"', 'dấu ":"'),
    (r'\bAnh sáng:\b', 'Ánh sáng:'),
    (r'\bánh hường tới không khi\b', 'ảnh hưởng tới không khí'),
    (r'\bGoogle AI Sludio\b', 'Google AI Studio'),
    (r'\bHoa tinh\b', 'Hỏa tinh'),
    (r'\bquý đạo các hành tinh\b', 'quỹ đạo các hành tinh'),
    (r'\bquỳ đạo\b', 'quỹ đạo'),
    (r'\bthực hiện bằng chinh LLM\b', 'thực hiện bằng chính LLM'),
    (r'\bsao chỗi\b', 'sao chổi'),
    (r'\bbên trong ánh\b', 'bên trong ảnh'),
    (r'\bNhảy chuột chọn\b', 'Nháy chuột chọn'),
    (r'\bnhấn tổ hợp phim\b', 'nhấn tổ hợp phím'),
    (r'chọn nú! Generate Media, liếp theo chon Veo \(Hình 124\)\.', 'chọn nút Generate Media, tiếp theo chọn Veo (Hình 12.4).'),
    (r'\bbên dười là đồ thị thể hiện lì độ\b', 'bên dưới là đồ thị thể hiện li độ'),
    (r'Không tiếng ổn" vào ở Prompt', 'Không tiếng ồn" vào ô Prompt'),
    (r'\bđiện từ của co quan\b', 'điện tử của cơ quan'),
    (r'\bbảo cáo nghiên cứu\b', 'báo cáo nghiên cứu'),
    (r'\bbảng cách gợi ý từ khoa\b', 'bằng cách gợi ý từ khóa'),
    (r'\bhiểu sàu vẫn đề và tạo dầu ấn\b', 'hiểu sâu vấn đề và tạo dấu ấn'),
    (r'\bnhững sàn phẩm này\b', 'những sản phẩm này'),
    (r'\bNHÀ XUÁT BẢN\b', 'NHÀ XUẤT BẢN'),
    (r'\bLỚNỮ LỚN\b', 'LỚN'),
    (r'\bchía nhỏ\b', 'chia nhỏ'),
    (r'\btò mò hồi:\b', 'tò mò hỏi:'),
    (r'\bchuyến dã ngoạ\b', 'chuyến dã ngoại'),
    (r'\bkhi cân\b', 'khi cần'),
    (r'\bdựa trên do liệu huấn\b', 'dựa trên dữ liệu huấn'),
    (r'\bThực Hiện nhiệm vu tư đồng\b', 'Thực hiện nhiệm vụ tự động'),
    (r'\bRs quyết đinh thông minh\b', 'Ra quyết định thông minh'),
    (r'\bauay lai bước 2 để tiếp tục chu trinh\b', 'quay lại bước 2 để tiếp tục chu trình'),
    (r'\bLập luận/Lập kê hoạch\b', 'Lập luận/Lập kế hoạch'),
    (r'\bkết quả tìm kiêm\b', 'kết quả tìm kiếm'),
    (r'\bđược đề cập trong huân luyện\b', 'được đề cập trong huấn luyện'),
    (r'\bthường cân truy cập\b', 'thường cần truy cập'),
    (r'\bcó thề làm thay đổi\b', 'có thể làm thay đổi'),
    (r'\bviệc tim kiếm\b', 'việc tìm kiếm'),
    (r'\bCông cụ no-code/low-code trọng AI Agent\b', 'Công cụ no-code/low-code trong AI Agent'),
    (r'\bDenerate Text\b', 'Generate Text'),
    (r'\bbehalt of user\b', 'behalf of user'),
    (r'\bDsta Sources\b', 'Data Sources'),
    (r'\bUsor Inputs\b', 'User Inputs'),
    (r'\bMain\.fow\b', 'Main.flow'),
    (r'\bOvervien\b', 'Overview'),
    (r'cài đặt chung cho Agen cúa em:', 'cài đặt chung cho Agent của em:'),
    (r'\bTransoribe Audio\b', 'Transcribe Audio'),
    (r'\bColleci data\b', 'Collect data'),
    (r'\bPrompt cơ bản = \s*\+ \[Dữ liệu đầu vào\]\.', 'Prompt cơ bản = [Chỉ thị] + [Dữ liệu đầu vào].'),
    (r'Prompt cơ bản = \+ \[Dữ liệu đầu vào\]\.', 'Prompt cơ bản = [Chỉ thị] + [Dữ liệu đầu vào].'),
    (r'Prompt cơ bàn = \+ \[Dữ liệu đầu vào\]\.', 'Prompt cơ bản = [Chỉ thị] + [Dữ liệu đầu vào].'),
    (r'Prompt nâng cao = \+ \[Vi dụ\]\* \+ \[Ngữ cành\]\* \+ \[Dữ liệu đầu vào\]', 'Prompt nâng cao = [Chỉ thị] + [Ví dụ]* + [Ngữ cảnh]* + [Dữ liệu đầu vào]'),
    (r'Prompt nâng cao =   \+ \[Vi dụ\]\* \+ \[Ngữ cành\]\*', 'Prompt nâng cao = [Chỉ thị] + [Ví dụ]* + [Ngữ cảnh]*'),
    (r'Prompt nâng cao = \+ \[Ví dụ\]\* \+ \[Ngữ cảnh\]\* \+ \[Dữ liệu đầu vào\]', 'Prompt nâng cao = [Chỉ thị] + [Ví dụ]* + [Ngữ cảnh]* + [Dữ liệu đầu vào]'),
    (r'\bBảng 1\.1\. So sánh prompt co bản và prompt nàng cao\b', 'Bảng 1.1. So sánh prompt cơ bản và prompt nâng cao'),
    (r'\bBảng 1\.1\. So sánh prompt cơ bản và prompt nàng cao\b', 'Bảng 1.1. So sánh prompt cơ bản và prompt nâng cao'),
    (r'\bkhống lồ\b', 'khổng lồ'),
    (r'\btiền hành qua\b', 'tiến hành qua'),
    (r'\bchuyên mỗn\b', 'chuyên môn'),
    (r'cos2x\s*-\s*cosx\s*=\s*0', 'cos 2x - cos x = 0'),
    (r'sinx\s*\+\s*cos2x\s*=\s*0', 'sin x + cos 2x = 0'),
    (r'\bĐiều khoảnsử dụng\b', 'Điều khoản sử dụng'),
    (r'\bđiều khoảnsử dụng\b', 'điều khoản sử dụng'),
    (r'\bHiếu được text-to-video\b', 'Hiểu được text-to-video'),
    (r'\bnội dụng mong muốn\b', 'nội dung mong muốn'),
    (r'\btính nắng Search the web\b', 'tính năng Search the web'),
    (r'"iều lượng thuốc cảm" không chừa', '"Liều lượng thuốc cảm" không chứa'),
    (r'\bAsk enything\b', 'Ask anything'),
    (r'\bGreate an image\b', 'Create an image'),
    (r'\bWnite or code\b', 'Write or code'),
    (r'\bThink for langer\b', 'Think for longer'),
    (r'\bquan sại\b', 'quan sát'),
    (r'\bsử dung\b', 'sử dụng'),
    (r'\bSupervised Learing\b', 'Supervised Learning'),
    (r'\bReinforcement Leaming\b', 'Reinforcement Learning'),
    (r'\blự nhận thức\b', 'tự nhận thức'),
    (r'\blự khám phá\b', 'tự khám phá'),
    (r'\blự động\b', 'tự động'),
    (r'\bThay vi tự\b', 'Thay vì tự'),
    (r'phân phối xác suất hình chuỗng', 'phân phối xác suất hình chuông'),
    (r'Tì lệ tương lác nói dung "Tìn sức - loần thọc"', 'Tỉ lệ tương tác nội dung "Tin tức - Kiến thức"'),
    (r'Tỉ tường tác nói dùng "Giái tí"', 'Tỉ lệ tương tác nội dung "Giải trí"'),
    (r'T lộ tương tác nội dung "Tin tức - Kiến thừc', 'Tỉ lệ tương tác nội dung "Tin tức - Kiến thức"'),
    (r'phần Khởí động', 'phần Khởi động'),
    (r'\bvấn để liên quan\b', 'vấn đề liên quan'),
    (r'\bnghệ thuât\b', 'nghệ thuật'),
    (r'\bpháp luât\b', 'pháp luật'),
    (r'\bxừa\b', 'xưa'),
    (r'\bđủ/sai\b', 'đúng/sai'),
    (r'\bđù/sai\b', 'đúng/sai'),
    (r'\blập trung\b', 'tập trung'),
    (r'\bchuân\b', 'chuẩn'),
    (r'\bmổi\b', 'mỗi'),
    (r'\blổi\b', 'lỗi'),
    (r'\bchử\b', 'chữ')
]

def clean_text_with_rules(text):
    if not text:
        return text
    current = text
    for pat, repl in GLOBAL_REPLACEMENTS:
        current = re.sub(pat, repl, current)
    return current

def clean_data_structure(data):
    if isinstance(data, str):
        return clean_text_with_rules(data)
    elif isinstance(data, list):
        return [clean_data_structure(it) for it in data]
    elif isinstance(data, dict):
        return {k: clean_data_structure(v) for k, v in data.items()}
    return data

def process_books_json():
    bp = DATA_DIR / "books.json"
    with open(bp, encoding="utf-8") as f:
        books_data = json.load(f)
    cleaned = clean_data_structure(books_data)
    with open(bp, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print("Updated data/books.json")

def process_book_lessons(book_id):
    lp = DATA_DIR / f"lessons-{book_id}.json"
    with open(lp, encoding="utf-8") as f:
        lessons_data = json.load(f)
        
    cleaned_lessons = clean_data_structure(lessons_data)
    
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(cleaned_lessons, f, ensure_ascii=False, indent=2)
    print(f"Updated {lp}")
    
    # Also update static HTML files in lessons/<book_id>/*.html
    html_dir = LESSONS_DIR / book_id
    if html_dir.exists():
        # Map by id
        lesson_map = {les["id"]: les.get("html", "") for les in cleaned_lessons}
        for html_file in html_dir.glob("*.html"):
            stem = html_file.stem
            if stem in lesson_map:
                # Read file, check if it's full document or just snippet
                content = html_file.read_text(encoding="utf-8")
                cleaned_content = clean_text_with_rules(content)
                html_file.write_text(cleaned_content, encoding="utf-8")
        print(f"Updated static HTML files in {html_dir}")

def rebuild_search_indexes():
    for b in ["lop-10", "lop-11", "lop-12"]:
        lp = DATA_DIR / f"lessons-{b}.json"
        sp = DATA_DIR / f"search-{b}.json"
        
        lessons = json.loads(lp.read_text(encoding="utf-8"))
        search_data = []
        
        for item in lessons:
            html = item.get("html", "")
            # Strip HTML tags
            clean_text = re.sub(r"<[^>]+>", " ", html)
            clean_text = re.sub(r"\s+", " ", clean_text).strip()
            
            # Combine title, group, and content
            full_content = f"{item.get('group', '')} {item.get('title', '')} {clean_text}".strip()
            full_content = re.sub(r"\s+", " ", full_content)
            
            search_data.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "group": item.get("group"),
                "startPage": item.get("startPage", 1),
                "content": full_content
            })
        
        sp.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Rebuilt {sp} with {len(search_data)} entries.")

print("Starting master deep fix across all 3 books...")
process_books_json()
process_book_lessons("lop-10")
process_book_lessons("lop-11")
process_book_lessons("lop-12")
rebuild_search_indexes()
print("Master deep fix complete!")
