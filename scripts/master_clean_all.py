import json
import re
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Exact string replacements (applied in order)
exact_replacements = [
    # Books.json specific summaries
    ("BẬI 3. HIỀU ĐÙNG VỀ AI TẠO SINH: THIÊN VỊ HIỀU LẬM VÀ TÁC HẠI VỚI CON NGƯỜI",
     "BÀI 8. HIỂU ĐÚNG VỀ AI TẠO SINH: THIÊN VỊ, HIỂU LẦM VÀ TÁC HẠI VỚI CON NGƯỜI"),
    ("l 5 Prompt - Giao tiếp với AI lạo sinh Bòi 6 ÀI tạo sinh hỗ trợ học",
     "Bài 5 Prompt - Giao tiếp với AI tạo sinh. Bài 6 AI tạo sinh hỗ trợ học"),
    ("tinh huóng xuất hiện trong cuộc sống", "tình huống xuất hiện trong cuộc sống"),
    ("không vl dụ", "không ví dụ"),
    ("không v1 dụ", "không ví dụ"),
    ("không vi dụ", "không ví dụ"),
    ("prompt không vl dụ", "prompt không ví dụ"),
    ("prompt là gi", "prompt là gì"),
    ("làm gi", "làm gì"),
    ("Làm gi", "Làm gì"),
    ("có gi đỏ không ổn", "có gì đó không ổn"),
    ("có gi không ổn", "có gì không ổn"),
    ("đỏ không ổn", "đó không ổn"),
    
    # Lop 10 specific OCR headers and fixes
    ("BÂI 4: DỮ LIỆU HUẬN LUYỆN", "BÀI 4: DỮ LIỆU HUẤN LUYỆN"),
    ("Bòl 4 Dữ liệu huán luyện", "Bài 4 Dữ liệu huấn luyện"),
    ("Bàl 7 Phần biệt thật - giò trong AI tạo sin", "Bài 7 Phân biệt thật - giả trong AI tạo sinh"),
    ("BẬI 3. HIỀU ĐÙNG VỀ AI TẠO SINH", "BÀI 8. HIỂU ĐÚNG VỀ AI TẠO SINH"),
    ("HIỀU ĐÙNG VỀ AI TẠO SINH", "HIỂU ĐÚNG VỀ AI TẠO SINH"),
    ("HIỀU LẬM VÀ TÁC HẠI", "HIỂU LẦM VÀ TÁC HẠI"),
    ("HIỀU LẬM", "HIỂU LẦM"),
    ("Môt số công cụ AI tạo sinh", "Một số công cụ AI tạo sinh"),
    ("yều cầu cho ChatGPT", "yêu cầu cho ChatGPT"),
    ("âm thanh mởi", "âm thanh mới"),
    ("yêu câu khá giống", "yêu cầu khá giống"),
    ("yêu câu", "yêu cầu"),
    ("Diêu này cho thây", "Điều này cho thấy"),
    ("có sản", "có sẵn"),
    ("vân bản", "văn bản"),
    ("đựa trên mô tả", "dựa trên mô tả"),
    ("bắng AI tạo sinh", "bằng AI tạo sinh"),
    ("hướng dẫn (hực hành", "hướng dẫn thực hành"),
    ("minh thấy phù hợp", "mình thấy phù hợp"),
    ("đại Aần chuân bị những kĩ nằng gì để theo đuối", "lại cần chuẩn bị những kĩ năng gì để theo đuổi"),
    ("đại Aần chuân bị", "lại cần chuẩn bị"),
    ("theo đuối", "theo đuổi"),
    ("bó cục hợp lí", "bố cục hợp lí"),
    ("prompt dể đảm bèo", "prompt để đảm bảo"),
    ("đảm bèo", "đảm bảo"),
    ("hai hoà với", "hài hòa với"),
    ("Tẹo một búc tranh", "Tạo một bức tranh"),
    ("cung đỉnh xưa", "cung đình xưa"),
    ("cá nhãn", "cá nhân"),
    ("bào vệ dữ liệu", "bảo vệ dữ liệu"),
    ("báo vệ dữ liệu", "bảo vệ dữ liệu"),
    ("mội trường số", "môi trường số"),
    ("nôi dung", "nội dung"),
    ("thục hành", "thực hành"),
    ("bài tạp", "bài tập"),
    ("Kẻ tên một số", "Kể tên một số"),
    ("Kẻ tên", "Kể tên"),
    ("bái viết do AI", "bài viết do AI"),
    ("thay đồi nội dung", "thay đổi nội dung"),
    ("Thay đồi prompt", "Thay đổi prompt"),
    ("thay đồi prompt", "thay đổi prompt"),
    ("thay đồi", "thay đổi"),
    ("Thay đồi", "Thay đổi"),
    ("Ạl tạo sinh", "AI tạo sinh"),
    ("lạo sinh", "tạo sinh"),
    ("Ai thô hệ trước", "AI thế hệ trước"),
    ("A/ lạo sinh", "AI tạo sinh"),
    ("công củ AI", "công cụ AI"),
    ("tao ra nội dung", "tạo ra nội dung"),
    ("tao ra sản phẩm", "tạo ra sản phẩm"),

    # Lop 11 specific OCR headers and fixes
    ("CHỦ ĐẺ 3", "CHỦ ĐỀ 3"),
    ("BÁNG GIẢI THÍCH THUẬT NGỮ", "BẢNG GIẢI THÍCH THUẬT NGỮ"),
    ("BÁI 4. GIỚI THIÊU VỀ RAG", "BÀI 4. GIỚI THIỆU VỀ RAG"),
    ("đểgian lận", "để gian lận"),
    ("đượcdùng đểhuẩn luyện", "được dùng để huấn luyện"),
    ("đưa ra   những đề xuất", "đưa ra những đề xuất"),
    ("đừa ra", "đưa ra"),
    ("Đừng dưa vào", "Đừng dựa vào"),
    ("Đậy là một", "Đây là một"),
    ("nhóm nào đổ hay", "nhóm nào đó hay"),
    ("mỗi đôi tượng sẽ được biêu điẻn", "mỗi đối tượng sẽ được biểu diễn"),
    ("bèn cung cấp", "bên cung cấp"),
    ("xoa bót bốn", "xóa bớt bốn"),
    ("gia đình bón người", "gia đình bốn người"),
    ("tài liệu bén ngoài", "tài liệu bên ngoài"),
    ("lài liệu", "tài liệu"),
    ("cảm xúc Buốn", "cảm xúc Buồn"),
    ("em bị ổm", "em bị ốm"),
    ("Khời động", "Khởi động"),
    ("khời động", "khởi động"),
    ("hãng quý", "hàng quý"),
    ("Gia sử sau", "Giả sử sau"),
    ("Gia sử", "Giả sử"),
    ("tìm hiều kì", "tìm hiểu kĩ"),
    ("AI hiều", "AI hiểu"),
    ("giúp em hiều", "giúp em hiểu"),
    ("Hiều, không sao chép", "Hiểu, không sao chép"),

    # Lop 12 specific OCR headers and fixes
    ("BÁI 1. GIỚI THIÊU VÊ AI AGENTS", "BÀI 1. GIỚI THIỆU VỀ AI AGENTS"),
    ("Sinh và tiều vận bân tự nhiện", "Sinh và hiểu văn bản tự nhiên"),
    ("Vê tinh minh bach, doi khi rát kho để hiểu cach thic AI da da quyết định hoặc liu lá nội dung. Các mô hình AI phức lạp thường hoạt động như một \"hộp đen\".",
     "Về tính minh bạch, đôi khi rất khó để hiểu cách thức AI đưa ra quyết định hoặc tạo ra nội dung. Các mô hình AI phức tạp thường hoạt động như một \"hộp đen\"."),
    ("Ahiển chùng la không rô vì sao chùng lại làm như vậy. Ví dụ, nêu một ứng dụng\n\n\nAi tựr động chấm điểm bài tập của em, em có thể không hiều vì sao minh lại Arư điêm đo hay vì sao một câu trẻ lời cụ thể bị đành giá là sai. Diều này gây Nho khân trong việc kiểm tra tinh công bằng, phát hiện sai sót và xây dựng niềm In Vào hệ thống AI.",
     "nghĩa là chúng ta không rõ vì sao chúng lại làm như vậy. Ví dụ, nếu một ứng dụng AI tự động chấm điểm bài tập của em, em có thể không hiểu vì sao mình lại được điểm đó hay vì sao một câu trả lời cụ thể bị đánh giá là sai. Điều này gây khó khăn trong việc kiểm tra tính công bằng, phát hiện sai sót và xây dựng niềm tin vào hệ thống AI."),
    ("Ahiển chùng la không rô vì sao chùng lại làm như vậy. Ví dụ, nêu một ứng dụng Ai tựr động chấm điểm bài tập của em, em có thể không hiều vì sao minh lại Arư điêm đo hay vì sao một câu trẻ lời cụ thể bị đành giá là sai. Diều này gây Nho khân trong việc kiểm tra tinh công bằng, phát hiện sai sót và xây dựng niềm In Vào hệ thống AI.",
     "nghĩa là chúng ta không rõ vì sao chúng lại làm như vậy. Ví dụ, nếu một ứng dụng AI tự động chấm điểm bài tập của em, em có thể không hiểu vì sao mình lại được điểm đó hay vì sao một câu trả lời cụ thể bị đánh giá là sai. Điều này gây khó khăn trong việc kiểm tra tính công bằng, phát hiện sai sót và xây dựng niềm tin vào hệ thống AI."),
    ("Gòm các văn đề như thiên vị", "Gồm các vấn đề như thiên vị"),
    ("Ddes tir vito erito tk: vià Aí nàng AI. UnI tiên cức môn học, khóa học về AI hoặc", "• Đầu tư vào kiến thức và kĩ năng AI: Ưu tiên các môn học, khóa học về AI hoặc"),
    ("do lit quer th ha nghe só ngay tr bay did hoặc khi vào đại học.", "công nghệ số ngay từ bây giờ hoặc khi vào đại học."),
    ("Pral tren tir đin sinh tuva vàt sẵn sửng thịch nghi: Chuẩn bị tình thần cho sự", "• Phát triển tư duy linh hoạt và sẵn sàng thích nghi: Chuẩn bị tinh thần cho sự"),
    ("may sti he tr chd ah nuné va săn sang học cái mói.", "thay đổi liên tục và sẵn sàng học cái mới."),
    ("TheM git cA 1 V2 918 1N08 Ah0d, dur ân AI: Tìm kiểm cơ hội trải nghiệm thực", "• Tham gia các câu lạc bộ, dự án AI: Tìm kiếm cơ hội trải nghiệm thực tế"),
    ("té rori AI dể mier vat viện tang nó vào cức dự ăn cá nhân hoặc nhỏm.", "với AI để nắm vững và vận dụng nó vào các dự án cá nhân hoặc nhóm."),
    ("Hạc hỏi tn củng đổng và chuyền gia: Tham gia các nhóm, diễn đàn về AI đề trao", "• Học hỏi từ cộng đồng và chuyên gia: Tham gia các nhóm, diễn đàn về AI để trao"),
    ("Bỏi khên thic và kinh nghệm với bạn bè, thầy có, chuyên gia.", "đổi kiến thức và kinh nghiệm với bạn bè, thầy cô, chuyên gia."),
    ("18 ng thường g lài só cng h ch gi?\n\nbảo hiếm sức khỏẻ với mức phí cao hơn cho nhóm này.",
     "động) và từ chối bán bảo hiểm hoặc chào bán gói bảo hiểm sức khỏe với mức phí cao hơn cho nhóm này."),
    ("18 ng thường g lài só cng h ch gi? bảo hiếm sức khỏẻ với mức phí cao hơn cho nhóm này.",
     "động) và từ chối bán bảo hiểm hoặc chào bán gói bảo hiểm sức khỏe với mức phí cao hơn cho nhóm này."),
    ("18 ng thường g lài só cng h ch gi?", ""),
    ("bảo hiếm sức khỏẻ", "bảo hiểm sức khỏe"),
    ("9. Hat ượng bải loán Học mây cợ bản a) Hôl quy (Koy/oes/on)", "2. Hai dạng bài toán Học máy cơ bản - a) Hồi quy (Regression)"),
    ("Đảu nhất bài toàn Hòi quy", "• Bản chất bài toán Hồi quy"),
    ("LÀ bàt luàn dự doân giá li) số liên luo (contnuovo valua)", "Là bài toán dự đoán giá trị số liên tục (continuous value)."),
    ("KÁI QUA ân rà luôn ở dạng số (sở nguyên hoặc só thụế)", "Kết quả đầu ra luôn ở dạng số (số nguyên hoặc số thực)."),
    ("Mục liêu: Hin mốt quan hệ loán học giờa sác biên đầu vào và đầu ra", "Mục tiêu: Tìm mối quan hệ toán học giữa các biến đầu vào và đầu ra."),
    ("Hội quy hoạt động bậng sách xây dụng một mô hình loận học du đoán đầu ra", "Hồi quy hoạt động bằng cách xây dựng một mô hình toán học dự đoán đầu ra"),
    ("Lam sach, chuyển đốt và", "Làm sạch, chuyển đổi và"),
    ("Tiền xử II d0 liệu", "Tiền xử lí dữ liệu"),
    ("Chia tập d0 liệu", "Chia tập dữ liệu"),
    ("Biss cao", "Bias cao"),
    ("DO Bộu thiêu", "Dữ liệu thiếu"),
    ("Outiers", "Outliers"),
    ("Undetfitting", "Underfitting"),
    ("Chậm hội tư", "Chậm hội tụ"),
    ("Thiểu random", "Thiếu random"),
    ("Thiều RAM", "Thiếu RAM"),
    ("Đường hòi quy tối ưu: y = {w: .2f]-x + (b: .2f)", "Đường hồi quy tối ưu: y = {w:.2f}*x + {b:.2f}"),
    ("5ố giờ hoc", "Số giờ học"),
    ("Bạn muốn hói gi vé sán phẩm?", "Bạn muốn hỏi gì về sản phẩm?"),
    ("Bạn muốn hói gi", "Bạn muốn hỏi gì"),
    ("vé sán phẩm?", "về sản phẩm?"),
    ("vé sán phẩm", "về sản phẩm"),
    ("sán phẩm", "sản phẩm"),
    ("Nhập càu hỏi của khác", "Nhập câu hỏi của khách"),
    ("càu hỏi", "câu hỏi"),
    ("càu trả lời", "câu trả lời"),
    ("cầu hói", "câu hỏi"),
    ("câu hói", "câu hỏi"),
    ("yêu càu", "yêu cầu"),
    ("yêu càu độ", "yêu cầu độ"),
    ("hói của khác", "hỏi của khách"),
    ("của khác", "của khách"),
    ("thong_tin_tio_kiem", "thong_tin_tim_kiem"),
    ("f[thong_tin_tio_kiem]", "f[thong_tin_tim_kiem]"),
    ("Hảy trả lời", "Hãy trả lời"),
    ("hảy trả lời", "hãy trả lời"),
    ("trà lời", "trả lời"),
    ("Trà lời", "Trả lời"),
    ("cài tiến", "cải tiến"),
    ("Cài tiến", "Cải tiến"),
    ("nhớ vậy, càu trả lời", "nhờ vậy, câu trả lời"),
    ("nhớ vậy,", "nhờ vậy,"),
    ("Nhớ vậy,", "Nhờ vậy,"),
    ("Khuyến mãt tháng 6 la gi", "Khuyến mãi tháng 6 là gì"),
    ("Khuyến mãt", "Khuyến mãi"),
    ("buợc hành động tiêp theo", "bước hành động tiếp theo"),
    ("buợc hành động", "bước hành động"),
    ("tiêp theo", "tiếp theo"),
    ("lại nguyên và", "tài nguyên và"),
    ("lài nguyên", "tài nguyên"),
    ("Tái sự dụng", "Tái sử dụng"),
    ("lãng phi", "lãng phí"),
    ("không chi tồn tại", "không chỉ tồn tại"),
    ("không chi", "không chỉ"),
    ("đàm bào cảo vấn đề", "đảm bảo các vấn đề"),
    ("đàm bào", "đảm bảo"),
    ("càn am gi để", "cần làm gì để"),
    ("Ap dung cho rds sin phám AI sir dung ki thuda RAG (Netseval-Augmented Generation) để truy xuất thông tin từ ngưồn kiến thức riêng",
     "Áp dụng cho các sản phẩm AI sử dụng kĩ thuật RAG (Retrieval-Augmented Generation) để truy xuất thông tin từ nguồn kiến thức riêng."),
    ("Tập hợp các tải hiệu cân thiết như bài giáng, sách giảo khoa tài liu duyen môn phuc vu cho tro li màn học",
     "Tập hợp các tài liệu cần thiết như bài giảng, sách giáo khoa, tài liệu chuyên môn phục vụ cho trợ lí môn học."),
    ("Thu thếp tài hiệu", "Thu thập tài liệu"),
    ("Tiền xử lí da liệu", "Tiền xử lí dữ liệu"),
    ("Cát nhd var bin (chunking), tạo embedding để chuẩn bị bị cho qua trình truy xuất thông tin hiệu quả.",
     "Cắt nhỏ văn bản (chunking), tạo embedding để chuẩn bị cho quá trình truy xuất thông tin hiệu quả."),
    ("kas Chunking Vector Store", "Chunking, Vector Store"),
    ("Bước cốt lỏi để hiện thực hóa thiết ké giái pháp két nối cóc thánh phân Ai thành một hệ thống hoàn chinh",
     "Bước cốt lõi để hiện thực hóa thiết kế giải pháp, kết nối các thành phần AI thành một hệ thống hoàn chỉnh."),
    (". Kết nết với mô hình ngôn ngữ lớn", "Kết nối với mô hình ngôn ngữ lớn"),
    ("Phương pháp Cấu hình/Lập trinh", "Phương pháp Cấu hình/Lập trình"),
    ("Sử dụng APl của các mô hình ngôn ngữ lớn hoàc triển khai mô hình cục bú", "Sử dụng API của các mô hình ngôn ngữ lớn hoặc triển khai mô hình cục bộ"),
    ("Chọn lập trình bằng viết mà hoặc công cu no code", "Chọn lập trình bằng viết mã hoặc công cụ no-code"),
    ("Tích hợp một hoặc nhiêu thư viện giúp điu phối các thành phần trong AI", "Tích hợp một hoặc nhiều thư viện giúp điều phối các thành phần trong AI"),
    ("Open/l GPT) Google Gemin", "OpenAI GPT, Google Gemini,..."),
    ("Tích hợp các thánh phần riêng lê thánh một luồng hoạt động hoàn chỉnh và thực hiện kiểm thử sớm.",
     "Tích hợp các thành phần riêng lẻ thành một luồng hoạt động hoàn chỉnh và thực hiện kiểm thử sớm."),
    ("Kết nói luòng hoạt động", "Kết nối luồng hoạt động"),
    ("Kiếm thứ từng phần", "Kiểm thử từng phần"),
    ("Tạo luồng hoàn chỉnh từ đầu vào của người dùng, qua xí lí AI, dến đầu ra cuối cùng.",
     "Tạo luồng hoàn chỉnh từ đầu vào của người dùng, qua xử lí AI, đến đầu ra cuối cùng."),
    ("Chay thừ và kiểm tra chưc nàng ngay sau khi hoàn thành mỗi phần nhỏ để phát hiện lôi răm",
     "Chạy thử và kiểm tra chức năng ngay sau khi hoàn thành mỗi phần nhỏ để phát hiện lỗi sớm."),
    ("ay tran vao Nêu câu hói liên quan đến một bài văn, hây cung cầp thông",
     "Nếu câu hỏi liên quan đến một bài văn, hãy cung cấp thông"),
    ("hây cung cầp", "hãy cung cấp"),
    ("Bạn có cầu hôi gi vệ mên Ngữ văn kho 122.", "Bạn có câu hỏi gì về môn Ngữ văn lớp 12?"),
    ("Bạn có cầu hôi gi vệ mên Ngữ văn kho 122", "Bạn có câu hỏi gì về môn Ngữ văn lớp 12"),
    ("Bạn có câu hỏi gi về môn Ngữ văn lớp 12?", "Bạn có câu hỏi gì về môn Ngữ văn lớp 12?"),
    ("tiêu biếu của văn học", "tiêu biểu của văn học"),
    ("kháng chiên", "kháng chiến"),
    ("về đắt nước,", "về đất nước,"),
    ("triển khai mô hình cục bú", "triển khai mô hình cục bộ"),
    ("cục bú", "cục bộ"),
    ("sử Aì co mể xuy tưân và sử dụng", "để AI có thể suy luận và sử dụng"),
    ("tác phẩm tiêu biếu nhất", "tác phẩm tiêu biểu nhất"),
    ("hay bât kì công cụ", "hay bất kì công cụ"),
    ("một bai trinh bà", "một bài trình bày"),
    ("Kĩ nắng trinh báy", "Kĩ năng trình bày"),
    ("cúc tác giả", "các tác giả"),

    # Universal subtle tone words across all texts
    ("tạo ra kết</p>\n<p class=\"lesson-p\">quà chính xác", "tạo ra kết quả chính xác"),
    ("tạo ra kết</p> <p class=\"lesson-p\">quà chính xác", "tạo ra kết quả chính xác"),
    ("tạo ra kết\nquà chính xác", "tạo ra kết quả chính xác"),
    ("quà chính xác", "quả chính xác"),
    ("tạo sinhh", "tạo sinh"),
    ("Hiều dúng", "Hiểu đúng"),
    ("hiều dúng", "hiểu đúng"),
    ("hiều lầm", "hiểu lầm"),
    ("Hiều lầm", "Hiểu lầm"),
    ("Agent trà Lời", "Agent trả lời"),
    ("trà Lời", "trả lời"),
    ("đùng ý", "đúng ý"),
    ("kết quà", "kết quả"),
    ("Kết quà", "Kết quả"),
    ("kết   quà", "kết quả"),
    ("hiệu quà", "hiệu quả"),
    ("Hiệu quà", "Hiệu quả"),
    ("thiếu tinh xác định", "thiếu tính xác định"),
    ("thiếu tinh", "thiếu tính"),
    ("tinh huống", "tình huống"),
    ("Tinh huống", "Tình huống"),
    ("tinh huồng", "tình huống"),
    ("tinh huóng", "tình huống"),
    ("tinh trạng", "tình trạng"),
    ("đồng tinh", "đồng tình"),
    ("tinh lãi", "tính lãi"),
    ("Tinh giá trị", "Tính giá trị"),
    ("tính giá trị", "tính giá trị"),
    ("chinh xác", "chính xác"),
    ("Chinh xác", "Chính xác"),
    ("ngữ cánh", "ngữ cảnh"),
    ("ngử cảnh", "ngữ cảnh"),
    ("từ khoá", "từ khóa"),
    ("Từ khoá", "Từ khóa"),
    ("cuối khoá", "cuối khóa"),
    ("phài", "phải"),
    ("chia sẽ", "chia sẻ"),
    ("Chia sẽ", "Chia sẻ"),
    ("xày ra", "xảy ra"),
    ("phản hỏi", "phản hồi"),
    ("Pravlew", "Preview"),
    ("vl dụ", "ví dụ"),
    ("Vl dụ", "Ví dụ"),
    ("v1 dụ", "ví dụ"),
    ("V1 dụ", "Ví dụ"),
]

def clean_str(text):
    if not isinstance(text, str):
        return text
    for old, new in exact_replacements:
        text = text.replace(old, new)
    
    # Specific regex fixes
    text = re.sub(r"\bkết\s+quà\b", "kết quả", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhiệu\s+quà\b", "hiệu quả", text, flags=re.IGNORECASE)
    text = re.sub(r"\bchinh\s+xác\b", "chính xác", text, flags=re.IGNORECASE)
    text = re.sub(r"\btừ\s+khoá\b", "từ khóa", text, flags=re.IGNORECASE)
    text = re.sub(r"\bkhông\s+vl\s+dụ\b", "không ví dụ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bvl\s+dụ\b", "ví dụ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bv1\s+dụ\b", "ví dụ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhiều\s+lầm\b", "hiểu lầm", text, flags=re.IGNORECASE)
    text = re.sub(r"\bHiều\s+dúng\b", "Hiểu đúng", text, flags=re.IGNORECASE)
    text = re.sub(r"\bhiều\s+dúng\b", "hiểu đúng", text, flags=re.IGNORECASE)
    text = re.sub(r"\btrà\s+lời\b", "trả lời", text, flags=re.IGNORECASE)
    text = re.sub(r"\bđùng\s+ý\b", "đúng ý", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(làm|là|có|điều|mục đích|hậu quả|kĩ năng|khó khăn|lỗi)\s+gi\b", r"\1 gì", text, flags=re.IGNORECASE)
    return text

def walk_and_clean(obj):
    if isinstance(obj, dict):
        return {k: walk_and_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_clean(item) for item in obj]
    elif isinstance(obj, str):
        return clean_str(obj)
    return obj

# 1. Clean data/books.json
books_p = ROOT / "data" / "books.json"
print("Cleaning data/books.json...")
books_data = json.loads(books_p.read_text(encoding="utf-8"))
cleaned_books = walk_and_clean(books_data)
books_p.write_text(json.dumps(cleaned_books, ensure_ascii=False, indent=2), encoding="utf-8")

# 2. Clean data/lessons-lop-{10,11,12}.json
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    print(f"Cleaning {lp}...")
    data = json.loads(lp.read_text(encoding="utf-8"))
    cleaned_data = walk_and_clean(data)
    lp.write_text(json.dumps(cleaned_data, ensure_ascii=False, indent=2), encoding="utf-8")

# 3. Clean all lessons/lop-*/*.html
html_files = glob.glob(str(ROOT / "lessons" / "*" / "*.html"))
print(f"Cleaning {len(html_files)} HTML files...")
for hf in html_files:
    p = Path(hf)
    content = p.read_text(encoding="utf-8")
    cleaned = clean_str(content)
    p.write_text(cleaned, encoding="utf-8")

# 4. Clean index.html and reader.html
for rf in ["index.html", "reader.html"]:
    rp = ROOT / rf
    if rp.exists():
        content = rp.read_text(encoding="utf-8")
        cleaned = clean_str(content)
        rp.write_text(cleaned, encoding="utf-8")

# 5. Rebuild search indexes
print("Rebuilding search indexes...")
for b in ["lop-10", "lop-11", "lop-12"]:
    lp = ROOT / "data" / f"lessons-{b}.json"
    sp = ROOT / "data" / f"search-{b}.json"
    
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

print("Master clean and rebuild complete!")
