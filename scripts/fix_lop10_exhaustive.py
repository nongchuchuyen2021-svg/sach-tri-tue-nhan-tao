import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LESSONS_DIR = ROOT / "lessons" / "lop-10"


def make_code_block(code: str) -> str:
    return (
        '\n                    <div class="code-block-wrapper">\n'
        '                        <div class="code-header"><span>Python / Code</span>'
        '<button class="btn-copy-code" onclick="copyCode(this)">Sao chép</button></div>\n'
        f'                        <pre><code class="language-python">{code}</code></pre>\n'
        '                    </div>\n                    '
    )


def section_open(cls: str, sec_id: str, icon: str, title: str) -> str:
    return (
        f'\n            <section class="lesson-card {cls}" id="{sec_id}">\n'
        '                <div class="section-badge-header">\n'
        f'                    <span class="sec-icon">{icon}</span>\n'
        f'                    <h2 class="section-title">{title}</h2>\n'
        '                </div>\n'
        '                <div class="section-body">\n            '
    )


BAI11_CODE_BLOCK1 = make_code_block("!pip install gTTS")

BAI11_CODE_BLOCK2 = make_code_block(
"""from gtts import gTTS
from IPython.display import Audio

tts = gTTS("Việt Nam đất nước ta ơi. Mênh mông biển lúa đâu trời đẹp hơn", lang='vi')
tts.save("vietnam.mp3")
Audio("vietnam.mp3", autoplay=True)"""
)


GLOSSARY_CLEAN_BODY = """
<p class="lesson-p"><strong>BẢNG GIẢI THÍCH THUẬT NGỮ</strong></p>
<p class="lesson-p"><strong>AI tạo sinh (Generative AI) (Trang 11):</strong> Loại trí tuệ nhân tạo có khả năng tạo ra nội dung mới dạng văn bản, hình ảnh, âm thanh, video, mã chương trình,...</p>
<p class="lesson-p"><strong>Bịa đặt (Hallucination) (Trang 47):</strong> Hiện tượng AI tạo sinh tạo ra thông tin sai lệch nhưng có thể thấy đúng hoặc hợp lí, dù không có dữ liệu hỗ trợ.</p>
<p class="lesson-p"><strong>Giả mạo (Deepfake) (Trang 47):</strong> Sử dụng AI để tạo ra hình ảnh, video hoặc âm thanh, khiến người xem tưởng rằng ai đó đã nói hoặc làm điều gì đó mà họ thực tế chưa từng làm.</p>
<p class="lesson-p"><strong>Mạng nơ-ron nhân tạo (Trang 8):</strong> Hệ thống phần mềm mô phỏng cách hoạt động của não người, gồm nhiều "nút" (gọi là nơ-ron nhân tạo) kết nối với nhau.</p>
<p class="lesson-p"><strong>Mạng nơ-ron tích chập (CNN) (Trang 9):</strong> Một loại mạng nơ-ron nhân tạo, được thiết kế chủ yếu để xử lí hình ảnh. Nó có thể tự động tìm ra các đặc điểm thông tin như hình dạng, màu sắc trong ảnh, hoặc âm thanh trong dữ liệu giọng nói, bằng cách xử lí dữ liệu có cấu trúc dạng lưới hoặc chuỗi.</p>
<p class="lesson-p"><strong>Thiên vị (Bias) (Trang 51):</strong> AI đưa ra kết quả không công bằng, nghiêng về một phía, do dữ liệu mà nó học bị thiếu cân bằng hoặc sai lệch.</p>
<p class="lesson-p"><strong>Trí tuệ nhân tạo (AI – Artificial Intelligence) (Trang 6):</strong> Ngành khoa học và công nghệ giúp máy móc có thể suy nghĩ, học tập và giải quyết vấn đề giống con người.</p>
<p class="lesson-p"><strong>Xử lí ngôn ngữ tự nhiên (NLP) (Trang 8):</strong> Lĩnh vực của trí tuệ nhân tạo giúp máy tính hiểu, phân tích và tạo ra ngôn ngữ của con người, như tiếng Việt hay tiếng Anh. Nhờ NLP, máy có thể dịch văn bản, trả lời câu hỏi, kiểm tra chính tả hay trò chuyện với người dùng như ChatGPT.</p>
""".strip()


MUC_LUC_CLEAN_BODY = """
<p class="lesson-p"><strong>MỤC LỤC</strong> (Nội dung – Trang)</p>
<p class="lesson-p"><strong>CHỦ ĐỀ 1. GIỚI THIỆU VỀ AI VÀ AI TẠO SINH</strong> (Trang 5)</p>
<ul class="lesson-bullet-list">
<li>Bài 1. Trí tuệ nhân tạo — Trang 6</li>
<li>Bài 2. AI tạo sinh — Trang 11</li>
<li>Bài 3. Mô hình ngôn ngữ lớn — Trang 19</li>
<li>Bài 4. Dữ liệu huấn luyện — Trang 26</li>
</ul>
<p class="lesson-p"><strong>CHỦ ĐỀ 2. KHÁM PHÁ CÔNG CỤ VÀ ỨNG DỤNG AI</strong> (Trang 31)</p>
<ul class="lesson-bullet-list">
<li>Bài 5. Prompt – Giao tiếp với AI tạo sinh — Trang 32</li>
<li>Bài 6. AI tạo sinh hỗ trợ học tập — Trang 39</li>
</ul>
<p class="lesson-p"><strong>CHỦ ĐỀ 3. ĐẠO ĐỨC VÀ TRÁCH NHIỆM KHI SỬ DỤNG AI</strong> (Trang 46)</p>
<ul class="lesson-bullet-list">
<li>Bài 7. Phân biệt thật – giả trong AI tạo sinh — Trang 47</li>
<li>Bài 8. Hiểu đúng về AI tạo sinh: thiên vị, hiểu lầm và tác hại với con người — Trang 51</li>
<li>Bài 9. Công dân số trong kỉ nguyên AI — Trang 56</li>
</ul>
<p class="lesson-p"><strong>CHỦ ĐỀ 4. PHÁT TRIỂN SẢN PHẨM VÀ ỨNG DỤNG AI</strong> (Trang 65)</p>
<ul class="lesson-bullet-list">
<li>Bài 10. AI và nghề nghiệp — Trang 66</li>
<li>Bài 11. Môi trường phát triển sản phẩm AI — Trang 70</li>
<li>Bài 12. Bài tập dự án — Trang 77</li>
</ul>
<p class="lesson-p"><strong>BẢNG GIẢI THÍCH THUẬT NGỮ</strong> — Trang 87</p>
""".strip()


REPLACEMENTS = {
    "bia-sach": [
        (
            "HÀ ĐẶNG CAO TUNG - HOÀNG THỊ MẠI - LE ANH VINH ĐỒNG CHÚ ĐIÊN",
            "HÀ ĐẶNG CAO TÙNG - HOÀNG THỊ MAI - LÊ ANH VINH (ĐỒNG CHỦ BIÊN)",
        ),
        ("NGUYÊN QUANG ĐỨC", "NGUYỄN QUANG ĐỨC"),
        (
            "NGUYÊN THỊ VAN ANH -PHẠM TUẦN ANH - VŨ VĂN LUÂN",
            "NGUYỄN THỊ VÂN ANH - PHẠM TUẤN ANH - VŨ VĂN LUÂN",
        ),
    ],
    "cong-van-tham-dinh-bia-lot": [
        (
            '<p class="lesson-p">Bộ tài liệu đã được Viện Khoa học Giáo dục Việt Nam tố chức đánh giá</p>\n'
            '<p class="lesson-p">theo chi đạo tại Công văn số 1362/BGDĐT-GDPT ngày 31/12/2025</p>\n'
            '<p class="lesson-p">của Bộ Giáo dục và Đào tạo và kết luận đủ điều kiện</p>\n'
            '<p class="lesson-p">"đưa vào triển khai thí điểm trong các cơ sở giáo dục phố thông".</p>',
            '<p class="lesson-p">Bộ tài liệu đã được Viện Khoa học Giáo dục Việt Nam tổ chức đánh giá theo chỉ đạo tại Công văn số 1362/BGDĐT-GDPT ngày 31/12/2025 của Bộ Giáo dục và Đào tạo và kết luận đủ điều kiện "đưa vào triển khai thí điểm trong các cơ sở giáo dục phổ thông".</p>',
        ),
        ("HÀ ĐANG CAO TUNG", "HÀ ĐẶNG CAO TÙNG"),
        (
            "VU TRUNG CHÍNH - NGUYỄN QUANG ĐỨC - NGUYÊN CHÍ THANH",
            "VŨ TRUNG CHÍNH - NGUYỄN QUANG ĐỨC - NGUYỄN CHÍ THANH",
        ),
        (
            "NGUYEN THỊ VAN ANH - PHẠM TUAN ANH",
            "NGUYỄN THỊ VÂN ANH - PHẠM TUẤN ANH",
        ),
        ('\n<p class="lesson-p"></p>', ""),
    ],
    "huong-dan-su-dung-sach": [
        ('<p class="lesson-p">HƯỚNG DẪN SỬ DỤNG SÁCH</p>\n', ""),
        (
            "<p class=\"lesson-p\">MỤC TIÊU Giúp em biết mình sẽ đạt được gì sau bài học.</p>\n"
            "<p class=\"lesson-p\">KHỞI ĐỘNG Giúp em nhận biết ý nghĩa của bài học bằng cách kết nối những tình huống xuất hiện trong cuộc sống với nội dung bài học.</p>",
            section_open("target-section", "sec-mục-tiêu", "🎯", "MỤC TIÊU").strip()
            + '\n<p class="lesson-p">Giúp em biết mình sẽ đạt được gì sau bài học.</p>\n</div></section>\n'
            + section_open("warmup-section", "sec-khởi-động", "💡", "KHỞI ĐỘNG").strip()
            + '\n<p class="lesson-p">Giúp em nhận biết ý nghĩa của bài học bằng cách kết nối những tình huống xuất hiện trong cuộc sống với nội dung bài học.</p>\n</div></section>',
        ),
        (
            "<p class=\"lesson-p\">HỘP KIẾN THỨC</p>\n<p class=\"lesson-p\">Tóm tắt kiến thức mới một cách cô đọng, giúp em dễ ghi nhớ.</p>\n<p class=\"lesson-p\">THỰC HÀNH Gồm những nhiệm vụ học tập có hướng dẫn chi tiết.</p>",
            "<p class=\"lesson-p\"><strong>HỘP KIẾN THỨC:</strong> Tóm tắt kiến thức mới một cách cô đọng, giúp em dễ ghi nhớ.</p>\n<p class=\"lesson-p\"><strong>THỰC HÀNH:</strong> Gồm những nhiệm vụ học tập có hướng dẫn chi tiết.</p>",
        ),
        ("để củng có kiến thức, kĩ năng trong bài học.", "để củng cố kiến thức, kĩ năng trong bài học."),
        (
            "<p class=\"lesson-p\">Gồm những câu hỏi, bài tập, thực hành nâng cao hoặc mở rộng kiến thức, kĩ năng đã học để giải quyết tình huống thực tiễn.</p>\n"
            "<p class=\"lesson-p\">Tài liệu giảng dạy.</p>\n"
            "<p class=\"lesson-p\">Học liệu số mở rộng.</p>\n"
            "</div></section>",
            "<p class=\"lesson-p\">Gồm những câu hỏi, bài tập, thực hành nâng cao hoặc mở rộng kiến thức, kĩ năng đã học để giải quyết tình huống thực tiễn.</p>\n"
            "</div></section>\n"
            "<p class=\"lesson-p\"><strong>Học liệu điện tử đi kèm:</strong> Tài liệu giảng dạy. Học liệu số mở rộng.</p>",
        ),
    ],
    "loi-noi-dau": [
        ('<p class="lesson-p">LỜI NÓI ĐẦU</p>\n', ""),
        (
            """<p class="lesson-p">Các em học sinh thân mền!</p>
<p class="lesson-p">Từ điện thoại thông minh, trợ lí ào đến những bài hát, bức tranh do máy.</p>
<p class="lesson-p">tạo ra - AI đang thay đổi cách con người học tập, làm việc và sáng tạo.</p>
<p class="lesson-p">Nhờ khả năng xử lí vượt trội và tiếp cận kho dữ liệu khổng lồ, AI đang tiến</p>
<p class="lesson-p">tới giới hạn có thể suy nghĩ, học hỏi và hành động gần như con người.</p>
<p class="lesson-p">Vì vậy, học để hiểu và làm chủ AI không còn là một lựa chọn; mà là một điều</p>
<p class="lesson-p">tất yếu để chúng ta có thể tồn tại và phát triển trong thế giới do chinh mình</p>
<p class="lesson-p">Cuốn sách Trí tuệ nhân tạo lớp 10 đưa các em bước vào thế giới đầy</p>
<p class="lesson-p">hấp dẫn của AI, đặc biệt là AI tạo sinh, hỗ trợ em trong học tập, sáng tạo.</p>
<p class="lesson-p">Trong thế giới ấy, AI có thể viết văn, giải toán, vẽ tranh, nhưng cũng có lúc</p>
<p class="lesson-p">thiên vị, hiểu lầm hoặc tạo ra thông tin không đúng. Các em sẽ được hướng</p>
<p class="lesson-p">dẫn cách nhận biết đúng - sai, thật - giả và học cách sử dụng AI một cách</p>
<p class="lesson-p">an toàn, hiệu quả và có trách nhiệm.</p>
<p class="lesson-p">Bộ sách được thiết kế hiện đại, sinh động, gần gũi với cuộc sống hàng</p>
<p class="lesson-p">ngày của các em. Những ví dụ, hoạt động và sản phẩm trong sách không</p>
<p class="lesson-p">chỉ dễ hiểu mà còn khơi gợi sự tò mò, khám phá và sáng tạo, làm cho việc</p>
<p class="lesson-p">học Ai trở thành một hành trình thú vị, truyền cảm hứng, giúp các em phát</p>
<p class="lesson-p">triền tư duy, năng lực giải quyết vấn đề, cũng như thái độ trách nhiệm trong</p>
<p class="lesson-p">thế giới số.</p>
<p class="lesson-p">Chúc các em học tập vui vẻ, khám phá hứng thủ và thành công trên con đường</p>
<p class="lesson-p">làm quen với Trí tuệ nhân tạo!</p>""",
            """<p class="lesson-p">Các em học sinh thân mến!</p>
<p class="lesson-p">Từ điện thoại thông minh, trợ lí ảo đến những bài hát, bức tranh do máy tạo ra – AI đang thay đổi cách con người học tập, làm việc và sáng tạo. Nhờ khả năng xử lí vượt trội và tiếp cận kho dữ liệu khổng lồ, AI đang tiến tới giới hạn có thể suy nghĩ, học hỏi và hành động gần như con người. Vì vậy, học để hiểu và làm chủ AI không còn là một lựa chọn, mà là một điều tất yếu để chúng ta có thể tồn tại và phát triển trong thế giới do chính mình tạo ra.</p>
<p class="lesson-p">Cuốn sách Trí tuệ nhân tạo lớp 10 đưa các em bước vào thế giới đầy hấp dẫn của AI, đặc biệt là AI tạo sinh, hỗ trợ em trong học tập, sáng tạo. Trong thế giới ấy, AI có thể viết văn, giải toán, vẽ tranh, nhưng cũng có lúc thiên vị, hiểu lầm hoặc tạo ra thông tin không đúng. Các em sẽ được hướng dẫn cách nhận biết đúng – sai, thật – giả và học cách sử dụng AI một cách an toàn, hiệu quả và có trách nhiệm.</p>
<p class="lesson-p">Bộ sách được thiết kế hiện đại, sinh động, gần gũi với cuộc sống hằng ngày của các em. Những ví dụ, hoạt động và sản phẩm trong sách không chỉ dễ hiểu mà còn khơi gợi sự tò mò, khám phá và sáng tạo, làm cho việc học AI trở thành một hành trình thú vị, truyền cảm hứng, giúp các em phát triển tư duy, năng lực giải quyết vấn đề, cũng như thái độ trách nhiệm trong thế giới số.</p>
<p class="lesson-p">Chúc các em học tập vui vẻ, khám phá hứng thú và thành công trên con đường làm quen với Trí tuệ nhân tạo!</p>""",
        ),
    ],
    "muc-luc": [
        (
            """<p class="lesson-p">MỤC LỤC</p>
<p class="lesson-p">NỘI DUNG</p>
<p class="lesson-p">CHỦ ĐỂ 1. GIỚI THIỆU VỀ AI VÀ AI TẠO SINH</p>
<p class="lesson-p">Bài 1</p>
<p class="lesson-p">Trí tuệ nhân tạo</p>
<p class="lesson-p">Bỏi 2</p>
<p class="lesson-p">AI tạo sinh</p>
<p class="lesson-p">Bài 3 Mô hình ngôn ngữ lớn</p>
<p class="lesson-p">Bài 4 Dữ liệu huấn luyện</p>
<p class="lesson-p">CHỦ ĐẾ 2. KHÁM PHA CÔNG CỤ VÀ ỨNG DỤNG AI</p>
<p class="lesson-p">Bài 5 Prompt - Giao tiếp với AI tạo sinh</p>
<p class="lesson-p">Bài 6 ÀI tạo sinh hỗ trợ học tập</p>
<p class="lesson-p">CHỦ ĐỀ 3. ĐẠO ĐỨC VÀ TRÁCH NHIỆM KHI SỬ DUNG AI</p>
<p class="lesson-p">Bài 7 Phân biệt thật - giả trong AI tạo sinh</p>
<p class="lesson-p">Bài 8 Hiểu đúng về AI tạo sinh: thiên vị, hiểu lầm và tác hại với con người</p>
<p class="lesson-p">Bài 9 Công dân số trong kỉ nguyên AI</p>
<p class="lesson-p">CHỦ ĐỀ 4. PHÁT TRIỂN SẢN PHẨM VÀ ỨNG DỤNG AI</p>
<p class="lesson-p">Bai 10 AI và nghề nghiệp</p>
<p class="lesson-p">Bài 11 Mỗi trường phát triển sản phẩm AI</p>
<p class="lesson-p">Bài 12 Bài tập dự án</p>
<p class="lesson-p">BẢNG GIẢI THÍCH THUẬT NGỮ</p>
<p class="lesson-p">Trang CHỦ ĐỀ 1. GIỚI THIỆU VỀ AI</p>
<p class="lesson-p">VÀ AI TẠO SINH</p>
<p class="lesson-p">OC</p>""",
            MUC_LUC_CLEAN_BODY,
        ),
    ],
    "bai-1-tri-tue-nhan-tao": [
        ("(FaceID & vân tay)", "(FaceID &amp; vân tay)"),
        (
            "<strong>AI hẹp</strong> - chuyên thực hiện các tác vụ chuyên biệt và <strong>AI tổng quát</strong> - hướng tới",
            "<strong>AI hẹp</strong> – chuyên thực hiện các tác vụ chuyên biệt và <strong>AI tổng quát</strong> – hướng tới",
        ),
    ],
    "bai-2-ai-tao-sinh": [
        (
            "<li>Tạo ra được sản phẩm mới dạng hình ảnh, văn bản hoặc âm thanh sử dụng công cụ AI tạo sinh.\n\nH</li>",
            "<li>Tạo ra được sản phẩm mới dạng hình ảnh, văn bản hoặc âm thanh sử dụng công cụ AI tạo sinh.</li>",
        ),
        (
            "<p class=\"lesson-p\">1. AI có thể hỗ trợ hai bạn Lan và Nam tạo ra sản phẩm theo mong muốn của mình không?\n\n2. Trong mỗi tình huống trên, AI tạo ra nội dung mới hay tìm kiếm và đưa ra nội dung có sẵn?</p>",
            "<p class=\"lesson-p\">1. AI có thể hỗ trợ hai bạn Lan và Nam tạo ra sản phẩm theo mong muốn của mình không?</p>\n<p class=\"lesson-p\">2. Trong mỗi tình huống trên, AI tạo ra nội dung mới hay tìm kiếm và đưa ra nội dung có sẵn?</p>",
        ),
        (
            '<p class="lesson-p">Trong tình huống ở phần Khởi động, Lan đã tạo tấm thiệp sinh nhật có hình ảnh dễ thương, còn Nam tạo một đoạn nhạc vui nhộn. Cả hai bạn đều chỉ cần nhập mô tả</p>\n'
            '<p class="lesson-p">cho công cụ AI, hệ thống đã tự động tạo ra sản phẩm đúng với ý tưởng. Điều đó</p>\n'
            '<p class="lesson-p">cho thấy công cụ AI có thể hiểu yêu cầu bằng mô tả (văn bản hay lời nói) và tạo ra nội dung mới dựa trên dữ liệu đã học.</p>',
            '<p class="lesson-p">Trong tình huống ở phần Khởi động, Lan đã tạo tấm thiệp sinh nhật có hình ảnh dễ thương, còn Nam tạo một đoạn nhạc vui nhộn. Cả hai bạn đều chỉ cần nhập mô tả cho công cụ AI, hệ thống đã tự động tạo ra sản phẩm đúng với ý tưởng. Điều đó cho thấy công cụ AI có thể hiểu yêu cầu bằng mô tả (văn bản hay lời nói) và tạo ra nội dung mới dựa trên dữ liệu đã học.</p>',
        ),
        (
            '<p class="lesson-p">Gemini</p>\n<p class="lesson-p">Suno AI</p>\n<p class="lesson-p">Suno AI</p>\n<p class="lesson-p">ChatGPT</p>\n',
            "",
        ),
        ("tạo ra kết quả tương ứng</p>", "tạo ra kết quả tương ứng.</p>"),
        (
            """<ul class="lesson-bullet-list">
<li>Một số công cụ AI tạo sinh có thể tạo hình ảnh/tranh như ChatGPT, Craiyon,...</li>
</ul>
<p class="lesson-p">cho phép người dùng nhập mô tả bằng lời và hệ thống tạo ra hình ảnh</p>
<ul class="lesson-bullet-list">
<li>Một số công cụ AI tạo sinh có thể tạo văn bản theo yêu cầu như ChatGPT,</li>
</ul>
<p class="lesson-p">Gemini, Microsoft Copilot,..

- Một số ứng dụng tạo nhạc như Suno AI, MusicGen, Voicemod Text-to-Song,...</p>
<p class="lesson-p">cho phép tạo ra âm thanh, bài nhạc theo mô tả bằng lời.</p>""",
            """<ul class="lesson-bullet-list">
<li>Một số công cụ AI tạo sinh có thể tạo hình ảnh/tranh như ChatGPT, Craiyon,... cho phép người dùng nhập mô tả bằng lời và hệ thống tạo ra hình ảnh.</li>
<li>Một số công cụ AI tạo sinh có thể tạo văn bản theo yêu cầu như ChatGPT, Gemini, Microsoft Copilot,...</li>
<li>Một số ứng dụng tạo nhạc như Suno AI, MusicGen, Voicemod Text-to-Song,... cho phép tạo ra âm thanh, bài nhạc theo mô tả bằng lời.</li>
</ul>""",
        ),
        ("Những hộ thống này thường được thiết kế", "Những hệ thống này thường được thiết kế"),
        (
            '<p class="lesson-p">Trong phần Khởi động, công cụ AI má Lan và Nam sử dụng có thể tạo ra hình ảnh hoặc âm thanh mới từ yêu cầu mô tả bằng lời. Kết quả tạo ra có thể khác nhau</p>\n'
            '<p class="lesson-p">giữa các lần, dù yêu cầu khá giống nhau. Điều này cho thấy công cụ không chỉ làm theo mẫu có sẵn mà còn có thể tạo ra nội dung mới theo yêu cầu.</p>',
            '<p class="lesson-p">Trong phần Khởi động, công cụ AI mà Lan và Nam sử dụng có thể tạo ra hình ảnh hoặc âm thanh mới từ yêu cầu mô tả bằng lời. Kết quả tạo ra có thể khác nhau giữa các lần, dù yêu cầu khá giống nhau. Điều này cho thấy công cụ không chỉ làm theo mẫu có sẵn mà còn có thể tạo ra nội dung mới theo yêu cầu.</p>',
        ),
        (
            '<p class="lesson-p">AI tạo sinh có khả năng tạo ra các nội dung mới dưới dạng văn bản, hình ảnh, âm thanh.... dựa trên mô tả của con người. Thay vì chọn một kết quả có sẵn, hệ thống</p>\n'
            '<p class="lesson-p">sẽ sử dụng các dữ liệu đã học để tạo ra nội dung đáp ứng các yêu cầu khác nhau, mang tính đa dạng và linh hoạt.</p>',
            '<p class="lesson-p">AI tạo sinh có khả năng tạo ra các nội dung mới dưới dạng văn bản, hình ảnh, âm thanh,... dựa trên mô tả của con người. Thay vì chọn một kết quả có sẵn, hệ thống sẽ sử dụng các dữ liệu đã học để tạo ra nội dung đáp ứng các yêu cầu khác nhau, mang tính đa dạng và linh hoạt.</p>',
        ),
        (
            "<li>AI thế hệ trước thường thực hiện nhiệm vụ theo quy trình cố định. Kết quả trả về giống nhau nếu đầu vào không đổi.\n\n• AI tạo sinh có thể cho nhiều kết quả khác nhau với cùng một yêu cầu, vì hệ thống tạo ra nội dung mới dựa trên dữ liệu người dùng nhập vào.</li>",
            "<li>AI thế hệ trước thường thực hiện nhiệm vụ theo quy trình cố định. Kết quả trả về giống nhau nếu đầu vào không đổi.</li>\n<li>AI tạo sinh có thể cho nhiều kết quả khác nhau với cùng một yêu cầu, vì hệ thống tạo ra nội dung mới dựa trên dữ liệu người dùng nhập vào.</li>",
        ),
        (
            '<p class="lesson-p">3. Thực hành: Tạo sản phẩm mới dạng hình ảnh, văn bản hoặc âm thanh bằng công cụ AI tạo sinh</p>',
            '<h3 class="subheading-h3"><span class="h3-num">3.</span> Thực hành: Tạo sản phẩm mới dạng hình ảnh, văn bản hoặc âm thanh bằng công cụ AI tạo sinh</h3>',
        ),
        (
            "<li>Để sử dụng công cụ, em có thể đăng nhập (Login) nếu đã có tài khoản</li>",
            "<li>Để sử dụng công cụ, em có thể đăng nhập (Login) nếu đã có tài khoản (Hình 2.4) hoặc đăng kí tài khoản miễn phí (Sign up for free) nếu chưa có tài khoản (Hình 2.3).</li>",
        ),
        ('<p class="lesson-p">Welcome back Create an account</p>\n', ""),
        (
            '<figcaption class="figure-caption"><strong>Hình 2.3 & 2.4.</strong> Đăng ký tài khoản mới và đăng nhập ChatGPT</figcaption>\n</figure>',
            '<figcaption class="figure-caption"><strong>Hình 2.3 &amp; 2.4.</strong> Đăng ký tài khoản mới và đăng nhập ChatGPT</figcaption>\n</figure>\n'
            '<p class="lesson-p">Bước 2. Nhập mô tả hình ảnh cần tạo vào ô trò chuyện.</p>\n'
            '<p class="lesson-p">Em nhập vào ô trò chuyện một yêu cầu. Ví dụ:</p>\n'
            '<ul class="lesson-bullet-list">\n'
            '<li>"Vẽ giúp em một con mèo đang đội mũ sinh nhật ngồi trước chiếc bánh kem";</li>\n'
            '<li>"Tạo một hình ảnh minh hoạ cho tấm thiệp sinh nhật có hoa và bóng bay".</li>\n'
            '</ul>',
        ),
        (
            '<p class="lesson-p">Bước 4. Ghi nhận và lưu kết quả</p>\n<p class="lesson-p">Em có thể tải về hình ảnh hoặc chụp ảnh màn hình kết quả để chia sẻ</p>',
            '<p class="lesson-p">Bước 4. Ghi nhận và lưu kết quả.</p>\n<p class="lesson-p">Em có thể tải về hình ảnh hoặc chụp ảnh màn hình kết quả để chia sẻ.</p>',
        ),
        (
            '<p class="lesson-p">"Một bài hát sinh nhật vui vẻ dành cho ban thân".</p>',
            '<p class="lesson-p">"Một bài hát sinh nhật vui vẻ dành cho bạn thân";</p>',
        ),
        (
            '<p class="lesson-p">"A happy pop song for Mother\'s Day".\n\n- Sau đó chọn Create.</p>',
            '<p class="lesson-p">"A happy pop song for Mother\'s Day".</p>\n<ul class="lesson-bullet-list">\n<li>Sau đó chọn Create.</li>\n</ul>',
        ),
        (
            """<p class="lesson-p">ChatGPT v 1 Share</p>
<p class="lesson-p">Viết một đoạn văn ngắn để chúc mừng Ngày của Mẹ</p>
<p class="lesson-p">Nhân Ngày của Mẹ, con xin gửi đến mẹ những lời chúc tốt đẹp và chân thành nhất. Cảm</p>
<p class="lesson-p">ơn mẹ vì đã luôn yêu thương, hy sinh và là chỗ dựa vững chắc cho con suốt bao năm</p>
<p class="lesson-p">mai. Con yêu mẹ nhiều lắm!</p>
<p class="lesson-p">qua. Mong mẹ luôn mạnh khỏe, hạnh phúc và mãi nở nụ cười rạng rỡ như ánh nắng ban</p>""",
            "",
        ),
        (
            '<figcaption class="figure-caption"><strong>Hình 2.9.</strong> Giao diện kết quả của ChatGPT</figcaption>',
            '<figcaption class="figure-caption"><strong>Hình 2.9.</strong> Giao diện kết quả của ChatGPT khi tạo đoạn văn</figcaption>',
        ),
        (
            """<p class="lesson-p">2. Vẽ một bảng gồm hai cột để so sánh sự khác nhau giữa AI ở thế hệ trước và AI tạo sinh. Mỗi cột nêu các đặc điểm như: nhiệm vụ thực hiện, cách tạo ra kết</p>
<p class="lesson-p">quả, khả năng thay đổi nội dung,....

3. Sử dụng công cụ khác của AI tạo sinh để tạo nội dung mới. Em hãy chọn một công cụ AI tạo sinh khác với bài học (ví dụ: Bing Image Creator, Gemini,</p>""",
            """<p class="lesson-p">2. Vẽ một bảng gồm hai cột để so sánh sự khác nhau giữa AI ở thế hệ trước và AI tạo sinh. Mỗi cột nêu các đặc điểm như: nhiệm vụ thực hiện, cách tạo ra kết quả, khả năng thay đổi nội dung,...</p>
<p class="lesson-p">3. Sử dụng công cụ khác của AI tạo sinh để tạo nội dung mới. Em hãy chọn một công cụ AI tạo sinh khác với bài học (ví dụ: Bing Image Creator, Gemini, Copilot,...).</p>""",
        ),
        (
            """<p class="lesson-p">1. Em hãy sử dụng một công cụ AI tạo sinh (như ChatGPT, Gemini hoặc công cụ tương tự) để tạo một tấm thiệp chúc mừng sinh nhật dành tặng cho một người bạn. Thiệp cần có:

- Một hình ảnh minh hoa phù hợp với chủ đề sinh nhật.</p>
<ul class="lesson-bullet-list">
<li>Một lời chúc sinh nhật do em tự nghĩ hoặc do AI gợi ý, thể hiện tình cảm</li>
</ul>
<p class="lesson-p">Sau khi hoàn thành, em hãy chia sẻ sản phẩm của minh với bạn bè hoặc thầy</p>
<p class="lesson-p">cô giáo, đồng thời nêu cảm nhận về việc sử dụng AI đề hỗ trợ sáng tạo.</p>""",
            """<p class="lesson-p">1. Em hãy sử dụng một công cụ AI tạo sinh (như ChatGPT, Gemini hoặc công cụ tương tự) để tạo một tấm thiệp chúc mừng sinh nhật dành tặng cho một người bạn. Thiệp cần có:</p>
<ul class="lesson-bullet-list">
<li>Một hình ảnh minh hoạ phù hợp với chủ đề sinh nhật.</li>
<li>Một lời chúc sinh nhật do em tự nghĩ hoặc do AI gợi ý, thể hiện tình cảm chân thành.</li>
</ul>
<p class="lesson-p">Sau khi hoàn thành, em hãy chia sẻ sản phẩm của mình với bạn bè hoặc thầy cô giáo, đồng thời nêu cảm nhận về việc sử dụng AI để hỗ trợ sáng tạo.</p>""",
        ),
    ],
    "bai-3-mo-hinh-ngon-ngu-lon": [
        ("một số mô hình ngôn ngữ lớn phố biến.", "một số mô hình ngôn ngữ lớn phổ biến."),
        ("tạo ảnh tử văn bản.", "tạo ảnh từ văn bản."),
        ("một số mô hình phố biến hiện nay", "một số mô hình phổ biến hiện nay"),
        ("bạn Minh tò mò hồi:", "bạn Minh tò mò hỏi:"),
        (
            '<ul class="lesson-bullet-list">\n<li>Thưa thầy, làm sao AI có thể vẽ tranh chỉ bằng một yêu cầu như "Vẽ một lớp</li>\n</ul>\n<p class="lesson-p">học đang học bài dưới tán cây xanh" a?</p>',
            '<ul class="lesson-bullet-list">\n<li>Thưa thầy, làm sao AI có thể vẽ tranh chỉ bằng một yêu cầu như "Vẽ một lớp học đang học bài dưới tán cây xanh" ạ?</li>\n</ul>',
        ),
        (
            '<ul class="lesson-bullet-list">\n<li>Câu hỏi rất hay! Đằng sau việc đó là cả một quá trình xử lí phức tạp mà mô hình</li>\n</ul>\n<p class="lesson-p">AI - cụ thể là mô hình ngôn ngữ lớn đã được huấn luyện từ rất nhiều dữ liệu.\n\nKhông chỉ vậy, AI còn chia nhỏ câu văn thành các phần nhỏ và dựa vào cách các phần đó liên kết với nhau để hiểu ý nghĩa. Nhờ đó, AI mới có thể tạo ra nội dung phù hợp với yêu cầu.</p>',
            '<ul class="lesson-bullet-list">\n<li>Câu hỏi rất hay! Đằng sau việc đó là cả một quá trình xử lí phức tạp mà mô hình AI – cụ thể là mô hình ngôn ngữ lớn – đã được huấn luyện từ rất nhiều dữ liệu. Không chỉ vậy, AI còn chia nhỏ câu văn thành các phần nhỏ và dựa vào cách các phần đó liên kết với nhau để hiểu ý nghĩa. Nhờ đó, AI mới có thể tạo ra nội dung phù hợp với yêu cầu.</li>\n</ul>',
        ),
        ('<p class="lesson-p">C\'S</p>\n', ""),
        (
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Hãy mô tả cách em tưởng tượng mô hình tạo ra hình ảnh từ văn bản.</h3>',
            '<p class="lesson-p">2. Hãy mô tả cách em tưởng tượng mô hình tạo ra hình ảnh từ văn bản.</p>',
        ),
        ("3. Hãy lấy ví dự về việc chia một câu", "3. Hãy lấy ví dụ về việc chia một câu"),
        (
            '<p class="lesson-p">KHÁM PHÁ</p>',
            '</div></section>' + section_open("discovery-section", "sec-khám-phá", "🔍", "KHÁM PHÁ"),
        ),
        (
            '<p class="lesson-p">1. Khái niệm mô hình ngôn ngữ lớn Trong phần Khởi động, thầy giáo đã giới thiệu mô hình ngôn ngữ lớn là một loại AI</p>\n'
            '<p class="lesson-p">có khả năng xử lí ngôn ngữ. Các mô hình này được huấn luyện bằng cách học từ một lượng rất lớn văn bản, bao gồm sách, bài viết, hội thoại và nhiều loại tải liệu khác và trong một số hệ thống, chúng có thể được kết hợp với dữ liệu hình ảnh hoặc âm thanh.</p>',
            '<h3 class="subheading-h3"><span class="h3-num">1.</span> Khái niệm mô hình ngôn ngữ lớn</h3>\n'
            '<p class="lesson-p">Trong phần Khởi động, thầy giáo đã giới thiệu mô hình ngôn ngữ lớn là một loại AI có khả năng xử lí ngôn ngữ. Các mô hình này được huấn luyện bằng cách học từ một lượng rất lớn văn bản, bao gồm sách, bài viết, hội thoại và nhiều loại tài liệu khác và trong một số hệ thống, chúng có thể được kết hợp với dữ liệu hình ảnh hoặc âm thanh.</p>',
        ),
        (
            "hỗ trợ viết văn Hình 3.1. Mô hình ngôn ngữ lớn bản, dịch thuật, tóm tắt nội dung hoặc đưa ra gợi ý phù hợp với yêu cầu của người dùng. Đày là lí do mô hình ngôn ngữ lớn",
            "hỗ trợ viết văn bản, dịch thuật, tóm tắt nội dung hoặc đưa ra gợi ý phù hợp với yêu cầu của người dùng. Đây là lí do mô hình ngôn ngữ lớn",
        ),
        ("được sử dựng rộng rãi", "được sử dụng rộng rãi"),
        (
            '<p class="lesson-p">Một số mô hình ngôn ngữ lớn hiện nay đang được sử dụng phổ biến gồm: ChatGPT,</p>\n'
            '<p class="lesson-p">Gemini, Claude. Các mô hình này đều có thể trò chuyện, hỗ trợ viết bài hoặc tạo nội dung theo yêu cầu bằng tiếng Việt và nhiều ngôn ngữ khác.</p>',
            '<p class="lesson-p">Một số mô hình ngôn ngữ lớn hiện nay đang được sử dụng phổ biến gồm: ChatGPT, Gemini, Claude. Các mô hình này đều có thể trò chuyện, hỗ trợ viết bài hoặc tạo nội dung theo yêu cầu bằng tiếng Việt và nhiều ngôn ngữ khác.</p>',
        ),
        (
            '<p class="lesson-p">Mô hình ngôn ngữ lớn (Large Language Model -\n\nLLM) là một loại AI được huấn luyện trên lượng lớn dữ liệu văn bản và đôi khi kết hợp với dữ liệu từ các dạng khác như hình ảnh, âm thanh. LLM có khả năng hiểu và tạo ra ngôn ngữ, hỗ trợ con người trong</p>\n'
            '<p class="lesson-p">các hoạt động như viết nội dung, trả lời câu hỏi, dịch thuật hoặc tạo hình ảnh, âm thanh từ mô tả</p>',
            '<p class="lesson-p">Mô hình ngôn ngữ lớn (Large Language Model – LLM) là một loại AI được huấn luyện trên lượng lớn dữ liệu văn bản và đôi khi kết hợp với dữ liệu từ các dạng khác như hình ảnh, âm thanh. LLM có khả năng hiểu và tạo ra ngôn ngữ, hỗ trợ con người trong các hoạt động như viết nội dung, trả lời câu hỏi, dịch thuật hoặc tạo hình ảnh, âm thanh từ mô tả.</p>',
        ),
        (
            '<span class="h3-num">2.</span> Sử dụng được LLM để tạo hình ánh từ văn bản</h3>',
            '<span class="h3-num">2.</span> Sử dụng được LLM để tạo hình ảnh từ văn bản</h3>',
        ),
        (
            '<p class="lesson-p">Khi người dùng nhập một đoạn mô tả bằng lời, LLM sẽ tiếp nhận và phân tích nội dung ngôn ngữ trong đoạn văn. Từ đó, hệ thống sẽ xác định các tử khóa và chí tiết như "lớp học", "tán cây"."học bài", rồi chuyển những thông tn này sang dạng dữ liệu phù hợp để mô hình tạo ảnh xử lí. Kết quả là một bức tranh được tạo ra dựa</p>\n'
            '<p class="lesson-p">trên mô tả ngôn ngữ ban đầu.</p>',
            '<p class="lesson-p">Khi người dùng nhập một đoạn mô tả bằng lời, LLM sẽ tiếp nhận và phân tích nội dung ngôn ngữ trong đoạn văn. Từ đó, hệ thống sẽ xác định các từ khoá và chi tiết như "lớp học", "tán cây", "học bài", rồi chuyển những thông tin này sang dạng dữ liệu phù hợp để mô hình tạo ảnh xử lí. Kết quả là một bức tranh được tạo ra dựa trên mô tả ngôn ngữ ban đầu.</p>',
        ),
        ('<p class="lesson-p">Vẽ một lớp học</p>\n<p class="lesson-p">đang học bài dưới tán cây xanh</p>\n', ""),
        ("LLM có thể tạo ảnh từ ván bản", "LLM có thể tạo ảnh từ văn bản"),
        (
            '<p class="lesson-p">Để làm được điều này, hệ thống cần được huấn luyện từ trước với một lượng lớn dữ liệu gồm các cặp văn bản - hình ảnh. quá trình huấn luyện này giúp mô hình học được cách liên kết giữa ngôn ngữ mô tả và các đặc điểm hình ảnh tương ứng.\n\n'
            'Khả năng chuyển đổi từ văn bản thành hình ảnh giúp mô hình không chỉ hiểu ngôn ngữ mà còn hỗ trợ con người thế hiện ý tưởng một cách sinh động và trực</p>',
            '<p class="lesson-p">Để làm được điều này, hệ thống cần được huấn luyện từ trước với một lượng lớn dữ liệu gồm các cặp văn bản – hình ảnh. Quá trình huấn luyện này giúp mô hình học được cách liên kết giữa ngôn ngữ mô tả và các đặc điểm hình ảnh tương ứng.</p>\n'
            '<p class="lesson-p">Khả năng chuyển đổi từ văn bản thành hình ảnh giúp mô hình không chỉ hiểu ngôn ngữ mà còn hỗ trợ con người thể hiện ý tưởng một cách sinh động và trực quan hơn.</p>',
        ),
        ("hình ảnh đề biến văn bản", "hình ảnh để biến văn bản"),
        (
            '<p class="lesson-p">Sử dụng Gemini đề tạo hình ảnh từ văn bản</p>\n<p class="lesson-p">Hướng dẫn:</p>',
            '<p class="lesson-p">Sử dụng Gemini để tạo hình ảnh từ văn bản</p>\n'
            '<p class="lesson-p">Hướng dẫn:</p>\n'
            '<p class="lesson-p">(Hình ảnh và hướng dẫn thực hành sau đây sử dụng Gemini.)</p>\n'
            '<p class="lesson-p">Bước 1. Truy cập công cụ Gemini.</p>\n'
            '<p class="lesson-p">Mở trình duyệt và vào trang web: https://gemini.google.com/.</p>\n'
            '<p class="lesson-p">Bước 2. Đăng nhập tài khoản Google.</p>\n'
            '<p class="lesson-p">Chọn Sign in trên màn hình và nhập tài khoản Google của em (nếu chưa có tài khoản Google thì cần tạo tài khoản bằng cách chọn Create account.)</p>',
        ),
        (
            """<p class="lesson-p">Tạo một bức tranh về mùa xuân</p>
<p class="lesson-p"></p>
<p class="lesson-p">Bạn có muốn tôi tạo thêm hình ảnh nào nữa không?</p>
<p class="lesson-p">Đây là một bức tranh về mùa xuân</p>
<p class="lesson-p">Ask Gemini</p>
<p class="lesson-p">+ @ Deep Research</p>""",
            "",
        ),
        (
            '<ul class="lesson-bullet-list">\n<li>Yêu cầu 2: "Tạo một bức tranh về mùa xuân có nắng nhẹ, hoa đào nở và cảnh</li>\n</ul>\n'
            '<p class="lesson-p">lộc non, phù hợp để dùng trong hoạt động tuyên truyền của câu lạc bộ Văn học</p>\n'
            '<p class="lesson-p">trường Trung học phổ thông."</p>',
            '<ul class="lesson-bullet-list">\n<li>Yêu cầu 2: "Tạo một bức tranh về mùa xuân có nắng nhẹ, hoa đào nở và cành lộc non, phù hợp để dùng trong hoạt động tuyên truyền của câu lạc bộ Văn học trường Trung học phổ thông."</li>\n</ul>',
        ),
        (
            '<p class="lesson-p">3. Token và cách LLM xử lí văn bản bằng token</p>',
            '<h3 class="subheading-h3"><span class="h3-num">3.</span> Token và cách LLM xử lí văn bản bằng token</h3>',
        ),
        (
            """<p class="lesson-p">TOKEN</p>
<p class="lesson-p">Để tạo ra hình ánh hoặc xử lí văn bản, mô</p>
<p class="lesson-p">Minh Gang học bài hình cần chia nhỏ nội dung đầu vào thành các phần gọi là token. Đây là bước đầu tiên trong quá trình xử lí ngôn ngữ của mô hình AI.</p>
<p class="lesson-p">Token là những đơn vị nhỏ trong văn bản, có thể là từ, âm tiết hoặc cụm kí tự.

Việc chia văn bản thành các token giúp</p>
<p class="lesson-p">Token trong LLM với nội dung "Minh đang học bài" mô hình dễ dàng phân tích và tính toán.</p>""",
            """<p class="lesson-p">Để tạo ra hình ảnh hoặc xử lí văn bản, mô hình cần chia nhỏ nội dung đầu vào thành các phần gọi là token. Đây là bước đầu tiên trong quá trình xử lí ngôn ngữ của mô hình AI.</p>
<p class="lesson-p">Token là những đơn vị nhỏ trong văn bản, có thể là từ, âm tiết hoặc cụm kí tự. Việc chia văn bản thành các token giúp mô hình dễ dàng phân tích và tính toán.</p>""",
        ),
        (
            '<p class="lesson-p">Ví dụ, với câu "Minh đang học bài", mô hình có thể chia thành các token là:\n\n"Minh", "đang", "học", "bài". Trong trường hợp khác, một cụm như "máy tính xách tay" cũng có thể được chia thành các token là: "máy tính". "xách tay"</p>',
            '<p class="lesson-p">Ví dụ, với câu "Minh đang học bài", mô hình có thể chia thành các token là: "Minh", "đang", "học", "bài". Trong trường hợp khác, một cụm như "máy tính xách tay" cũng có thể được chia thành các token là: "máy tính", "xách tay".</p>',
        ),
        (
            "đặc biệt là khi gặp những từ phức hoặc ít xuất hiện trong</p>",
            "đặc biệt là khi gặp những từ phức hoặc ít xuất hiện trong dữ liệu.</p>",
        ),
        (
            '<p class="lesson-p">Sau khi chía văn bản thành token, mô hình sẽ dự đoán token tiếp theo dựa trên những gì đã có. Chăng hạn, nếu người dùng nhập "Hà Nội là thủ đô của ..</p>\n'
            '<p class="lesson-p">hình có thể dự đoán tiếp là "Việt Nam". Quá trình này lặp lại liên tục cho đến khi tạo thành một câu hoặc đoạn văn hoàn chỉnh.</p>',
            '<p class="lesson-p">Sau khi chia văn bản thành token, mô hình sẽ dự đoán token tiếp theo dựa trên những gì đã có. Chẳng hạn, nếu người dùng nhập "Hà Nội là thủ đô của ...", mô hình có thể dự đoán tiếp là "Việt Nam". Quá trình này lặp lại liên tục cho đến khi tạo thành một câu hoặc đoạn văn hoàn chỉnh.</p>',
        ),
        (
            '<p class="lesson-p">Để làm được việc dự đoán này, mô hình được cung cấp một lượng lớn văn bản để học cách phát hiện các mối liên hệ giữa các phần trong câu. Khi người dùng nhập vào một đoạn văn bản, mô hình sẽ phân tích các token đã có để dự đoán token tiếp theo sao cho phù hợp với ngữ cảnh. Token mới sẽ được thêm vào</p>\n'
            '<p class="lesson-p">chuỗi và mô hình tiếp tục dự đoán token kế tiếp cho đến khi hoàn thành câu hoặc</p>',
            '<p class="lesson-p">Để làm được việc dự đoán này, mô hình được cung cấp một lượng lớn văn bản để học cách phát hiện các mối liên hệ giữa các phần trong câu. Khi người dùng nhập vào một đoạn văn bản, mô hình sẽ phân tích các token đã có để dự đoán token tiếp theo sao cho phù hợp với ngữ cảnh. Token mới sẽ được thêm vào chuỗi và mô hình tiếp tục dự đoán token kế tiếp cho đến khi hoàn thành câu hoặc đoạn văn.</p>',
        ),
        (
            '<p class="lesson-p">Token là những đơn vị nhỏ của văn bản mà mô hình AI cần tách ra để xử lí. Mô hình ngôn ngữ lớn học bằng cách dự đoán token tiếp theo trong chuỗi văn bản. Quá trình dự đoán lặp lại giúp hình thành</p>\n'
            '<p class="lesson-p">câu hoặc đoạn văn phù hợp với nội dung đầu vào.</p>',
            '<p class="lesson-p">Token là những đơn vị nhỏ của văn bản mà mô hình AI cần tách ra để xử lí. Mô hình ngôn ngữ lớn học bằng cách dự đoán token tiếp theo trong chuỗi văn bản. Quá trình dự đoán lặp lại giúp hình thành câu hoặc đoạn văn phù hợp với nội dung đầu vào.</p>',
        ),
        ("1. Công cụ Ai mà bạn Nam sữ dụng", "1. Công cụ AI mà bạn Nam sử dụng"),
        (
            '<p class="lesson-p">C. Mô hình ngôn ngữ lớn giúp Nam viết văn, dịch ngôn ngữ và tạo hình ảnh từ</p>',
            '<p class="lesson-p">C. Mô hình ngôn ngữ lớn giúp Nam viết văn, dịch ngôn ngữ và tạo hình ảnh từ mô tả.</p>',
        ),
        ("B. Tìm kiểm đoạn văn tương tự trên Internet.", "B. Tìm kiếm đoạn văn tương tự trên Internet."),
        ("D. Dịch đoạn văn sang ngôn ngừ khác trước khi xử lí.", "D. Dịch đoạn văn sang ngôn ngữ khác trước khi xử lí."),
        (
            "Kết quả mà hai bạn nhận được có sự khác biệt</p>",
            "Kết quả mà hai bạn nhận được có sự khác biệt rõ rệt.</p>",
        ),
        (
            "Nguồn dữ liệu đó có thể đến</p>",
            "Nguồn dữ liệu đó có thể đến từ đâu?</p>",
        ),
        ("3. a) Em hãy nhập hai yêu câu sau vào một công cụ AI tạo vàn bản:", "3. a) Em hãy nhập hai yêu cầu sau vào một công cụ AI tạo văn bản:"),
        ("kể lại một ki niệm đáng nhớ", "kể lại một kỉ niệm đáng nhớ"),
        (
            '<p class="lesson-p">Theo em, nếu chỉ có "Mùa hè đến, ve kêu ..." thì AI sẽ dự đoán từ nào tiếp theo?\n\nVì sao?</p>',
            '<p class="lesson-p">Theo em, nếu chỉ có "Mùa hè đến, ve kêu ..." thì AI sẽ dự đoán từ nào tiếp theo? Vì sao?</p>',
        ),
        ('<p class="lesson-p">24 25</p>\n', ""),
    ],
    "bai-4-du-lieu-huan-luyen": [
        ('<p class="lesson-p">BÀI 4: DỮ LIỆU HUẤN LUYỆN</p>\n', ""),
        (
            "<li>Trình bảy được tầm quan trọng của dữ liệu đối với việc huấn luyện mô hình Ai tạo sinh.</li>",
            "<li>Trình bày được tầm quan trọng của dữ liệu đối với việc huấn luyện mô hình AI tạo sinh.</li>",
        ),
        (
            "<li>Giái thich được chất lượng của dữ liệu và số lượng dữ liệu ành hưởng lớn đến kết quả của Ai.</li>",
            "<li>Giải thích được chất lượng của dữ liệu và số lượng dữ liệu ảnh hưởng lớn đến kết quả của AI.</li>",
        ),
        (
            '<p class="lesson-p">Trường Trung học phổ thông An Phú lổ chức cuộc thi sáng tạo khoa học. Một nhóm học sinh lớp 10 phát triển chatbot AI để hỗ trợ học tập. Dữ liệu huấn luyện ban đầu của chatbot chỉ tập trung vào món Vật lí lớp 10. Khi thử nghiệm,</p>\n'
            '<p class="lesson-p">chatbot trả lời khá tốt các câu hỏi liên quan đến Vật lí, nhưng thường xuyên không hiểu hoặc trả lời sai khi được hỏi về các môn khác như Toán, Hóa học hay Sinh học. Nhóm nghi ngờ rằng chatbot hoạt động chưa hiệu quả do dữ liệu huấn luyện còn hạn chế, mới chỉ bao phủ một môn học duy nhất.</p>',
            '<p class="lesson-p">Trường Trung học phổ thông An Phú tổ chức cuộc thi sáng tạo khoa học. Một nhóm học sinh lớp 10 phát triển chatbot AI để hỗ trợ học tập. Dữ liệu huấn luyện ban đầu của chatbot chỉ tập trung vào môn Vật lí lớp 10. Khi thử nghiệm, chatbot trả lời khá tốt các câu hỏi liên quan đến Vật lí, nhưng thường xuyên không hiểu hoặc trả lời sai khi được hỏi về các môn khác như Toán, Hóa học hay Sinh học. Nhóm nghi ngờ rằng chatbot hoạt động chưa hiệu quả do dữ liệu huấn luyện còn hạn chế, mới chỉ bao phủ một môn học duy nhất.</p>',
        ),
        ("trong quá trịnh huấn luyện AI như chatbot trên?", "trong quá trình huấn luyện AI như chatbot trên?"),
        (
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Em hãy kể tên một số loại dữ liệu mà AI có thể sử dụng đề huấn luyện.</h3>',
            '<p class="lesson-p">2. Em hãy kể tên một số loại dữ liệu mà AI có thể sử dụng để huấn luyện.</p>',
        ),
        (
            '<p class="lesson-p">KHÁM PHẢ</p>',
            '</div></section>' + section_open("discovery-section", "sec-khám-phá", "🔍", "KHÁM PHÁ"),
        ),
        (
            '<span class="h3-num">1.</span> Tầm quan trọng của dữ liệu đối với việc huấn luyện mô hình Ai</h3>',
            '<span class="h3-num">1.</span> Tầm quan trọng của dữ liệu đối với việc huấn luyện mô hình AI</h3>',
        ),
        (
            '<p class="lesson-p">Trong tịnh huống Khởi động, chatbot mà nhóm học sinh phát triển chỉ hoạt động tốt với các câu hỏi liên quan đến môn Vật lí lớp 10 - là lình vưc duy nhất có trong dữ liệu huấn luyện ban đầu. Khi nhận câu hỏi thuộc các món học khác như Toán.\n\nHóa học hay Sinh học, chatbot thường không đưa ra được câu trả lời phù hợp.\n\nTình huống này cho thấy, phạm vi dữ liệu huấn luyện có ảnh hưởng trực tiếp đến khả năng phản hồi của mô hình AI. Mô hình có xu hướng phản hồi chính xác hơn trong những lĩnh vực mà nó đã được cung cấp dữ liệu đầy đủ và gặp khó khăn với những nội dung nằm ngoài phạm vi dữ liệu đã học.</p>',
            '<p class="lesson-p">Trong tình huống Khởi động, chatbot mà nhóm học sinh phát triển chỉ hoạt động tốt với các câu hỏi liên quan đến môn Vật lí lớp 10 – là lĩnh vực duy nhất có trong dữ liệu huấn luyện ban đầu. Khi nhận câu hỏi thuộc các môn học khác như Toán, Hóa học hay Sinh học, chatbot thường không đưa ra được câu trả lời phù hợp.</p>\n'
            '<p class="lesson-p">Tình huống này cho thấy, phạm vi dữ liệu huấn luyện có ảnh hưởng trực tiếp đến khả năng phản hồi của mô hình AI. Mô hình có xu hướng phản hồi chính xác hơn trong những lĩnh vực mà nó đã được cung cấp dữ liệu đầy đủ và gặp khó khăn với những nội dung nằm ngoài phạm vi dữ liệu đã học.</p>',
        ),
        (
            '<p class="lesson-p">Trong các mô hình AI tạo sinh, dữ liệu huấn luyện có vai trò cung cấp nền tảng để mô hình học cách tạo ra nội dung mới như viết đoạn văn, giải thích hoặc trả lới</p>\n'
            '<p class="lesson-p">câu hỏi. Thông qua quá trình huần luyện, mô hình xây dựng được khả năng sử dụng ngôn ngữ, nhận diện ngữ cảnh và tạo phản hồi phù hợp với từng tình huống</p>',
            '<p class="lesson-p">Trong các mô hình AI tạo sinh, dữ liệu huấn luyện có vai trò cung cấp nền tảng để mô hình học cách tạo ra nội dung mới như viết đoạn văn, giải thích hoặc trả lời câu hỏi. Thông qua quá trình huấn luyện, mô hình xây dựng được khả năng sử dụng ngôn ngữ, nhận diện ngữ cảnh và tạo phản hồi phù hợp với từng tình huống.</p>',
        ),
        (
            '<p class="lesson-p">Dữ liệu huấn luyện là nguồn thông tin quan trọng giúp mô hình AI tạo sinh có thể học và hoạt động</p>\n'
            '<p class="lesson-p">được. Nếu không có dữ liệu, mô hình sẽ không có cơ sở để tạo ra nội dung theo yêu cầu.</p>',
            '<p class="lesson-p">Dữ liệu huấn luyện là nguồn thông tin quan trọng giúp mô hình AI tạo sinh có thể học và hoạt động được. Nếu không có dữ liệu, mô hình sẽ không có cơ sở để tạo ra nội dung theo yêu cầu.</p>',
        ),
        (
            '<p class="lesson-p">Để mô hình AI tạo ra được nội dung phù hợp với yêu cầu của người dùng, trước hết mô hình cần được huấn luyện từ những dữ liệu liên quan. Tuỳ theo mục địch sử dụng, AI có thể học từ nhiều loại dữ liệu khác nhau như văn bản, hình ảnh,</p>\n'
            '<p class="lesson-p">âm thanh hoặc video. Mỗi loại dữ liệu sẽ giúp mô hình học được những đặc điểm khác nhau trong việc xử lí và sinh nội dung</p>',
            '<p class="lesson-p">Để mô hình AI tạo ra được nội dung phù hợp với yêu cầu của người dùng, trước hết mô hình cần được huấn luyện từ những dữ liệu liên quan. Tuỳ theo mục đích sử dụng, AI có thể học từ nhiều loại dữ liệu khác nhau như văn bản, hình ảnh, âm thanh hoặc video. Mỗi loại dữ liệu sẽ giúp mô hình học được những đặc điểm khác nhau trong việc xử lí và sinh nội dung.</p>',
        ),
        (
            '<p class="lesson-p">Ví dụ, mô hình Ai dùng trong học tiếng</p>\n'
            '<p class="lesson-p">Anh cần được học từ các đoạn văn, từ điển, bài tập ngữ pháp và bản dịch có độ chính xác cao. Trong lĩnh vực nhận dạng hình ảnh, để phân biệt được các loài hoa, mô hình AI phải được cung</p>\n'
            '<p class="lesson-p">cấp nhiều hình ảnh khác nhau về mỗi loài hoa, hoặc có thể là video quay nhiều hướng của loài hoa đó, học cách nhận biết đặc điểm riêng của từng loài.\n\nHình 4.1. Các loại dữ liệu có thể dùng cho huấn luyện AI tạo sinh</p>',
            '<p class="lesson-p">Ví dụ, mô hình AI dùng trong học tiếng Anh cần được học từ các đoạn văn, từ điển, bài tập ngữ pháp và bản dịch có độ chính xác cao. Trong lĩnh vực nhận dạng hình ảnh, để phân biệt được các loài hoa, mô hình AI phải được cung cấp nhiều hình ảnh khác nhau về mỗi loài hoa, hoặc có thể là video quay nhiều hướng của loài hoa đó, học cách nhận biết đặc điểm riêng của từng loài.</p>',
        ),
        (
            'alt="Hình 4.1. Các loại dữ liệu có thể"',
            'alt="Hình 4.1. Các loại dữ liệu có thể dùng cho huấn luyện AI tạo sinh"',
        ),
        (
            '<figcaption class="figure-caption"><strong>Hình 4.1.</strong> Các loại dữ liệu có thể</figcaption>',
            '<figcaption class="figure-caption"><strong>Hình 4.1.</strong> Các loại dữ liệu có thể dùng cho huấn luyện AI tạo sinh</figcaption>',
        ),
        (
            "Ngoài văn bản và hình ảnh, mó hình AI còn có thể được huấn luyện bằng âm thanh hoặc video tuy theo chức năng cần thực hiện. Các nguồn cung cấp dữ liệu bao gồm Internet, kho dữ liệu công khai, tài liệu nghiên cửu,",
            "Ngoài văn bản và hình ảnh, mô hình AI còn có thể được huấn luyện bằng âm thanh hoặc video tuỳ theo chức năng cần thực hiện. Các nguồn cung cấp dữ liệu bao gồm Internet, kho dữ liệu công khai, tài liệu nghiên cứu,",
        ),
        ('<p class="lesson-p">Al</p>\n', ""),
        (
            'alt="Hình 4.2. Chất lượng của dữ liệu và số lượng dữ liệu huấn luyện"',
            'alt="Hình 4.2. Chất lượng của dữ liệu và số lượng dữ liệu huấn luyện ảnh hưởng đến kết quả mô hình AI"',
        ),
        (
            '<figcaption class="figure-caption"><strong>Hình 4.2.</strong> Chất lượng của dữ liệu và số lượng dữ liệu huấn luyện</figcaption>',
            '<figcaption class="figure-caption"><strong>Hình 4.2.</strong> Chất lượng của dữ liệu và số lượng dữ liệu huấn luyện ảnh hưởng đến kết quả mô hình AI</figcaption>',
        ),
        ('<p class="lesson-p">ảnh hưởng đến kết quả mô hình AI</p>\n', ""),
        (
            '<p class="lesson-p">Để mô hình AI hoạt động hiệu quả, không chỉ cần dữ liệu để huấn luyện má còn</p>\n'
            '<p class="lesson-p">cần dữ liệu có chất lượng đù tốt và số lượng đủ nhiều. Chất lượng của dữ liệu và số lượng dữ liệu đóng vai trò quan trọng trong việc giúp mô hình học đúng và tạo ra nội dung phù hợp với yêu cầu. Cả hai yếu tố này đều rất quan trọng trong việc</p>\n'
            '<p class="lesson-p">huấn luyện năng lực tạo sinh của mô hình AI.</p>',
            '<p class="lesson-p">Để mô hình AI hoạt động hiệu quả, không chỉ cần dữ liệu để huấn luyện mà còn cần dữ liệu có chất lượng đủ tốt và số lượng đủ nhiều. Chất lượng của dữ liệu và số lượng dữ liệu đóng vai trò quan trọng trong việc giúp mô hình học đúng và tạo ra nội dung phù hợp với yêu cầu. Cả hai yếu tố này đều rất quan trọng trong việc huấn luyện năng lực tạo sinh của mô hình AI.</p>',
        ),
        (
            'điều kiện lí tường thì ô tô tự lái có thể gặp khó khăn khi phải</p>\n<p class="lesson-p">di chuyển vào ban đêm hoặc trong điều kiện thời tiết xấu.</p>',
            'điều kiện lí tưởng thì ô tô tự lái có thể gặp khó khăn khi phải di chuyển vào ban đêm hoặc trong điều kiện thời tiết xấu.</p>',
        ),
        (
            '<p class="lesson-p">Trong huấn luyện mô hình AI tạo sinh, chất lượng của dữ liêu đóng vai trò quan trọng hơn số lượng dữ liệu. Một mô hình AI được huấn luyện từ ít dữ liệu nhưng rõ ràng, chính xác và phù hợp vẫn có thể cho kết quả đúng. Trong khi đó, nếu dữ liệu huân luyện quá nhiều nhưng không chỉnh xác hoặc không phù hợp, mô hình</p>\n'
            '<p class="lesson-p">AI tạo sinh sẽ dễ học sai và cho kết quả không hợp lí.</p>',
            '<p class="lesson-p">Trong huấn luyện mô hình AI tạo sinh, chất lượng của dữ liệu đóng vai trò quan trọng hơn số lượng dữ liệu. Một mô hình AI được huấn luyện từ ít dữ liệu nhưng rõ ràng, chính xác và phù hợp vẫn có thể cho kết quả đúng. Trong khi đó, nếu dữ liệu huấn luyện quá nhiều nhưng không chính xác hoặc không phù hợp, mô hình AI tạo sinh sẽ dễ học sai và cho kết quả không hợp lí.</p>',
        ),
        (
            '<p class="lesson-p">Dữ liệu huấn luyện càng có chất lượng và số lượng đù nhiều thì mô hình AI càng học đúng, hiểu được nhiều tình huống và cho kết quả càng chính xác.\n\nNếu dữ liệu ít hoặc sai lệch, AI dễ học sai và cho kết quả không hợp lí.</p>',
            '<p class="lesson-p">Dữ liệu huấn luyện càng có chất lượng và số lượng đủ nhiều thì mô hình AI càng học đúng, hiểu được nhiều tình huống và cho kết quả càng chính xác.</p>\n'
            '<p class="lesson-p">Nếu dữ liệu ít hoặc sai lệch, AI dễ học sai và cho kết quả không hợp lí.</p>',
        ),
        (
            '<p class="lesson-p">LUYỆN TẬP</p>',
            '</div></section>' + section_open("exercise-section", "sec-luyện-tập", "✏️", "LUYỆN TẬP"),
        ),
        (
            'chỉ được huấn luyện với ảnh chụp</p>\n<p class="lesson-p">các món ăn theo góc nhìn từ trên xuống, trong khi ành của món bún bò Huế dũng để nhận dạng được chụp ở góc nghiêng và thiếu dữ liệu huấn luyện về món này.</p>',
            'chỉ được huấn luyện với ảnh chụp các món ăn theo góc nhìn từ trên xuống, trong khi ảnh của món bún bò Huế dùng để nhận dạng được chụp ở góc nghiêng và thiếu dữ liệu huấn luyện về món này.</p>',
        ),
        ("C. Độ phong phú và đa dang của dữ liệu huấn luyện.", "C. Độ phong phú và đa dạng của dữ liệu huấn luyện."),
        (
            "3. Muốn mô hình AI đó cải thiện khả nhận dạng món ăn, nhóm học sinh nên làm gì?",
            "3. Muốn mô hình AI đó cải thiện khả năng nhận dạng món ăn, nhóm học sinh nên làm gì?",
        ),
        (
            '<p class="lesson-p">A. Giảm độ phân giải ảnh.\n\nB. Chụp thêm nhiều ảnh cáo món ăn ở nhiều góc độ và điều kiện ánh sáng</p>\n<p class="lesson-p">khác nhau.</p>',
            '<p class="lesson-p">A. Giảm độ phân giải ảnh.</p>\n<p class="lesson-p">B. Chụp thêm nhiều ảnh các món ăn ở nhiều góc độ và điều kiện ánh sáng khác nhau.</p>',
        ),
        ("Khi thứ nghiệm, hệ thống không thể nhận dạng", "Khi thử nghiệm, hệ thống không thể nhận dạng"),
        (
            """<p class="lesson-p">CHỦ ĐẾ 2. KHÂM PHÁ CÔNG CỤ</p>
<p class="lesson-p">VÀ ỨNG DỤNG AI</p>
<p class="lesson-p">PROMPT AI</p>
<p class="lesson-p">CONTENT</p>
<p class="lesson-p">IMAGE</p>
<p class="lesson-p"></p>
<p class="lesson-p">balat</p>\n""",
            "",
        ),
    ],
    "bai-5-prompt-giao-tiep-voi-ai-tao-sinh": [
        ('<p class="lesson-p">BÃI 5. PROMPT -\n\nGIAO TIẾP VỚI AI TẠO SINH</p>\n', ""),
        ("muốn có hình minh hoa phù hợp", "muốn có hình minh hoạ phù hợp"),
        ('nhập yêu cầu: "Tạo ành công chúa"', 'nhập yêu cầu: "Tạo ảnh công chúa"'),
        ("phong cách minh hoa sách thiếu nhi,", "phong cách minh hoạ sách thiếu nhi,"),
        (
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Minh đã thay đổi nội dung yêu cầu nhập cho AI tạo sinh như thế nào?</h3>',
            '<p class="lesson-p">2. Minh đã thay đổi nội dung yêu cầu nhập cho AI tạo sinh như thế nào?</p>',
        ),
        (
            '<h3 class="subheading-h3"><span class="h3-num">4.</span> Khi thay đổi một chi tiết trong prompt, kết quả AI tạo ra sẽ thay đổi ra sao?</h3>',
            '<p class="lesson-p">4. Khi thay đổi một chi tiết trong prompt, kết quả AI tạo ra sẽ thay đổi ra sao?</p>',
        ),
        (
            '<p class="lesson-p">Prompt (yêu cầu) là nội dung mà người dùng nhập vào để hướng dẫn công cụ AI tạo ra kết quả theo mục tiêu đặt ra. Một prompt rõ ràng giúp hệ thống dễ hiểu và phản hồi chính xác hơn. Ngược lại, nếu prompt</p>\n'
            '<p class="lesson-p">chung chung hoặc thiêu thông tin, kết quả có thể không đầy đủ hoặc chưa đúng với mong đợi.\n\nHình 5.1. Prompt trong AI tạo sinh</p>',
            '<p class="lesson-p">Prompt (yêu cầu) là nội dung mà người dùng nhập vào để hướng dẫn công cụ AI tạo ra kết quả theo mục tiêu đặt ra. Một prompt rõ ràng giúp hệ thống dễ hiểu và phản hồi chính xác hơn. Ngược lại, nếu prompt chung chung hoặc thiếu thông tin, kết quả có thể không đầy đủ hoặc chưa đúng với mong đợi.</p>',
        ),
        ("Prompt trong Al tạo sinh", "Prompt trong AI tạo sinh"),
        ("Sau khi nhóm Minh viết lai prompt", "Sau khi nhóm Minh viết lại prompt"),
        ("hệ thống Ai đã tạo ra kết quả", "hệ thống AI đã tạo ra kết quả"),
        (
            '<p class="lesson-p">Prompt là yêu cầu của người dùng nhập vào để công cụ AI tạo ra kết quả theo yêu cầu đó. Prompt càng rõ ràng.\n\nkết quả càng phù hợp với mục tiêu sử dụng.</p>',
            '<p class="lesson-p">Prompt là yêu cầu của người dùng nhập vào để công cụ AI tạo ra kết quả theo yêu cầu đó. Prompt càng rõ ràng, kết quả càng phù hợp với mục tiêu sử dụng.</p>',
        ),
        (
            '<p class="lesson-p">Một prompt được coi là rõ ràng nếu nó giúp AI hiểu đúng việc cần làm, chủ đề liên</p>\n'
            '<p class="lesson-p">quan và cách thể hiện phù hợp. Prompt càng rõ ràng thì kết quả mà AI tạo ra càng phù hợp với mục tiêu sử dụng.</p>',
            '<p class="lesson-p">Một prompt được coi là rõ ràng nếu nó giúp AI hiểu đúng việc cần làm, chủ đề liên quan và cách thể hiện phù hợp. Prompt càng rõ ràng thì kết quả mà AI tạo ra càng phù hợp với mục tiêu sử dụng.</p>',
        ),
        (
            '<p class="lesson-p">Một prompt rõ ràng thường gồm hai phần chỉnh. Phần đầu là chỉ thị, thể hiện hành động mà người dùng muốn ON H AI thực hiện, ví dụ: viết đoạn văn, tạo hình ảnh hoặc lập bảng. Phần thứ hai là dữ liệu đầu vào, thể hiện nội dung</p>\n'
            '<p class="lesson-p">cụ thể mà người dùng muốn AI xử lí. Ngoài hai phần này, người dùng có thể bổ sung</p>\n'
            '<p class="lesson-p">thêm thông tin như ví dụ minh hoạ, ngữ cảnh sử dụng hoặc định dạng mong muốn để kết quả chính xác và phủ</p>',
            '<p class="lesson-p">Một prompt rõ ràng thường gồm hai phần chính. Phần đầu là chỉ thị, thể hiện hành động mà người dùng muốn AI thực hiện, ví dụ: viết đoạn văn, tạo hình ảnh hoặc lập bảng. Phần thứ hai là dữ liệu đầu vào, thể hiện nội dung cụ thể mà người dùng muốn AI xử lí. Ngoài hai phần này, người dùng có thể bổ sung thêm thông tin như ví dụ minh hoạ, ngữ cảnh sử dụng hoặc định dạng mong muốn để kết quả chính xác và phù hợp hơn.</p>',
        ),
        (
            '<p class="lesson-p">Ở prompt thứ hai trong phần Khởi động, chỉ thị Tạo hình ảnh" thể hiện hành động mà nhóm bạn Minh muốn AI thực hiện. Dữ liệu đầu vào là "công chúa Việt Nam</p>\n'
            '<p class="lesson-p">mặc áo dài truyền thống. đứng trong khu vườn cung đình xưa", cho biết nội dung chính mà AI cần thể hiện. Cuối cùng, thông tin bổ sung "phong cách minh hoạ sách thiều nhi, màu sắc tươi sáng" giúp định hướng phong cách thể hiện của hình ảnh. Nhờ có đầy đủ các thành phần này, prompt trở nên rõ ràng hơn và giúp AI tạo ra kết quả phù hợp với mong muốn.</p>',
            '<p class="lesson-p">Ở prompt thứ hai trong phần Khởi động, chỉ thị "Tạo hình ảnh" thể hiện hành động mà nhóm bạn Minh muốn AI thực hiện. Dữ liệu đầu vào là "công chúa Việt Nam mặc áo dài truyền thống, đứng trong khu vườn cung đình xưa", cho biết nội dung chính mà AI cần thể hiện. Cuối cùng, thông tin bổ sung "phong cách minh hoạ sách thiếu nhi, màu sắc tươi sáng" giúp định hướng phong cách thể hiện của hình ảnh. Nhờ có đầy đủ các thành phần này, prompt trở nên rõ ràng hơn và giúp AI tạo ra kết quả phù hợp với mong muốn.</p>',
        ),
        (
            "ba phần chính: chí thị (nêu việc cần làm), dữ liệu đầu vào (nội dung cụ thể mà AI cần xừ II) và thông tin bổ sung (các yêu cầu thêm về bối cảnh, cách thế hiện hoặc định dạng).",
            "ba phần chính: chỉ thị (nêu việc cần làm), dữ liệu đầu vào (nội dung cụ thể mà AI cần xử lí) và thông tin bổ sung (các yêu cầu thêm về bối cảnh, cách thể hiện hoặc định dạng).",
        ),
        (
            '<p class="lesson-p">Lớp em sắp tổ chức một buổi sinh hoạt chuyên đề với chủ đề "Ứng xử văn minh trên mạng xã hội". Em muốn sử dụng Ai để viết một email gửi đến cô Trần Khánh Linh - giáo viên Ngừ văn đang giảng dạy lớp - để mời cô đến tham dự và chia sẻ cùng lớp một vài câu chuyện thực tế, kinh nghiệm hoặc lời khuyên. Em mong</p>\n'
            '<p class="lesson-p">muốn email thể hiện sự trân trọng, nhắc lại một ấn tượng đáng nhớ trong giờ học và thông báo thời gian, địa điểm của buổi sinh hoạt.</p>',
            '<p class="lesson-p">Lớp em sắp tổ chức một buổi sinh hoạt chuyên đề với chủ đề "Ứng xử văn minh trên mạng xã hội". Em muốn sử dụng AI để viết một email gửi đến cô Trần Khánh Linh – giáo viên Ngữ văn đang giảng dạy lớp – để mời cô đến tham dự và chia sẻ cùng lớp một vài câu chuyện thực tế, kinh nghiệm hoặc lời khuyên. Em mong muốn email thể hiện sự trân trọng, nhắc lại một ấn tượng đáng nhớ trong giờ học và thông báo thời gian, địa điểm của buổi sinh hoạt.</p>',
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Chỉ thị: Viết email mời.</li>
<li>Dữ liệu đầu vào: Gửi cho cô Trần Khánh Linh - giáo viên Ngữ văn đang giảng</li>
</ul>
<p class="lesson-p">dạy lớp.</p>
<ul class="lesson-bullet-list">
<li>Thông tin bổ sung: Buổi sinh hoạt chuyên đề về "Ứng xử văn minh trên mạng xã</li>
</ul>
<p class="lesson-p">hội"; thể hiện sự trân trọng; nhắc đến một ấn tượng trong giờ học; nêu rõ thời gian và địa điểm; giọng văn trang trọng, ấm áp.</p>""",
            """<ul class="lesson-bullet-list">
<li>Chỉ thị: Viết email mời.</li>
<li>Dữ liệu đầu vào: Gửi cho cô Trần Khánh Linh – giáo viên Ngữ văn đang giảng dạy lớp.</li>
<li>Thông tin bổ sung: Buổi sinh hoạt chuyên đề về "Ứng xử văn minh trên mạng xã hội"; thể hiện sự trân trọng; nhắc đến một ấn tượng trong giờ học; nêu rõ thời gian và địa điểm; giọng văn trang trọng, ấm áp.</li>
</ul>""",
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Xác định vai trò của AI và định dạng mong muốn: Viết một email mời. Email cần</li>
</ul>
<p class="lesson-p">có cấu trúc gồm lời chào, nội dung chính và lời kết.</p>
<ul class="lesson-bullet-list">
<li>Nêu rõ người nhận và mục đích của email: Người nhận là cô Trần Khánh Linh</li>
<li>giáo viên Ngữ văn đang giảng dạy lớp. Mục đích là mời cô tham dự buổi sinh hoạt chuyên đề về "Ứng xử văn minh trên mạng xã hội".</li>
<li>Bổ sung thông tin chi tiết:</li>
</ul>""",
            """<ul class="lesson-bullet-list">
<li>Xác định vai trò của AI và định dạng mong muốn: Viết một email mời. Email cần có cấu trúc gồm lời chào, nội dung chính và lời kết.</li>
<li>Nêu rõ người nhận và mục đích của email: Người nhận là cô Trần Khánh Linh – giáo viên Ngữ văn đang giảng dạy lớp. Mục đích là mời cô tham dự buổi sinh hoạt chuyên đề về "Ứng xử văn minh trên mạng xã hội".</li>
<li>Bổ sung thông tin chi tiết:</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">+ Trong email, cần thể hiện sự biết ơn chân thành, lòng ghép một kỉ niệm đáng</p>\n'
            '<p class="lesson-p">nhớ. Ví dụ: "Em vẫn nhớ bài học hôm cô giảng về ngôn ngũ giao tiếp trên</p>\n'
            '<p class="lesson-p">mạng, cô đã nhân mạnh tầm quan trọng của sự tử tế qua từng lới nói."</p>\n'
            '<p class="lesson-p">+ Buổi sinh hoạt diễn ra lúc 14h00, thứ Sáu ngày 24/10/2025, tại phòng học</p>\n'
            '<p class="lesson-p">lớp 10A2. Giọng văn trang trọng, gần gũi. Kết thư có lời mời cô xác nhận</p>',
            '<p class="lesson-p">+ Trong email, cần thể hiện sự biết ơn chân thành, lồng ghép một kỉ niệm đáng nhớ. Ví dụ: "Em vẫn nhớ bài học hôm cô giảng về ngôn ngữ giao tiếp trên mạng, cô đã nhấn mạnh tầm quan trọng của sự tử tế qua từng lời nói."</p>\n'
            '<p class="lesson-p">+ Buổi sinh hoạt diễn ra lúc 14h00, thứ Sáu ngày 24/10/2025, tại phòng học lớp 10A2. Giọng văn trang trọng, gần gũi. Kết thư có lời mời cô xác nhận tham dự.</p>',
        ),
        (
            """<p class="lesson-p">Ví dụ: Viết một email mời. Email cần có lời chào, nội dung chinh và lời kết.</p>
<p class="lesson-p">Người nhận là cô Trần Khánh Linh - giáo viên Ngữ văn đang giảng day lớp.

Mục đích là mời cô tham dự buổi sinh hoạt chuyên đề "Ứng xử văn minh trên mạng xã hội". Trong nội dung, thể hiện sự trân trọng đối với những bài giảng và sự đồng hành của cô trong suốt quá trình học tập, đồng thời thể hiện mong</p>
<p class="lesson-p">muồn cô hiện diện chia sẻ với lớp những kinh nghiệm, câu chuyện thực tế hoặc lời khuyên ý nghĩa. Lồng ghép kì niệm: "Em vẫn nhớ bài học hôm cô giảng về ngôn ngữ giao tiếp trên mạng, cô đã nhấn mạnh tầm quan trong của sự từ tế</p>
<p class="lesson-p">qua từng lời nói.". Buổi sinh hoạt diễn ra lúc 14h00, thứ Sáu ngày 24/10/2025, tại phòng học lớp 10A2. Giọng văn trang trọng, ấm áp. Kết thư có lời mời cô xác</p>""",
            '<p class="lesson-p">Ví dụ: Viết một email mời. Email cần có lời chào, nội dung chính và lời kết. Người nhận là cô Trần Khánh Linh – giáo viên Ngữ văn đang giảng dạy lớp. Mục đích là mời cô tham dự buổi sinh hoạt chuyên đề "Ứng xử văn minh trên mạng xã hội". Trong nội dung, thể hiện sự trân trọng đối với những bài giảng và sự đồng hành của cô trong suốt quá trình học tập, đồng thời thể hiện mong muốn cô hiện diện chia sẻ với lớp những kinh nghiệm, câu chuyện thực tế hoặc lời khuyên ý nghĩa. Lồng ghép kỉ niệm: "Em vẫn nhớ bài học hôm cô giảng về ngôn ngữ giao tiếp trên mạng, cô đã nhấn mạnh tầm quan trọng của sự tử tế qua từng lời nói.". Buổi sinh hoạt diễn ra lúc 14h00, thứ Sáu ngày 24/10/2025, tại phòng học lớp 10A2. Giọng văn trang trọng, ấm áp. Kết thư có lời mời cô xác nhận tham dự.</p>',
        ),
        ("ChatGPT, Gemini....", "ChatGPT, Gemini,..."),
        ("Nhiệm vụ 2: Viết prompt đề tạo hình ảnh", "Nhiệm vụ 2: Viết prompt để tạo hình ảnh"),
        (
            """<ul class="lesson-bullet-list">
<li>Chỉ thị: Tạo hình ảnh minh hoạ cho áp phích truyền thông</li>
<li>Dữ liệu đầu vào: Cuộc thi truyền thông với chủ đề "Cân bằng giữa học tập và</li>
</ul>
<p class="lesson-p">đam mê cá nhân".</p>

<ul class="lesson-bullet-list">
<li>Thông tin bổ sung: Hình ảnh có hai học sinh Trung học phổ thông đang tranh</li>
</ul>
<p class="lesson-p">biện hoặc trò chuyên, có biểu tượng micro, sách và, nền lớp học, phong cách minh hoạ hiện đại, màu sắc nỗi bật, ánh sáng tươi sáng, bố cục cản đối.</p>""",
            """<ul class="lesson-bullet-list">
<li>Chỉ thị: Tạo hình ảnh minh hoạ cho áp phích truyền thông.</li>
<li>Dữ liệu đầu vào: Cuộc thi truyền thông với chủ đề "Cân bằng giữa học tập và đam mê cá nhân".</li>
<li>Thông tin bổ sung: Hình ảnh có hai học sinh Trung học phổ thông đang tranh biện hoặc trò chuyện, có biểu tượng micro, sách vở, nền lớp học, phong cách minh hoạ hiện đại, màu sắc nổi bật, ánh sáng tươi sáng, bố cục cân đối.</li>
</ul>""",
        ),
        ("Bước 2. Xày dựng prompt từng phần.", "Bước 2. Xây dựng prompt từng phần."),
        (
            '<p class="lesson-p">+ Em cần yêu cầu AI tạo ra một hình ảnh minh hoa sinh động, có thể sử dụng</p>\n'
            '<p class="lesson-p">làm trung tâm cho áp phích truyền thông của lớp.</p>\n'
            '<p class="lesson-p">+ Ví dụ prompt: Tạo hình ảnh minh hoa sinh động cho áp phích tuyên truyền</p>\n'
            '<p class="lesson-p">học đường</p>',
            '<p class="lesson-p">+ Em cần yêu cầu AI tạo ra một hình ảnh minh hoạ sinh động, có thể sử dụng làm trung tâm cho áp phích truyền thông của lớp.</p>\n'
            '<p class="lesson-p">+ Ví dụ prompt: Tạo hình ảnh minh hoạ sinh động cho áp phích tuyên truyền học đường.</p>',
        ),
        (
            '<p class="lesson-p">+ Em cần mô tả rõ chủ đề của cuộc thi và bồi cảnh của hình ảnh để AI hiểu</p>\n'
            '<p class="lesson-p">đúng ý tưởng.</p>\n'
            '<p class="lesson-p">+ Ví dụ prompt: Chủ đề là "Cân bằng giữa học tập và đạm mề cả nhân". Trong</p>\n'
            '<p class="lesson-p">ảnh có hai học sinh Trung học phổ thông - một bạn cầm sách, một bạn đang chơi đàn guitar, đứng đối diện nhau như đang chia sẻ góc nhin trong một buổi tranh biện.</p>',
            '<p class="lesson-p">+ Em cần mô tả rõ chủ đề của cuộc thi và bối cảnh của hình ảnh để AI hiểu đúng ý tưởng.</p>\n'
            '<p class="lesson-p">+ Ví dụ prompt: Chủ đề là "Cân bằng giữa học tập và đam mê cá nhân". Trong ảnh có hai học sinh Trung học phổ thông – một bạn cầm sách, một bạn đang chơi đàn guitar, đứng đối diện nhau như đang chia sẻ góc nhìn trong một buổi tranh biện.</p>',
        ),
        (
            '<p class="lesson-p">+ Hình ảnh nên có biểu tượng liên quan đến học tập (sách, bút,...), đam mê</p>\n'
            '                    \n<p class="lesson-p">cá nhân (đàn guitar, tranh vê...), phong cách hiện đại, màu sắc hài hoà,...\n\nphù hợp với học sinh Trung học phổ thông.</p>',
            '<p class="lesson-p">+ Hình ảnh nên có biểu tượng liên quan đến học tập (sách, bút,...), đam mê cá nhân (đàn guitar, tranh vẽ,...), phong cách hiện đại, màu sắc hài hoà,... phù hợp với học sinh Trung học phổ thông.</p>',
        ),
        (
            "Phong cách minh hoa hiện đại, màu sắc nồi bật, ánh sáng tươi sáng.",
            "Phong cách minh hoạ hiện đại, màu sắc nổi bật, ánh sáng tươi sáng.",
        ),
        ("Bước 4. Sử dụng prompt đề tạo kết quả.", "Bước 4. Sử dụng prompt để tạo kết quả."),
        (
            """<ul class="lesson-bullet-list">
<li>Truy cập vào công cụ AI tạo hình ảnh như https://designer.microsoft.com/</li>
</ul>
<p class="lesson-p">image-creator hoặc https://www.bing.com/images/create,...</p>
<ul class="lesson-bullet-list">
<li>Nhập prompt đã viết đầy đủ ở Bước 3. Lưu lại hình ảnh do hệ thống tạo ra.</li>
</ul>""",
            """<ul class="lesson-bullet-list">
<li>Truy cập vào công cụ AI tạo hình ảnh như https://designer.microsoft.com/image-creator hoặc https://www.bing.com/images/create,...</li>
<li>Nhập prompt đã viết đầy đủ ở Bước 3. Lưu lại hình ảnh do hệ thống tạo ra.</li>
</ul>""",
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Nếu hình ảnh chưa đạt yêu cầu, em có thể chỉnh sửa prompt bằng cách thay</li>
</ul>
<p class="lesson-p">đổi chi tiết (thêm biểu tượng, điều chỉnh số lượng học sinh, đổi góc chụp,....) hoặc phong cách (vẽ tay, hoạt hình, tranh cổ động, tranh bìa sách,....).</p>""",
            """<ul class="lesson-bullet-list">
<li>Nếu hình ảnh chưa đạt yêu cầu, em có thể chỉnh sửa prompt bằng cách thay đổi chi tiết (thêm biểu tượng, điều chỉnh số lượng học sinh, đổi góc chụp,...) hoặc phong cách (vẽ tay, hoạt hình, tranh cổ động, tranh bìa sách,...).</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">Ví dự: Tạo hình ảnh minh hoạ cho áp phích truyền thông học sinh Trung học phổ thông về chủ đề "Cân bằng giữa học tập và đam mẻ cá nhân". Một học sinh nam đang đọc sách, một học sinh nữ đang vẽ tranh. Cả hai ngồi đối diện nhau trong thư viện trường. Cỏ ánh sáng từ cửa số, sách được xếp ngăn nắp, bảng</p>\n'
            '<p class="lesson-p">đen phía sau có dòng chữ khầu hiệu. Phong cách minh hoạ kiều tranh bia sách, màu sắc sinh động, cảm xúc tích cực.</p>',
            '<p class="lesson-p">Ví dụ: Tạo hình ảnh minh hoạ cho áp phích truyền thông học sinh Trung học phổ thông về chủ đề "Cân bằng giữa học tập và đam mê cá nhân". Một học sinh nam đang đọc sách, một học sinh nữ đang vẽ tranh. Cả hai ngồi đối diện nhau trong thư viện trường. Có ánh sáng từ cửa sổ, sách được xếp ngăn nắp, bảng đen phía sau có dòng chữ khẩu hiệu. Phong cách minh hoạ kiểu tranh bìa sách, màu sắc sinh động, cảm xúc tích cực.</p>',
        ),
        (
            '<p class="lesson-p">Em hãy thực hành viết các prompt khác nhau đề quan sát sự thay đổi kết quả mà công cụ AI tạo ra với chủ đề: "Mô tả buổi sáng ở nông thôn Việt Nam.".\n\nHướng dẫn:</p>',
            '<p class="lesson-p">Em hãy thực hành viết các prompt khác nhau để quan sát sự thay đổi kết quả mà công cụ AI tạo ra với chủ đề: "Mô tả buổi sáng ở nông thôn Việt Nam.".</p>\n<p class="lesson-p">Hướng dẫn:</p>',
        ),
        (
            '<p class="lesson-p">Ví dụ prompt: Mô tả một buổi sáng ở nông thôn Việt Nam</p>\n'
            '<p class="lesson-p">Bước 2. Theo dõi kết quả với một prompt cụ thể hơn</p>\n'
            '<p class="lesson-p">Ví dụ prompt: Hãy viết một đoạn văn ngắn mô tả một buổi sáng yên binh ở vùng</p>\n'
            '<p class="lesson-p">nông thôn Việt Nam, tập trung vào ảm thanh và mùi hương</p>\n'
            '<p class="lesson-p">Bước 3. Thay đổi đối tượng và mục tiêu sử dụng</p>',
            '<p class="lesson-p">Ví dụ prompt: Mô tả một buổi sáng ở nông thôn Việt Nam.</p>\n'
            '<p class="lesson-p">Bước 2. Theo dõi kết quả với một prompt cụ thể hơn.</p>\n'
            '<p class="lesson-p">Ví dụ prompt: Hãy viết một đoạn văn ngắn mô tả một buổi sáng yên bình ở vùng nông thôn Việt Nam, tập trung vào âm thanh và mùi hương.</p>\n'
            '<p class="lesson-p">Bước 3. Thay đổi đối tượng và mục tiêu sử dụng.</p>',
        ),
        ("giới thiệu ngắn về buổi sảng ở nông thôn Việt Nam", "giới thiệu ngắn về buổi sáng ở nông thôn Việt Nam"),
        (
            "Viết một đoạn thơ gồm bồn câu để miêu tả vè đẹp thanh bình của buổi sáng ở một làng qué Việt Nam.",
            "Viết một đoạn thơ gồm bốn câu để miêu tả vẻ đẹp thanh bình của buổi sáng ở một làng quê Việt Nam.",
        ),
        (
            '<p class="lesson-p">Gợi ý trao đổi:\n\nSau mỗi bước, em có thể trao đổi với bạn để so sánh kết quả và thảo luận xem phần nào trong prompt đã làm thay đổi kết quả đầu ra.</p>',
            '<p class="lesson-p">Gợi ý trao đổi:</p>\n<p class="lesson-p">Sau mỗi bước, em có thể trao đổi với bạn để so sánh kết quả và thảo luận xem phần nào trong prompt đã làm thay đổi kết quả đầu ra.</p>',
        ),
        (
            '<p class="lesson-p">LUYÊN TẬP</p>',
            '</div></section>' + section_open("exercise-section", "sec-luyện-tập", "✏️", "LUYỆN TẬP"),
        ),
        (
            '<p class="lesson-p">Nhóm bạn Mai và nhóm bạn An đang chuẩn bị bài thuyết trình về cùng chủ đề "Ước mơ nghề nghiệp". Mỗi nhóm muốn tạo một hình minh hoa bằng công cụ AI.\n\n'
            'Nhóm bạn Mai nhập prompt: "Vẽ một hình ảnh về nghề bác sĩ.". Nhóm bạn An nhập prompt: Tạo hình ảnh minh hoa cho một bác sĩ đang khám bệnh tại bệnh viện, mặc áo blouse trắng, đeo khẩu trang, có bệnh nhân ngồi phía trước theo phong cách vẽ tranh mình hoa sách giáo khoa."</p>',
            '<p class="lesson-p">Nhóm bạn Mai và nhóm bạn An đang chuẩn bị bài thuyết trình về cùng chủ đề "Ước mơ nghề nghiệp". Mỗi nhóm muốn tạo một hình minh hoạ bằng công cụ AI.</p>\n'
            '<p class="lesson-p">Nhóm bạn Mai nhập prompt: "Vẽ một hình ảnh về nghề bác sĩ.". Nhóm bạn An nhập prompt: "Tạo hình ảnh minh hoạ cho một bác sĩ đang khám bệnh tại bệnh viện, mặc áo blouse trắng, đeo khẩu trang, có bệnh nhân ngồi phía trước theo phong cách vẽ tranh minh hoạ sách giáo khoa."</p>',
        ),
        ('<p class="lesson-p">C</p>\n', ""),
        (
            '<p class="lesson-p">C. Vì prompt của nhóm bạn An nâu rõ nội dung, bối cảnh và chi tiết cần có hơn</p>\n'
            '<p class="lesson-p">prompt của nhóm bạn Mai.</p>',
            '<p class="lesson-p">C. Vì prompt của nhóm bạn An nêu rõ nội dung, bối cảnh và chi tiết cần có hơn prompt của nhóm bạn Mai.</p>',
        ),
        (
            """<p class="lesson-p">Thành phần Nội dung tương ứng cua prompt</p>
<h3 class="subheading-h3"><span class="h3-num">1.</span> Chỉ thị</h3>
<p class="lesson-p">A. Tạo hình ảnh minh hoạ.</p>
<h3 class="subheading-h3"><span class="h3-num">2.</span> Dữ liệu đầu vào</h3>
<p class="lesson-p">B. Một bác sĩ đang khám bệnh tại bệnh viện, mặc áo blouse trắng, đeo khẩu trang, có bệnh nhân ngồi phía trước.</p>
<h3 class="subheading-h3"><span class="h3-num">3.</span> Thông tin bổ sung</h3>
<p class="lesson-p">C. Theo phong cách vẽ tranh minh hoa sách giáo khoa.</p>
<p class="lesson-p">1. Em hãy viết một prompt rõ ràng để công cụ AI tạo sinh có thể thực hiện chính xác mỗi công việc sau đây, sau đó, nhập prompt này vào một công cụ AI mà em biết (nếu có điều kiện) và chia sẻ kết quả với bạn cùng nhóm.</p>""",
            """<p class="lesson-p"><strong>Thành phần của prompt — Nội dung tương ứng:</strong></p>
<ul class="lesson-bullet-list">
<li>1. Chỉ thị — A. Tạo hình ảnh minh hoạ.</li>
<li>2. Dữ liệu đầu vào — B. Một bác sĩ đang khám bệnh tại bệnh viện, mặc áo blouse trắng, đeo khẩu trang, có bệnh nhân ngồi phía trước.</li>
<li>3. Thông tin bổ sung — C. Theo phong cách vẽ tranh minh hoạ sách giáo khoa.</li>
</ul>
</div></section>"""
            + section_open("apply-section", "sec-vận-dụng", "🚀", "VẬN DỤNG")
            + '<p class="lesson-p">1. Em hãy viết một prompt rõ ràng để công cụ AI tạo sinh có thể thực hiện chính xác mỗi công việc sau đây, sau đó, nhập prompt này vào một công cụ AI mà em biết (nếu có điều kiện) và chia sẻ kết quả với bạn cùng nhóm.</p>',
        ),
        (
            '<p class="lesson-p">2. Một bạn viết prompt: "Tạo hình ảnh minh hoạ về việc bảo vệ môi trường.".\n\nKết quả AI tạo ra chưa sát với ý tưởng của bạn, hình ảnh còn chung chung và thiếu nội dung cụ thể.</p>',
            '<p class="lesson-p">2. Một bạn viết prompt: "Tạo hình ảnh minh hoạ về việc bảo vệ môi trường."</p>\n<p class="lesson-p">Kết quả AI tạo ra chưa sát với ý tưởng của bạn, hình ảnh còn chung chung và thiếu nội dung cụ thể.</p>',
        ),
        ('<p class="lesson-p">ALi</p>\n', ""),
    ],
    "bai-6-ai-tao-sinh-ho-tro-hoc-tap": [
        ('<p class="lesson-p">BÀI 6: AI TẠO SINH HỖ TRỢ</p>\n<p class="lesson-p">HỌC TẬP</p>\n', ""),
        (
            "không sao chép nguyên văn kết quả từ AI tạo sinh.\n\nVẠN DỤNG</li>",
            "không sao chép nguyên văn kết quả từ AI tạo sinh.</li>",
        ),
        (
            'sử dụng AI tạo sinh để tim thêm tư liệu và hình ảnh minh hoạ. Nhóm bạn Minh kiểm tra, chọn lọc thông tin từ kết quả của AI tạo sinh, diễn đạt nội dung theo văn phong của mình và luyện tập trình bày rõ ràng. Trong khi đó, nhóm bạn Long sao chép toàn bộ nội dung được tạo ra từ AI</p>\n'
            '<p class="lesson-p">mà không đọc lại hay kiểm tra.</p>',
            'sử dụng AI tạo sinh để tìm thêm tư liệu và hình ảnh minh hoạ. Nhóm bạn Minh kiểm tra, chọn lọc thông tin từ kết quả của AI tạo sinh, diễn đạt nội dung theo văn phong của mình và luyện tập trình bày rõ ràng. Trong khi đó, nhóm bạn Long sao chép toàn bộ nội dung được tạo ra từ AI mà không đọc lại hay kiểm tra.</p>',
        ),
        ("phần trình bảy của nhóm bạn Minh", "phần trình bày của nhóm bạn Minh"),
        ("lúng túng vì không hiếu hết nội dung", "lúng túng vì không hiểu hết nội dung"),
        ('<span class="h3-num">1.</span> Ai tạo sinh có thể hỗ trợ học tập</h3>', '<span class="h3-num">1.</span> AI tạo sinh có thể hỗ trợ học tập</h3>'),
        (
            '<p class="lesson-p">Trong tỉnh huống Khởi động, nhóm bạn Minh đã sử dụng Ai tạo sinh để tim them tư liệu và hình ảnh minh hoa cho bài thuyết trình môn Lịch sử. Nhờ biết cách kiêm tra, chọn lọc và trình bày lại nội dung, các bạn đã làm bài tốt và được giáo viên khen ngợi. Điều này cho thấy, nếu sử dụng đúng cách thì Ai tạo sinh có thể giúp em học tập hiệu quả</p>',
            '<p class="lesson-p">Trong tình huống Khởi động, nhóm bạn Minh đã sử dụng AI tạo sinh để tìm thêm tư liệu và hình ảnh minh hoạ cho bài thuyết trình môn Lịch sử. Nhờ biết cách kiểm tra, chọn lọc và trình bày lại nội dung, các bạn đã làm bài tốt và được giáo viên khen ngợi. Điều này cho thấy, nếu sử dụng đúng cách thì AI tạo sinh có thể giúp em học tập hiệu quả.</p>',
        ),
        ('<p class="lesson-p">ABC</p>\n', ""),
        ("Hình 6.1. Al tạo sinh có thể hỗ trợ học tập", "Hình 6.1. AI tạo sinh có thể hỗ trợ học tập"),
        ("<strong>Hình 6.1.</strong> Al tạo sinh có thể hỗ trợ học tập", "<strong>Hình 6.1.</strong> AI tạo sinh có thể hỗ trợ học tập"),
        (
            '<p class="lesson-p">Ai tạo sinh có thể hỗ try em ở nhiều môn học khác nhau. Khi học Ngữ văn, em có thể dùng Ai để gọi ý cách lập dàn ý hoặc luyện viết đoạn vẫn. Trong môn Toán, em có thể nhờ AI gọi ý các bước giải bài tập dạng mẫu để tham khảo. Với môn Tiếng Anh, em có thể luyện viết câu, sửa lỏi ngữ pháp hoặc mở rộng tử vựng. Khi học Lịch sử hay Địa lí, ern có thể yêu cầu AI tóm tắt nội dung bài học, giải thích sự kiện</p>\n'
            '<p class="lesson-p">hoặc mô tả hiện tượng. Tuy nhiên, với bất kì môn học nào, em chỉ nên sử dụng Ai tạo sinh với vải tro hồ trọ. Chính em là người cần hiểu, ghi nhớ và trình bày lại</p>\n'
            '<p class="lesson-p">kiến thức theo cách hiếu của minh.</p>',
            '<p class="lesson-p">AI tạo sinh có thể hỗ trợ em ở nhiều môn học khác nhau. Khi học Ngữ văn, em có thể dùng AI để gợi ý cách lập dàn ý hoặc luyện viết đoạn văn. Trong môn Toán, em có thể nhờ AI gợi ý các bước giải bài tập dạng mẫu để tham khảo. Với môn Tiếng Anh, em có thể luyện viết câu, sửa lỗi ngữ pháp hoặc mở rộng từ vựng. Khi học Lịch sử hay Địa lí, em có thể yêu cầu AI tóm tắt nội dung bài học, giải thích sự kiện hoặc mô tả hiện tượng. Tuy nhiên, với bất kì môn học nào, em chỉ nên sử dụng AI tạo sinh với vai trò hỗ trợ. Chính em là người cần hiểu, ghi nhớ và trình bày lại kiến thức theo cách hiểu của mình.</p>',
        ),
        (
            "bằng cách gọi ý, giải thích hoặc minh hoạ. Tuy nhiên, em cần chủ động tiếp thu và trình bảy lại",
            "bằng cách gợi ý, giải thích hoặc minh hoạ. Tuy nhiên, em cần chủ động tiếp thu và trình bày lại",
        ),
        ("Cách sử dụng AI tạo sinh hiệu quả trong học lập</h3>", "Cách sử dụng AI tạo sinh hiệu quả trong học tập</h3>"),
        (
            '<p class="lesson-p">Ngoài việc tim thông tin, AI còn có thể hỏ ty em trong việc lập kể hoạch học tập chuẩn bị bài, luyện lập theo chú đề hoặc mở rộng kĩ năng khi cần thiết</p>',
            '<p class="lesson-p">Ngoài việc tìm thông tin, AI còn có thể hỗ trợ em trong việc lập kế hoạch học tập, chuẩn bị bài, luyện tập theo chủ đề hoặc mở rộng kĩ năng khi cần thiết.</p>',
        ),
        ("AI có thể hỗ trợ ern xây dựng", "AI có thể hỗ trợ em xây dựng"),
        (
            'ôn tập món Toán bằng cách nhập prompt "Lập kể hoạch ôn tập 7 ngày, mỗi ngày 2 tiêng,',
            'ôn tập môn Toán bằng cách nhập prompt "Lập kế hoạch ôn tập 7 ngày, mỗi ngày 2 tiếng,',
        ),
        (
            '<p class="lesson-p">Việc sử dụng AI như một người bạn học giúp em chủ động hơn trong việc chuẩn</p>',
            '<p class="lesson-p">Việc sử dụng AI như một người bạn học giúp em chủ động hơn trong việc chuẩn bị bài.</p>',
        ),
        (
            '<p class="lesson-p">Ví dụ: Bạn Hoa dùng Ai để tóm tắt bài Sinh học và giái thích các khái niệm khó.\n\nTrước giờ học, Hoa ghi chép lại theo cách hiếu của mình. Trong giờ học, Hoa đã chủ động hỏi giáo viên những nội dung chưa hiểu để được giải đáp</p>',
            '<p class="lesson-p">Ví dụ: Bạn Hoa dùng AI để tóm tắt bài Sinh học và giải thích các khái niệm khó. Trước giờ học, Hoa ghi chép lại theo cách hiểu của mình. Trong giờ học, Hoa đã chủ động hỏi giáo viên những nội dung chưa hiểu để được giải đáp.</p>',
        ),
        (
            '<p class="lesson-p">Ví dụ: Bạn Nam làm xong bài tập Toán rồi nhập lời giải vào AI và nhờ nhận xét.</p>\n<p class="lesson-p">Sau khi phát hiện lỗi sai, Nam đã tự sửa lại và làm lại bài.</p>',
            '<p class="lesson-p">Ví dụ: Bạn Nam làm xong bài tập Toán rồi nhập lời giải vào AI và nhờ nhận xét. Sau khi phát hiện lỗi sai, Nam đã tự sửa lại và làm lại bài.</p>',
        ),
        (
            '<p class="lesson-p">d) Mở rộng kĩ năng Em có thể thử nghiệm các công cụ AI để năng cao năng lực và mở rộng kĩ năng cá nhân theo sở thích và mục tiêu học tập.\n\nVí dụ: Bạn Lan muốn học kĩ năng thuyết trình nên nhờ AI gợi ý các bước chuẩn bị và cách trình bày hiệu quả. Lan đã áp dụng khi làm bài thuyết trình nhóm trên lớp.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">d)</span> Mở rộng kĩ năng</h4>\n'
            '<p class="lesson-p">Em có thể thử nghiệm các công cụ AI để nâng cao năng lực và mở rộng kĩ năng cá nhân theo sở thích và mục tiêu học tập.</p>\n'
            '<p class="lesson-p">Ví dụ: Bạn Lan muốn học kĩ năng thuyết trình nên nhờ AI gợi ý các bước chuẩn bị và cách trình bày hiệu quả. Lan đã áp dụng khi làm bài thuyết trình nhóm trên lớp.</p>',
        ),
        (
            '<p class="lesson-p">Ai tạo sinh có thể hỗ trợ em từ việc lập kế hoạch học tập,</p>\n<p class="lesson-p">chuẩn bị bài, luyện lập, kiểm tra kết quả đến mở rộng kĩ năng.</p>',
            '<p class="lesson-p">AI tạo sinh có thể hỗ trợ em từ việc lập kế hoạch học tập, chuẩn bị bài, luyện tập, kiểm tra kết quả đến mở rộng kĩ năng.</p>',
        ),
        (
            'Tuy nhiên, em</p>\n<p class="lesson-p">cần có trách nhiệm và ý thức rõ ràng để sử dụng công cụ này đúng mục đích và trung thực trong học lập</p>',
            'Tuy nhiên, em cần có trách nhiệm và ý thức rõ ràng để sử dụng công cụ này đúng mục đích và trung thực trong học tập.</p>',
        ),
        ('<p class="lesson-p">Al</p>\n', ""),
        ("Trách nhiệm của học sinh khi sử dụng Al tạo sinh", "Trách nhiệm của học sinh khi sử dụng AI tạo sinh"),
        ("thể hiện được quan điểm cá nhân:</p>", "thể hiện được quan điểm cá nhân.</p>"),
        (
            '<p class="lesson-p">Ví dụ: Bạn Hưng dùng AI đề tham khảo khi viết đoạn văn nghị luân. Sau khi đọc gợi ý. Hưng viết lại bằng cách chọn lọc ý chính và diễn đạt theo văn phong riêng.\n\nđồng thời ghi chú: "Có tham khảo ý tưởng từ công cụ AI.".</p>',
            '<p class="lesson-p">Ví dụ: Bạn Hưng dùng AI để tham khảo khi viết đoạn văn nghị luận. Sau khi đọc gợi ý, Hưng viết lại bằng cách chọn lọc ý chính và diễn đạt theo văn phong riêng, đồng thời ghi chú: "Có tham khảo ý tưởng từ công cụ AI.".</p>',
        ),
        ('<span class="h4-letter">b)</span> Kiềm tra thông tin trước khi sử dụng</h4>', '<span class="h4-letter">b)</span> Kiểm tra thông tin trước khi sử dụng</h4>'),
        (
            "dùng AI để tìm hiếu về một hiện lượng thiên nhiên cho bài thuyết trình. Sau khi nhận được kết quả, Linh đã đối chiếu lại với sách giáo khoa và hồi thêm giáo viên",
            "dùng AI để tìm hiểu về một hiện tượng thiên nhiên cho bài thuyết trình. Sau khi nhận được kết quả, Linh đã đối chiếu lại với sách giáo khoa và hỏi thêm giáo viên",
        ),
        ("Cà nhóm đã ghi rõ trong slide:", "Cả nhóm đã ghi rõ trong slide:"),
        ("Em cần có thái độ tôn trong khi sử dụng", "Em cần có thái độ tôn trọng khi sử dụng"),
        ("minh hoạ cho bài thuyết trình Trang chọn lọc", "minh hoạ cho bài thuyết trình. Trang chọn lọc"),
        (
            '<p class="lesson-p">Khi sử dụng AI tạo sinh, em cần trung thực, kiểm chứng thông tin, trình bày lại theo cách hiểu của</p>\n<p class="lesson-p">mình và ghi rõ vai trò hỗ trợ của AI nếu cần.',
            '<p class="lesson-p">Khi sử dụng AI tạo sinh, em cần trung thực, kiểm chứng thông tin, trình bày lại theo cách hiểu của mình và ghi rõ vai trò hỗ trợ của AI nếu cần.',
        ),
        ('<span class="h3-num">4.</span> Thực hành: Sử dụng Ai hỗ trợ học tập</h3>', '<span class="h3-num">4.</span> Thực hành: Sử dụng AI hỗ trợ học tập</h3>'),
        (
            '<p class="lesson-p">Tuần tới lớp em sẽ có bài kiểm tra môn Tiếng Anh. Em muốn luyện tập và tự kiểm tra trước đề đánh giá khả năng của mình. Để thực hiện, em sử dụng một công cụ AI tạo sinh để tạo ra bộ câu hỏi trắc nghiệm và tự luận ngắn, sau đó làm bài, đối chiếu kết quả và phần biên lại với AI đề hiểu sâu hơn. Em hãy sử dụng công cụ</p>\n'
            '<p class="lesson-p">AI tạo sinh để tạo ra bộ câu hỏi luyện tập phù hợp với nội dung Tiếng Anh lớp 10 (ví dụ: thì hiện tại hoàn thành, thì quá khứ đơn). Em làm thử trong 15 phút, sau đỏ nếu còn thời gian thì làm thêm các câu hỏi khác. Sau khi làm xong, em đối chiếu kết quả với AI, nêu thắc mắc hoặc phản biện khi chưa đồng ý với lời giải.</p>\n'
            '<p class="lesson-p">C</p>',
            '<p class="lesson-p">Tuần tới lớp em sẽ có bài kiểm tra môn Tiếng Anh. Em muốn luyện tập và tự kiểm tra trước để đánh giá khả năng của mình. Để thực hiện, em sử dụng một công cụ AI tạo sinh để tạo ra bộ câu hỏi trắc nghiệm và tự luận ngắn, sau đó làm bài, đối chiếu kết quả và phản biện lại với AI để hiểu sâu hơn. Em hãy sử dụng công cụ AI tạo sinh để tạo ra bộ câu hỏi luyện tập phù hợp với nội dung Tiếng Anh lớp 10 (ví dụ: thì hiện tại hoàn thành, thì quá khứ đơn). Em làm thử trong 15 phút, sau đó nếu còn thời gian thì làm thêm các câu hỏi khác. Sau khi làm xong, em đối chiếu kết quả với AI, nêu thắc mắc hoặc phản biện khi chưa đồng ý với lời giải.</p>',
        ),
        (
            '<ul class="lesson-bullet-list">\n<li>Xem kết quả. Nếu thấy dễ, yêu cầu AI tăng độ khó (ví dụ: thêm bài đọc hiểu ngắn).</li>\n</ul>\n<p class="lesson-p">Nếu thấy khó, yêu cầu AI điều chỉnh.</p>',
            '<ul class="lesson-bullet-list">\n<li>Xem kết quả. Nếu thấy dễ, yêu cầu AI tăng độ khó (ví dụ: thêm bài đọc hiểu ngắn). Nếu thấy khó, yêu cầu AI điều chỉnh.</li>\n</ul>',
        ),
        (
            """<p class="lesson-p">+ Câu 1: She</p>
<p class="lesson-p">(never/see) a lion before.</p>
<p class="lesson-p">+ Câu 2: They</p>
<p class="lesson-p">. (go) to the cinema last night.</p>
<p class="lesson-p">+ Câu 3: 1</p>
<p class="lesson-p">(finish) my homework already.</p>""",
            """<p class="lesson-p">+ Câu 1: She ________ (never/see) a lion before.</p>
<p class="lesson-p">+ Câu 2: They ________ (go) to the cinema last night.</p>
<p class="lesson-p">+ Câu 3: I ________ (finish) my homework already.</p>""",
        ),
        ('<p class="lesson-p">→ Ihaven\'t...</p>', '<p class="lesson-p">→ I haven\'t ...</p>'),
        ("Bước 3. Đối chiếu, phần biện và tự đánh giá.", "Bước 3. Đối chiếu, phản biện và tự đánh giá."),
        (
            """<ul class="lesson-bullet-list">
<li>Sau khi hoàn thành, em nhập lại đáp án vào AI để nhận góp ý chi tiết.</li>
<li>Khi có câu sai, em cần hỏi ngược lại AI: "Tại sao chọn đáp án này mà không</li>
</ul>
<p class="lesson-p">phải đáp án kia?".</p>
<ul class="lesson-bullet-list">
<li>Em có thể so sánh cách giải thích của AI với sách giáo khoa hoặc ghi chú của</li>
</ul>
<p class="lesson-p">mình để kiểm chứng</p>""",
            """<ul class="lesson-bullet-list">
<li>Sau khi hoàn thành, em nhập lại đáp án vào AI để nhận góp ý chi tiết.</li>
<li>Khi có câu sai, em cần hỏi ngược lại AI: "Tại sao chọn đáp án này mà không phải đáp án kia?".</li>
<li>Em có thể so sánh cách giải thích của AI với sách giáo khoa hoặc ghi chú của mình để kiểm chứng.</li>
</ul>""",
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Em ghi lại số câu đúng, những lỗi sai và lí do.</li>
<li>Ví dụ ghi chú: "Em làm đúng 2/3 câu trắc nghiệm. Ở câu viết lại, AI cho đáp án</li>
</ul>
<p class="lesson-p">I haven't visited my grandparents for two years, em hỏi lại tại sao không dùng since two years ago và AI giải thích thêm về cách dùng since/for. Nhờ vậy em hiểu rõ hơn.".</p>
<ul class="lesson-bullet-list">
<li>Dựa vào nhận xét và phần phản biện, em điều chỉnh cách học, bổ sung kiến</li>
</ul>
<p class="lesson-p">thức và luyện thêm.</p>""",
            """<ul class="lesson-bullet-list">
<li>Em ghi lại số câu đúng, những lỗi sai và lí do.</li>
<li>Ví dụ ghi chú: "Em làm đúng 2/3 câu trắc nghiệm. Ở câu viết lại, AI cho đáp án I haven't visited my grandparents for two years, em hỏi lại tại sao không dùng since two years ago và AI giải thích thêm về cách dùng since/for. Nhờ vậy em hiểu rõ hơn.".</li>
<li>Dựa vào nhận xét và phần phản biện, em điều chỉnh cách học, bổ sung kiến thức và luyện thêm.</li>
</ul>""",
        ),
        ("C. Gợi ý cách viết bài, tóm tất nội dung", "C. Gợi ý cách viết bài, tóm tắt nội dung"),
        ("cho bài kiếm tra trên lớp.", "cho bài kiểm tra trên lớp."),
        ("A. Đặt yêu cầu căng ngắn càng tốt", "A. Đặt yêu cầu càng ngắn càng tốt"),
        ("D. Vị AI không hỗ trợ các môn học ở trường</p>", "D. Vì AI không hỗ trợ các môn học ở trường.</p>"),
        ("và mục tiêu học lập của bản thân.", "và mục tiêu học tập của bản thân."),
        (
            """<p class="lesson-p">A</p>
<p class="lesson-p">CHỦ ĐẾ 3. ĐẠO ĐỨC VÀ TRÁCH NHIỆM KHI SỬ DỤNG AI</p>
<p class="lesson-p">HM Vese I VGC</p>
<p class="lesson-p">AI Heinesicy</p>""",
            "",
        ),
    ],
    "bai-7-phan-biet-that-gia-trong-ai-tao-sinh": [
        ('<p class="lesson-p">TRONG ÁI TẠO SINH</p>\n', ""),
        (
            'một đoạn video gày chú ý, trong đó một người nổi tiếng phát biểu những lời khó nghe về người hàm mộ. Mai định chia sẻ ngay</p>\n'
            '<p class="lesson-p">đoạn video cho bạn bè cùng xem. Tuy nhiên, Hương (bạn thân của Mai) đã nhanh chóng lên liếng:',
            'một đoạn video gây chú ý, trong đó một người nổi tiếng phát biểu những lời khó nghe về người hâm mộ. Mai định chia sẻ ngay đoạn video cho bạn bè cùng xem. Tuy nhiên, Hương (bạn thân của Mai) đã nhanh chóng lên tiếng:',
        ),
        ("Trong tình huống Khởi đông,", "Trong tình huống Khởi động,"),
        ('<p class="lesson-p">Bịa đật Già mạo AI</p>\n', ""),
        ("Những rủi ro khi dùng Al tạo sinh", "Những rủi ro khi dùng AI tạo sinh"),
        ("một học sinh tim bài thuyết trình", "một học sinh tìm bài thuyết trình"),
        (
            '<p class="lesson-p">Vì vậy, khi sử dụng nội dung do AI tạo ra hoặc tiếp cận thông tin trên Internet, em</p>\n'
            '<p class="lesson-p">cần kiềm chứng qua các nguồn đàng tin cậy như sách giáo khoa, báo chí chính thống hoặc hỏi thầy có giáo.',
            '<p class="lesson-p">Vì vậy, khi sử dụng nội dung do AI tạo ra hoặc tiếp cận thông tin trên Internet, em cần kiểm chứng qua các nguồn đáng tin cậy như sách giáo khoa, báo chí chính thống hoặc hỏi thầy cô giáo.',
        ),
        (
            '<p class="lesson-p">AI tạo sinh có thể tạo ra nội dung bia đặt hoặc giả mạo.\n\nNếu không kiểm chứng,',
            '<p class="lesson-p">AI tạo sinh có thể tạo ra nội dung bịa đặt hoặc giả mạo.</p>\n<p class="lesson-p">Nếu không kiểm chứng,',
        ),
        ('<span class="h3-num">2.</span> Nhân biết thông tin và hình ảnh giả do AI tạo ra</h3>', '<span class="h3-num">2.</span> Nhận biết thông tin và hình ảnh giả do AI tạo ra</h3>'),
        (
            'chữ viết bị méo, khuôn mặt hơi cứng hoặc</p>\n<p class="lesson-p">chuyển động mắt không tự nhiên.',
            'chữ viết bị méo, khuôn mặt hơi cứng hoặc chuyển động mắt không tự nhiên.',
        ),
        (
            '<p class="lesson-p">Để nhận biết chính xác hơn, em nên kiểm tra các thông tin đi kèm như: tính chính</p>\n'
            '<p class="lesson-p">thống của nguồn tin và người đăng; nếu không phải là sự kiện thật, em sẽ không tim thấy thông tin xác nhận từ các kênh chính thức như trang web của trường học.\n\n'
            'cơ quan báo chí uy tín hoặc trang mạng xã hội đã được xác thực.</p>',
            '<p class="lesson-p">Để nhận biết chính xác hơn, em nên kiểm tra các thông tin đi kèm như: tính chính thống của nguồn tin và người đăng; nếu không phải là sự kiện thật, em sẽ không tìm thấy thông tin xác nhận từ các kênh chính thức như trang web của trường học, cơ quan báo chí uy tín hoặc trang mạng xã hội đã được xác thực.</p>',
        ),
        (
            '<p class="lesson-p">Nếu đoạn văn bản chứa thông tin không thể tìm thấy trong sách giáo khoa, bài</p>\n'
            '<p class="lesson-p">giảng hoặc tài liệu đáng tin cậy, em cần cảnh giác. Một số dấu hiệu của tin già do AI tạo có thể là; thông tin quá chung chung,',
            '<p class="lesson-p">Nếu đoạn văn bản chứa thông tin không thể tìm thấy trong sách giáo khoa, bài giảng hoặc tài liệu đáng tin cậy, em cần cảnh giác. Một số dấu hiệu của tin giả do AI tạo có thể là: thông tin quá chung chung,',
        ),
        (
            "bởi nội dung già, em nên đối chiếu thông tin với sách giáo khoa, trang web chính thức, hỏi thầy cô giáo hoặc tham khảo từ các nguồn nội dung học lập đã được kiểm duyệt.",
            "bởi nội dung giả, em nên đối chiếu thông tin với sách giáo khoa, trang web chính thức, hỏi thầy cô giáo hoặc tham khảo từ các nguồn nội dung học tập đã được kiểm duyệt.",
        ),
        ("B. Chia sẻ ngay nội dung đoạn văn đỏ cho bạn bè.", "B. Chia sẻ ngay nội dung đoạn văn đó cho bạn bè."),
        (
            '<p class="lesson-p">C. Đối chiếu nội dung đoạn văn đó với nguồn chính thống</p>\n'
            '<p class="lesson-p">D. Diễn đạt lại theo ý mình và không cần kiểm tra lại độ chính xác của đoạn văn</p>\n'
            '<p class="lesson-p">được tạo ra.</p>',
            '<p class="lesson-p">C. Đối chiếu nội dung đoạn văn đó với nguồn chính thống.</p>\n'
            '<p class="lesson-p">D. Diễn đạt lại theo ý mình và không cần kiểm tra lại độ chính xác của đoạn văn được tạo ra.</p>',
        ),
        (
            """<p class="lesson-p">Hiện tượng Khái niệm</p>
<p class="lesson-p">A. Một đoạn văn trôi chảy nhưng chứa thông tin</p>
<p class="lesson-p">không đúng.</p>
<h3 class="subheading-h3"><span class="h3-num">1.</span> Bia dặt.</h3>
<p class="lesson-p">B. Một video giả mạo người nỗi tiếng đang phát biểu.

2. Giả mạo.</p>""",
            """<p class="lesson-p"><strong>Hiện tượng — Khái niệm:</strong></p>
<ul class="lesson-bullet-list">
<li>1. Bịa đặt. — A. Một đoạn văn trôi chảy nhưng chứa thông tin không đúng.</li>
<li>2. Giả mạo. — B. Một video giả mạo người nổi tiếng đang phát biểu.</li>
</ul>""",
        ),
        (
            'với chủ đề Nguy cơ từ nội dung giả do AI tạo ra".',
            'với chủ đề "Nguy cơ từ nội dung giả do AI tạo ra".',
        ),
        ("cuộc thì thuyết trình", "cuộc thi thuyết trình"),
        ("lòng ghép khái niệm bịa đặt", "lồng ghép khái niệm bịa đặt"),
        ("khiến nhiều người hiểu lầm,</p>", "khiến nhiều người hiểu lầm.</p>"),
        ("học sinh Trung học phố thông", "học sinh Trung học phổ thông"),
    ],
    "bai-8-hieu-dung-ve-ai-tao-sinh-thien-vi-hieu-lam-va-tac-hai-voi-con-nguoi": [
        (
            """<p class="lesson-p">BÀI 8. HIỂU ĐÚNG VỀ AI TẠO SINH: THIÊN VỊ</p>
<p class="lesson-p">HIỂU LẦM VÀ TÁC HẠI VỚI CON NGƯỜI</p>
<p class="lesson-p">MUC TIEU</p>
<p class="lesson-p">Sau bài học này, em sẽ:</p>
<p class="lesson-p">• Giải thích được thiên vị (bias) trong AI tạo sinh và nêu ví dụ về hậu quả.</p>
<p class="lesson-p">• Nhận biết được một số hiểu làm thường gặp về AI.</p>
<p class="lesson-p">• Nêu được vai trò của con người trong việc sử dụng AI đúng cách và công băng.</p>""",
            section_open("target-section", "sec-mục-tiêu", "🎯", "MỤC TIÊU").strip()
            + '\n<p class="lesson-p">Sau bài học này, em sẽ:</p>\n'
            '<ul class="lesson-bullet-list">\n'
            '<li>Giải thích được thiên vị (bias) trong AI tạo sinh và nêu ví dụ về hậu quả.</li>\n'
            '<li>Nhận biết được một số hiểu lầm thường gặp về AI.</li>\n'
            '<li>Nêu được vai trò của con người trong việc sử dụng AI đúng cách và công bằng.</li>\n'
            '</ul>\n</div></section>',
        ),
        (
            '<p class="lesson-p">Một công ty dùng AI để chọn hồ sơ ứng viên. Sau một thời gian, họ thây Ai thường</p>\n'
            '<p class="lesson-p">chọn hồ sơ ứng viên nam giới cho vị trí kĩ thuật, dù có nhiều ứng viên nữ năng lực tương đương. Hoa ra, AI học từ dữ liệu cũ',
            '<p class="lesson-p">Một công ty dùng AI để chọn hồ sơ ứng viên. Sau một thời gian, họ thấy AI thường chọn hồ sơ ứng viên nam giới cho vị trí kĩ thuật, dù có nhiều ứng viên nữ năng lực tương đương. Hoá ra, AI học từ dữ liệu cũ',
        ),
        (
            '<p class="lesson-p">KHÁM PHẢ</p>',
            '</div></section>' + section_open("discovery-section", "sec-khám-phá", "🔍", "KHÁM PHÁ"),
        ),
        (
            '<p class="lesson-p">Trong tình huống Khởi động, hệ thống AI đề xuất hồ sơ ứng viên chủ yếu là nam giới cho các vi trí kĩ thuật, dù có những nữ ứng viên có trình độ tương đương.\n\n'
            'Đây không phải lỗi kĩ thuật mà là do dữ liêu huấn luyên hê thống AI đó bi mất cân bằng.</p>\n'
            '<p class="lesson-p">50 51</p>\n<p class="lesson-p">→ E Bias</p>',
            '<p class="lesson-p">Trong tình huống Khởi động, hệ thống AI đề xuất hồ sơ ứng viên chủ yếu là nam giới cho các vị trí kĩ thuật, dù có những nữ ứng viên có trình độ tương đương. Đây không phải lỗi kĩ thuật mà là do dữ liệu huấn luyện hệ thống AI đó bị mất cân bằng.</p>',
        ),
        ("Al tạo sinh có thể tạo ra nội dung thiên vị", "AI tạo sinh có thể tạo ra nội dung thiên vị"),
        (
            'AI có thể</p>\n<p class="lesson-p">cùng cố định kiến,',
            'AI có thể củng cố định kiến,',
        ),
        (
            '<p class="lesson-p">Ví dụ, nếu Ai được huấn luyện chủ yếu tử dữ liệu của một vùng địa lí hoặc ngón ngữ nhất định, khi người dùng hỏi về văn hóa, phong tục hoặc truyền thống. AI có thể thiên về khu vực đó và bỏ sót các đặc điểm của những vùng khác. Điều này có thể khiến người dùng hiểu chưa đầy đủ về sự đa dạng văn hóa hoặc đưa ra kết luân thiếu chính xác</p>',
            '<p class="lesson-p">Ví dụ, nếu AI được huấn luyện chủ yếu từ dữ liệu của một vùng địa lí hoặc ngôn ngữ nhất định, khi người dùng hỏi về văn hóa, phong tục hoặc truyền thống, AI có thể thiên về khu vực đó và bỏ sót các đặc điểm của những vùng khác. Điều này có thể khiến người dùng hiểu chưa đầy đủ về sự đa dạng văn hóa hoặc đưa ra kết luận thiếu chính xác.</p>',
        ),
        (
            '<p class="lesson-p">Thiên vị trong AI tạo sinh là hiện tượng mô hình tạo ra kết</p>\n'
            '<p class="lesson-p">quả thiếu công bằng hoặc mang định kiến, do ảnh hưởng từ dữ liệu mà nó được huấn luyện.</p>\n'
            '<ul class="lesson-bullet-list">\n'
            '<li>Thiên vị trong AI tạo sinh có thể dẫn đến thông tin sai lệch, quyết định thiếu công bằng, củng cố đinh kiến xã hôi và làm giảm độ tin cậy của hệ thống AI, nhất là trong các lĩnh vực như giáo dục, tuyển dụng, y tế, truyền thông....</li>\n'
            '</ul>',
            '<ul class="lesson-bullet-list">\n'
            '<li>Thiên vị trong AI tạo sinh là hiện tượng mô hình tạo ra kết quả thiếu công bằng hoặc mang định kiến, do ảnh hưởng từ dữ liệu mà nó được huấn luyện.</li>\n'
            '<li>Thiên vị trong AI tạo sinh có thể dẫn đến thông tin sai lệch, quyết định thiếu công bằng, củng cố định kiến xã hội và làm giảm độ tin cậy của hệ thống AI, nhất là trong các lĩnh vực như giáo dục, tuyển dụng, y tế, truyền thông,...</li>\n'
            '</ul>',
        ),
        (
            '<p class="lesson-p">2. Một số hiểu lầm thường gặp khi sử dụng AI tạo sinh Trở lại tình huống Khởi động, có thể thấy kết quả do AI tạo sinh đưa ra đôi khi bi ành hưởng bởi dữ liệu huấn luyện và không phản ánh đầy đủ thực tế. Điều này cho thấy nếu người dùng không hiểu rõ về cách hoạt động của Ai, có thể dễ gặp phải một số hiểu lầm khi sử dụng công cụ này trong học tập hoặc đời sống.\n\n52</p>',
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Một số hiểu lầm thường gặp khi sử dụng AI tạo sinh</h3>\n'
            '<p class="lesson-p">Trở lại tình huống Khởi động, có thể thấy kết quả do AI tạo sinh đưa ra đôi khi bị ảnh hưởng bởi dữ liệu huấn luyện và không phản ánh đầy đủ thực tế. Điều này cho thấy nếu người dùng không hiểu rõ về cách hoạt động của AI, có thể dễ gặp phải một số hiểu lầm khi sử dụng công cụ này trong học tập hoặc đời sống.</p>',
        ),
        (
            '<p class="lesson-p">Một trong những hiếu lầm đó là cho rằng nội dung do AI tạo sinh tạo ra luôn đúng và có thể sử dụng ngay. Tuy nhiên, AI tạo nội dung dựa trên dữ liệu đã học, nên</p>\n'
            '<p class="lesson-p">kết quả có thể chưa phù hợp với từng mục tiêu sử dụng khác nhau. Người dùng</p>\n'
            '<p class="lesson-p">cần đọc kĩ, căn nhắc và điều chỉnh nội dung để đám bảo',
            '<p class="lesson-p">Một trong những hiểu lầm đó là cho rằng nội dung do AI tạo sinh tạo ra luôn đúng và có thể sử dụng ngay. Tuy nhiên, AI tạo nội dung dựa trên dữ liệu đã học, nên kết quả có thể chưa phù hợp với từng mục tiêu sử dụng khác nhau. Người dùng cần đọc kĩ, cân nhắc và điều chỉnh nội dung để đảm bảo',
        ),
        ("nghĩ rắng AI có thể thay thế hoàn toàn khá năng suy nghĩ", "nghĩ rằng AI có thể thay thế hoàn toàn khả năng suy nghĩ"),
        ("người dùng có thể hiểu lầm như:\n\nnội dung luôn đúng,", "người dùng có thể hiểu lầm như: nội dung luôn đúng,"),
        ('<p class="lesson-p">V</p>\n', ""),
        (
            '<p class="lesson-p">Trong tình huống Khởi động, hệ thống AI tạo sinh được dùng trong tuyển dụng đã</p>\n'
            '<p class="lesson-p">đưa ra kết quả có xu hướng ưu tiên ứng viên nam giới, dù năng lực giữa các ứng viên nam giới và nữ giới là tương đương. Điều này cho thấy AI có thể tạo ra nội</p>\n'
            '<p class="lesson-p">dung chưa chính xác hoặc mang định kiến. Trên thực tế, nhiều ứng dụng AI như ChatGPT cũng thường hiển thị cảnh báo ở phần kết quả, khuyến nghị người dùng nên kiểm tra lại thông tin trước khi sử dụng. Do đó, khi sử dụng AI, con người cần</p>\n'
            '<p class="lesson-p">theo dõi và điều chỉnh kết quả để đảm bảo tính chính xác và công bằng.</p>',
            '<p class="lesson-p">Trong tình huống Khởi động, hệ thống AI tạo sinh được dùng trong tuyển dụng đã đưa ra kết quả có xu hướng ưu tiên ứng viên nam giới, dù năng lực giữa các ứng viên nam giới và nữ giới là tương đương. Điều này cho thấy AI có thể tạo ra nội dung chưa chính xác hoặc mang định kiến. Trên thực tế, nhiều ứng dụng AI như ChatGPT cũng thường hiển thị cảnh báo ở phần kết quả, khuyến nghị người dùng nên kiểm tra lại thông tin trước khi sử dụng. Do đó, khi sử dụng AI, con người cần theo dõi và điều chỉnh kết quả để đảm bảo tính chính xác và công bằng.</p>',
        ),
        (
            '<p class="lesson-p">Việc sử dụng Ai đúng cách không chỉ phụ thuộc vào công nghệ, mà còn phụ thuộc vao cách con người thiết kế, kiểm tra và vận hành hệ thống. Người phát triển và</p>\n'
            '<p class="lesson-p">người sử dụng cần thường xuyên đánh giá dữ liệu đầu vào, theo dõi kết quả đầu ra và điều chỉnh khi phát hiện dấu hiệu thiên vị. Ngoài ra, kết quả do AI tạo ra cân được xem xét kĩ lưỡng trước khi sử dụng, tránh phụ thuộc hoàn toàn vào nội dung được gợi ý.</p>',
            '<p class="lesson-p">Việc sử dụng AI đúng cách không chỉ phụ thuộc vào công nghệ, mà còn phụ thuộc vào cách con người thiết kế, kiểm tra và vận hành hệ thống. Người phát triển và người sử dụng cần thường xuyên đánh giá dữ liệu đầu vào, theo dõi kết quả đầu ra và điều chỉnh khi phát hiện dấu hiệu thiên vị. Ngoài ra, kết quả do AI tạo ra cần được xem xét kĩ lưỡng trước khi sử dụng, tránh phụ thuộc hoàn toàn vào nội dung được gợi ý.</p>',
        ),
        ("Sử dụng Ai công bằng nghĩa là tôn trọng sự đa dạng và đàm bảo", "Sử dụng AI công bằng nghĩa là tôn trọng sự đa dạng và đảm bảo"),
        ("tận dụng được hổ trợ từ AI", "tận dụng được hỗ trợ từ AI"),
        ("phản biện và thế hiện ý kiến cá nhân", "phản biện và thể hiện ý kiến cá nhân"),
        ("đóng vai trò kiềm soát và điều chỉnh", "đóng vai trò kiểm soát và điều chỉnh"),
        ("D. Vì AI chỉ dùng ngôn ngũ lập trình đề suy luận.", "D. Vì AI chỉ dùng ngôn ngữ lập trình để suy luận."),
        ("A. Cần kiểm tra lại nội dung do AI tạo ra trước khi sử dụng</p>", "A. Cần kiểm tra lại nội dung do AI tạo ra trước khi sử dụng.</p>"),
        ("B. Có thể điều chinh thông tin", "B. Có thể điều chỉnh thông tin"),
        ("A. Tin tường tuyệt đối", "A. Tin tưởng tuyệt đối"),
        ("D. Dùng nguyên văn nội dung AI trà về", "D. Dùng nguyên văn nội dung AI trả về"),
        ("Em sẽ làm gì đề đảm bảo", "Em sẽ làm gì để đảm bảo"),
        (
            '<p class="lesson-p">2. Ở nhà, em muốn tìm hiểu thêm kiến thức và rèn kĩ năng viết đoạn văn nghị luận.\n\nEm dự định dùng AI tạo sinh để thạm khảo ý tưởng và luyện tập thêm. Em sẽ sử dụng AI như thế nào để đảm bảo đúng cách và công băng?</p>',
            '<p class="lesson-p">2. Ở nhà, em muốn tìm hiểu thêm kiến thức và rèn kĩ năng viết đoạn văn nghị luận. Em dự định dùng AI tạo sinh để tham khảo ý tưởng và luyện tập thêm. Em sẽ sử dụng AI như thế nào để đảm bảo đúng cách và công bằng?</p>',
        ),
        ('<p class="lesson-p">D</p>\n', ""),
    ],
    "bai-9-cong-dan-so-trong-ki-nguyen-ai": [
        ("của công dân số trong kì nguyên AI hướng tới", "của công dân số trong kỉ nguyên AI hướng tới"),
        (
            '<li>Trình bày được quan điểm cá nhân về trách nhiệm của công dân số trong kỉ nguyên AI hướng tới một xã hội công bằng, an toàn và phát triển bền vững.</li>\n</ul>\n<p class="lesson-p">Rèn luyện tư duy phân biện và kĩ năng tranh biện về lợi ích và rủi ro từ việc sử dụng AI.</p>',
            '<li>Trình bày được quan điểm cá nhân về trách nhiệm của công dân số trong kỉ nguyên AI hướng tới một xã hội công bằng, an toàn và phát triển bền vững.</li>\n<li>Rèn luyện tư duy phản biện và kĩ năng tranh biện về lợi ích và rủi ro từ việc sử dụng AI.</li>\n</ul>',
        ),
        ("để lại thông tin cá nhân ờ phản bình luận", "để lại thông tin cá nhân ở phần bình luận"),
        ("công dân số trong ki nguyên AI</h3>", "công dân số trong kỉ nguyên AI</h3>"),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Thảo luận để trả lời cho câu hỏi: Công dân số cần trang bị những gì trong</h4>\n<p class="lesson-p">ki nguyên AI?</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Thảo luận để trả lời cho câu hỏi: Công dân số cần trang bị những gì trong kỉ nguyên AI?</h4>',
        ),
        ("mỗi chúng ta cần phát huy vai trò và trách nhiệm của mình để cùng nhau giữ gin,", "mỗi chúng ta cần phát huy vai trò và trách nhiệm của mình để cùng nhau giữ gìn,"),
        ("thực hiện những thỏi quen nào", "thực hiện những thói quen nào"),
        ("cần làm gì đề nhận diện", "cần làm gì để nhận diện"),
        (
            """<p class="lesson-p">Bảng 9.1. Một số năng lực đối với mỗi công dân số trong kỉ nguyên A/</p>
<p class="lesson-p">Chủ đê thảo luận Năng lực cần trang bị</p>
<p class="lesson-p">Khai thác dữ liêu và thông tin</p>
<p class="lesson-p">Biết tìm kiếm, thu thập, lưu trữ, đánh giá và chọn lọc nguồn thông tin đáng tin cậy.</p>
<p class="lesson-p">Giao tiếp và hợp tác trong môi trường số</p>
<p class="lesson-p">Ứng xử văn minh, tôn trong khi trao đỏi trực tuyến; lưu ý bảo mật và trách nhiệm khi chia sẻ nội dung.</p>
<p class="lesson-p">Tạo ra và chia sẻ sản phẩm số có giá trị, sử dụng nội dung Sáng tạo nội dung số do AI tạo ra một cách có trách nhiệm, tuân thủ đạo đức và pháp luật.</p>
<p class="lesson-p">An toàn số Bảo vệ dữ liệu cá nhân, giữ gìn quyền riêng tư, thực hiện thói quen an toàn để hạn chế rủi ro trên mạng.</p>
<p class="lesson-p">Giải quyết vấn đề Nhận diện và xử lí sự cố kĩ thuật, lựa chọn giải pháp công nghệ phú hợp trong từng tình huống.</p>
<p class="lesson-p">Hiểu biết và ứng dụng Có kiến thức cơ bản về AI, biết sử dụng AI trong học tập,</p>
<p class="lesson-p">Al công việc và đời sống, đồng thời có trách nhiệm khi khai thác công nghệ này.</p>""",
            """<p class="lesson-p"><strong>Bảng 9.1. Một số năng lực đối với mỗi công dân số trong kỉ nguyên AI</strong></p>
<ul class="lesson-bullet-list">
<li><strong>Khai thác dữ liệu và thông tin:</strong> Biết tìm kiếm, thu thập, lưu trữ, đánh giá và chọn lọc nguồn thông tin đáng tin cậy.</li>
<li><strong>Giao tiếp và hợp tác trong môi trường số:</strong> Ứng xử văn minh, tôn trọng khi trao đổi trực tuyến; lưu ý bảo mật và trách nhiệm khi chia sẻ nội dung.</li>
<li><strong>Sáng tạo nội dung số:</strong> Tạo ra và chia sẻ sản phẩm số có giá trị, sử dụng nội dung do AI tạo ra một cách có trách nhiệm, tuân thủ đạo đức và pháp luật.</li>
<li><strong>An toàn số:</strong> Bảo vệ dữ liệu cá nhân, giữ gìn quyền riêng tư, thực hiện thói quen an toàn để hạn chế rủi ro trên mạng.</li>
<li><strong>Giải quyết vấn đề:</strong> Nhận diện và xử lí sự cố kĩ thuật, lựa chọn giải pháp công nghệ phù hợp trong từng tình huống.</li>
<li><strong>Hiểu biết và ứng dụng AI:</strong> Có kiến thức cơ bản về AI, biết sử dụng AI trong học tập, công việc và đời sống, đồng thời có trách nhiệm khi khai thác công nghệ này.</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">Dựa trên cơ sở khoa học và các yếu tố như con người, bối cảnh xã hội, cũng như sự phát triển nhanh chóng của công nghệ, nhiều nghiên cứu trên thế giới đã đề xuất khung năng lực số, khung năng lực trí tuệ nhân tạo mà mỗi người cần được</p>\n'
            '<p class="lesson-p">Các khung năng lực thường được phân chia thành nhiều cấp độ cụ thể theo từng giai đoạn.</p>',
            '<p class="lesson-p">Dựa trên cơ sở khoa học và các yếu tố như con người, bối cảnh xã hội, cũng như sự phát triển nhanh chóng của công nghệ, nhiều nghiên cứu trên thế giới đã đề xuất khung năng lực số, khung năng lực trí tuệ nhân tạo mà mỗi người cần được hình thành và phát triển trong kỉ nguyên AI. Các khung năng lực thường được phân chia thành nhiều cấp độ cụ thể theo từng giai đoạn.</p>',
        ),
        (
            """<p class="lesson-p">KHAI THÁC DỮ LIỆU</p>
<p class="lesson-p">VÀ THÔNG TIN</p>
<p class="lesson-p">TRONG MÔI TRƯỜNG SỐ</p>
<p class="lesson-p">GIAO TIẾP VÀ HỢP TÁC</p>
<p class="lesson-p">SÁNG TẠO NỘI DUNG SỐ</p>
<p class="lesson-p">ỨNG DỤNG</p>
<p class="lesson-p">TRÍ TUỆ NHÂN TẠO</p>
<p class="lesson-p">GIÁI QUYẾT</p>
<p class="lesson-p">VẤN ĐỀ AN TOÀN</p>""",
            "",
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Tư duy lấy con người làm trung tâm: Hướng đến việc giúp học sinh nhận thức</li>
</ul>
<p class="lesson-p">vai trò chủ động của con người, đánh giá lợi ích và rủi ro của AI, đồng thời thúc đẩy sự hiểu biết sâu sắc về sự phù hợp của các công cụ AI với nhu cầu của con người và sự phát triển bền vững của xã hội.</p>
<ul class="lesson-bullet-list">
<li>Đạo đức AI: Trang bị cho học sinh các kĩ năng xã hội đề nhận diện, thấu hiểu và</li>
</ul>
<p class="lesson-p">thực hành các nguyên tắc đạo đức trong suốt vòng đời của AI, từ đó hình thành</p>
<p class="lesson-p">ý thức trách nhiệm và đóng góp vào việc xây dựng các quy tắc ứng xử phù hợp</p>
<ul class="lesson-bullet-list">
<li>Kĩ thuật và ứng dụng AI: Cung cấp cho học sinh kiến thức tổng hợp về các khái</li>
</ul>
<p class="lesson-p">niệm cốt lõi của AI và kĩ năng vận hành các công cụ AI đã được chọn lọc để giải quyết các nhiệm vụ thực tế, tạo nền tảng cho việc ứng dụng AI một cách hiệu quả.</p>
<ul class="lesson-bullet-list">
<li>Thiết kế hệ thống AI: Phát triển các kĩ năng kĩ thuật toàn diện, từ việc xác định</li>
</ul>
<p class="lesson-p">vấn đề, xây dựng kiến trúc, huấn luyện, thử nghiệm đến tối ưu hóa hệ thống Al, qua đó thử thách và giúp học sinh hiểu sâu hơn về cách các hệ thống này hoạt động</p>""",
            """<ul class="lesson-bullet-list">
<li>Tư duy lấy con người làm trung tâm: Hướng đến việc giúp học sinh nhận thức vai trò chủ động của con người, đánh giá lợi ích và rủi ro của AI, đồng thời thúc đẩy sự hiểu biết sâu sắc về sự phù hợp của các công cụ AI với nhu cầu của con người và sự phát triển bền vững của xã hội.</li>
<li>Đạo đức AI: Trang bị cho học sinh các kĩ năng xã hội để nhận diện, thấu hiểu và thực hành các nguyên tắc đạo đức trong suốt vòng đời của AI, từ đó hình thành ý thức trách nhiệm và đóng góp vào việc xây dựng các quy tắc ứng xử phù hợp.</li>
<li>Kĩ thuật và ứng dụng AI: Cung cấp cho học sinh kiến thức tổng hợp về các khái niệm cốt lõi của AI và kĩ năng vận hành các công cụ AI đã được chọn lọc để giải quyết các nhiệm vụ thực tế, tạo nền tảng cho việc ứng dụng AI một cách hiệu quả.</li>
<li>Thiết kế hệ thống AI: Phát triển các kĩ năng kĩ thuật toàn diện, từ việc xác định vấn đề, xây dựng kiến trúc, huấn luyện, thử nghiệm đến tối ưu hoá hệ thống AI, qua đó thử thách và giúp học sinh hiểu sâu hơn về cách các hệ thống này hoạt động.</li>
</ul>""",
        ),
        (
            """<p class="lesson-p">Bảng 9.2. Khung năng lực trí tuệ nhân tạo cho học sinh (UNESCO, 2024)</p>
<p class="lesson-p">Các cấp độ tiến triển Khía cạnh năng lực</p>
<p class="lesson-p">Tiếp thu Áp dụng</p>
<p class="lesson-p">Kiến tạo</p>
<p class="lesson-p">Tư duy lấy con người</p>
<p class="lesson-p">Quyền tự chủ của Trách nhiệm giải</p>
<p class="lesson-p">con người.

trình của con người.</p>
<p class="lesson-p">Quyền công dân trong thời đại AI.</p>
<p class="lesson-p">làm trung tâm</p>
<p class="lesson-p">Đạo đức được Sử dụng an toàn thấm nhuần.

và có trách nhiêm.</p>
<p class="lesson-p">Đạo đức trong thiết kế.</p>
<p class="lesson-p">Kĩ thuật và ứng dụng AI</p>
<p class="lesson-p">Các nền tăng AI.

Kĩ năng áp dụng</p>
<p class="lesson-p">Tạo các công cụ AI.</p>
<p class="lesson-p">Thiết kế hệ thống AI</p>
<p class="lesson-p">Cải tiến và phản hồi.

vấn đề.</p>
<p class="lesson-p">Xác định phạm vi Thiết kế kiến trúc.</p>""",
            """<p class="lesson-p"><strong>Bảng 9.2. Khung năng lực trí tuệ nhân tạo cho học sinh (UNESCO, 2024)</strong></p>
<ul class="lesson-bullet-list">
<li><strong>Tư duy lấy con người làm trung tâm:</strong> Tiếp thu: Quyền tự chủ của con người. | Áp dụng: Trách nhiệm giải trình của con người. | Kiến tạo: Quyền công dân trong thời đại AI.</li>
<li><strong>Đạo đức AI:</strong> Tiếp thu: Đạo đức được thấm nhuần. | Áp dụng: Sử dụng an toàn và có trách nhiệm. | Kiến tạo: Đạo đức trong thiết kế.</li>
<li><strong>Kĩ thuật và ứng dụng AI:</strong> Tiếp thu: Các nền tảng AI. | Áp dụng: Kĩ năng áp dụng. | Kiến tạo: Tạo các công cụ AI.</li>
<li><strong>Thiết kế hệ thống AI:</strong> Tiếp thu: Xác định phạm vi vấn đề. | Áp dụng: Thiết kế kiến trúc. | Kiến tạo: Cải tiến và phản hồi.</li>
</ul>""",
        ),
        (
            """<p class="lesson-p">Trong kỉ nguyên AI, công dân số cần hình thành những năng lự°c cốt lỗi để sử dụng công nghệ an toàn, hiệu quả, có trách nhiệm, với mục tiêu phát triển bản thân và đóng góp tích cục cho cộng đồng, xã hội.</p>
<ul class="lesson-bullet-list">
<li>Các năng lực đó bao gồm kha năng khai thắc thông tin, giao tiếp và sáng tạo nội dung, cùng với năng lực đảm bảo an toàn</li>
</ul>
<p class="lesson-p">số để bảo vệ bán thân và dữ liệu. Quan trọng hơn, công dân số cần có tư duy lấy con người làm trung tâm, ý thức về đạo đức và năng lực ứng dụng AI để làm chủ công nghệ vì một tương lai phát triển bền vững</p>""",
            """<ul class="lesson-bullet-list">
<li>Trong kỉ nguyên AI, công dân số cần hình thành những năng lực cốt lõi để sử dụng công nghệ an toàn, hiệu quả, có trách nhiệm, với mục tiêu phát triển bản thân và đóng góp tích cực cho cộng đồng, xã hội.</li>
<li>Các năng lực đó bao gồm khả năng khai thác thông tin, giao tiếp và sáng tạo nội dung, cùng với năng lực đảm bảo an toàn số để bảo vệ bản thân và dữ liệu. Quan trọng hơn, công dân số cần có tư duy lấy con người làm trung tâm, ý thức về đạo đức và năng lực ứng dụng AI để làm chủ công nghệ vì một tương lai phát triển bền vững.</li>
</ul>""",
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Thào luận để trả lời cho câu hỏi: Công dân số cần có trách nhiệm gi khi</h4>\n<p class="lesson-p">sử dụng AI?</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Thảo luận để trả lời cho câu hỏi: Công dân số cần có trách nhiệm gì khi sử dụng AI?</h4>',
        ),
        (
            "Nhiệm vụ 2: Em hãy thào luận cùng các bạn trong lớp để trình bày một số nội dung cơ bản về trách nhiệm, nghĩa vụ của công dân số khi sử dụng AI và những thôi quen hành động",
            "Nhiệm vụ 2: Em hãy thảo luận cùng các bạn trong lớp để trình bày một số nội dung cơ bản về trách nhiệm, nghĩa vụ của công dân số khi sử dụng AI và những thói quen hành động",
        ),
        (
            '<p class="lesson-p">+ Em cần lưu ý điều gì khi tương tác, giao tiếp và đưa ra phản hồi cho hệ thống</p>\n<p class="lesson-p">Al?</p>',
            '<p class="lesson-p">+ Em cần lưu ý điều gì khi tương tác, giao tiếp và đưa ra phản hồi cho hệ thống AI?</p>',
        ),
        (
            """<p class="lesson-p">Bảng 9.3. Trách nhiệm, nghĩa vụ của công dân số khi sử dụng AI</p>
<p class="lesson-p">Khía cạnh Trách nhiệm, nghĩa vụ</p>
<p class="lesson-p">Bảo vệ dữ liệu cả nhân và thông tin riêng tư</p>
<p class="lesson-p">Cần thận trong khi chia sẻ dữ liệu, biết lụa chọn và sử dụng công cụ AI an toàn để trành bị thu thập thông tn ngoài ý muốn.</p>
<p class="lesson-p">Sử dụng nội dung do AI tạo ra</p>
<p class="lesson-p">Cần cân nhắc khi sử dụng và chia sẻ sản phẩm do Ai tạo.

tránh phát tán tháng tri sai lệch, gáy ảnh hưởng đến cộng đồng</p>
<p class="lesson-p">Tác động đỏi với hệ thống AI</p>
<p class="lesson-p">Khi tương tác và phản hồi với AI, cần đưa ra thông tin rõ ràng.

chính xác, gáp phần giúp hệ thống hoạt động hiệu quả và đáng tin cậy hơn.</p>""",
            """<p class="lesson-p"><strong>Bảng 9.3. Trách nhiệm, nghĩa vụ của công dân số khi sử dụng AI</strong></p>
<ul class="lesson-bullet-list">
<li><strong>Bảo vệ dữ liệu cá nhân và thông tin riêng tư:</strong> Cần thận trọng khi chia sẻ dữ liệu, biết lựa chọn và sử dụng công cụ AI an toàn để tránh bị thu thập thông tin ngoài ý muốn.</li>
<li><strong>Sử dụng nội dung do AI tạo ra:</strong> Cần cân nhắc khi sử dụng và chia sẻ sản phẩm do AI tạo, tránh phát tán thông tin sai lệch, gây ảnh hưởng đến cộng đồng.</li>
<li><strong>Tác động đối với hệ thống AI:</strong> Khi tương tác và phản hồi với AI, cần đưa ra thông tin rõ ràng, chính xác, góp phần giúp hệ thống hoạt động hiệu quả và đáng tin cậy hơn.</li>
</ul>""",
        ),
        (
            '<span class="h4-letter">b)</span> Một số thói quen quan trong khi sử dụng AI</h4>',
            '<span class="h4-letter">b)</span> Một số thói quen quan trọng khi sử dụng AI</h4>',
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Bảo vệ dữ liệu cá nhân và quyền riêng tư. Không chia sẻ thông tin nhạy cảm.</li>
</ul>
<p class="lesson-p">cần trọng với yêu cầu truy cập dữ liệu và đọc kĩ chính sách bào mặt trước khi sử dụng công cụ AI.</p>
<ul class="lesson-bullet-list">
<li>Đánh giá mức độ cần thiết hay việc nên/không nên sử dụng AI: Tuy thuộc vào</li>
</ul>
<p class="lesson-p">mục đích và điều kiện cụ thể, mỗi người cần đánh giá và trả lời câu hỏi "Liệu tình huống này có phù hợp để dùng AI không?'. Đồng thời, cần cản nhắc mức độ tin cậy và đánh giá khả năng ảnh hưởng, tác động hay những hậu quả mà nó có thể gây ra cho bản thân, cộng đồng và xã hội trước khi đưa ra quyết định.</p>
<ul class="lesson-bullet-list">
<li>Có trách nhiệm trong việc sử dụng nội dung tạo bởi AI: Luôn kiểm chứng các</li>
</ul>
<p class="lesson-p">nội dung trước khi chia sẻ, trích dẫn rõ nguồn gốc hoặc tuyên bố các nội dung được tạo ra bởi AI khi sử dụng; tránh lan truyền thông tin sai lệch. Đồng thời, không được khai thác AI cho các mục đích xấu hoặc tạo nội dung gây hại</p>
<ul class="lesson-bullet-list">
<li>Nhận thức vai trò tác động ngược lại đối với hệ thống AI: Việc đưa ra phản hồi</li>
</ul>
<p class="lesson-p">đúng, đầy đủ và có trách nhiệm sẽ giúp AI cải thiện chất lượng. Ngược lại, các phân hồi sai lệch có thể làm giảm hiệu quả của các công cụ AI.</p>""",
            """<ul class="lesson-bullet-list">
<li>Bảo vệ dữ liệu cá nhân và quyền riêng tư: Không chia sẻ thông tin nhạy cảm, cẩn trọng với yêu cầu truy cập dữ liệu và đọc kĩ chính sách bảo mật trước khi sử dụng công cụ AI.</li>
<li>Đánh giá mức độ cần thiết hay việc nên/không nên sử dụng AI: Tuỳ thuộc vào mục đích và điều kiện cụ thể, mỗi người cần đánh giá và trả lời câu hỏi "Liệu tình huống này có phù hợp để dùng AI không?". Đồng thời, cần cân nhắc mức độ tin cậy và đánh giá khả năng ảnh hưởng, tác động hay những hậu quả mà nó có thể gây ra cho bản thân, cộng đồng và xã hội trước khi đưa ra quyết định.</li>
<li>Có trách nhiệm trong việc sử dụng nội dung tạo bởi AI: Luôn kiểm chứng các nội dung trước khi chia sẻ, trích dẫn rõ nguồn gốc hoặc tuyên bố các nội dung được tạo ra bởi AI khi sử dụng; tránh lan truyền thông tin sai lệch. Đồng thời, không được khai thác AI cho các mục đích xấu hoặc tạo nội dung gây hại.</li>
<li>Nhận thức vai trò tác động ngược lại đối với hệ thống AI: Việc đưa ra phản hồi đúng, đầy đủ và có trách nhiệm sẽ giúp AI cải thiện chất lượng. Ngược lại, các phản hồi sai lệch có thể làm giảm hiệu quả của các công cụ AI.</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">3. Trách nhiệm xã hội của công dân trong ki nguyễn AI a) Công dân số cần làm gì để thể hiện trách nhiệm xã hội trong kỉ nguyên AI?</p>',
            '<h3 class="subheading-h3"><span class="h3-num">3.</span> Trách nhiệm xã hội của công dân trong kỉ nguyên AI</h3>\n'
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Công dân số cần làm gì để thể hiện trách nhiệm xã hội trong kỉ nguyên AI?</h4>',
        ),
        ("Em hãy thào luận cùng các bạn trong lớp đề trình bày", "Em hãy thảo luận cùng các bạn trong lớp để trình bày"),
        (
            '<p class="lesson-p">+ Em nên làm gì khi bắt gặp các thông tin chưa chắc chắn, có dâu hiệu sai lệch</p>\n'
            '<p class="lesson-p">trên mạng xã hội hoạc từ cộng đồng xung quanh?</p>\n'
            '<p class="lesson-p">+ Công dân số có thể làm gì đế góp phần tạo môi trường số minh bạch và tin cậy?</p>',
            '<p class="lesson-p">+ Em nên làm gì khi bắt gặp các thông tin chưa chắc chắn, có dấu hiệu sai lệch trên mạng xã hội hoặc từ cộng đồng xung quanh?</p>\n'
            '<p class="lesson-p">+ Công dân số có thể làm gì để góp phần tạo môi trường số minh bạch và tin cậy?</p>',
        ),
        (
            '<p class="lesson-p">+ Cũng với sự hỗ trợ của AI, chúng ta có thể làm những điều gì để đóng góp</p>\n'
            '<p class="lesson-p">cho cộng đồng, xã hội?</p>\n'
            '<p class="lesson-p">+ Em có thể chia sẻ kiến thức và kĩ năng của minh như thế nào để góp phần</p>\n'
            '<p class="lesson-p">nâng cao hiểu biết của mọi người xung quanh về AI và cách sử dụng AI?</p>',
            '<p class="lesson-p">+ Cùng với sự hỗ trợ của AI, chúng ta có thể làm những điều gì để đóng góp cho cộng đồng, xã hội?</p>\n'
            '<p class="lesson-p">+ Em có thể chia sẻ kiến thức và kĩ năng của mình như thế nào để góp phần nâng cao hiểu biết của mọi người xung quanh về AI và cách sử dụng AI?</p>',
        ),
        (
            """<p class="lesson-p">Bảng 9.4. Trách nhiệm xã hội của công dân số trong kỉ nguyên AI</p>
<p class="lesson-p">Khía cạnh</p>
<p class="lesson-p">Trách nhiệm xã hội</p>
<p class="lesson-p">Cần thận trọng trước những thông tin chưa chắc chấn hoặc có dấu hiệu sai lệch; biết kiểm chứng và lựa chọn nguồn</p>
<p class="lesson-p">Phân biện và chia sẻ thông tin</p>
<p class="lesson-p">tin đáng tin cậy; góp phần xây dựng không gian mạng mình bạch va tin cậy.</p>
<p class="lesson-p">Biết khai thác AI đề hỗ trợ các hoạt động có ích cho cộng đồng; sẵn sàng chia sẻ kiến thức, kĩ năng và kinh nghiệm, giúp nâng cao hiểu biết của mọi người về AI và cách sử dụng công nghệ một cách hiệu quả, an toàn.</p>
<p class="lesson-p">Tham gia hoạt động cộng đồng, xã hội</p>""",
            """<p class="lesson-p"><strong>Bảng 9.4. Trách nhiệm xã hội của công dân số trong kỉ nguyên AI</strong></p>
<ul class="lesson-bullet-list">
<li><strong>Phản biện và chia sẻ thông tin:</strong> Cần thận trọng trước những thông tin chưa chắc chắn hoặc có dấu hiệu sai lệch; biết kiểm chứng và lựa chọn nguồn tin đáng tin cậy; góp phần xây dựng không gian mạng minh bạch và tin cậy.</li>
<li><strong>Tham gia hoạt động cộng đồng, xã hội:</strong> Biết khai thác AI để hỗ trợ các hoạt động có ích cho cộng đồng; sẵn sàng chia sẻ kiến thức, kĩ năng và kinh nghiệm, giúp nâng cao hiểu biết của mọi người về AI và cách sử dụng công nghệ một cách hiệu quả, an toàn.</li>
</ul>""",
        ),
        ("Công dân sô trong thời đại AI cân nhận thức", "Công dân số trong thời đại AI cần nhận thức"),
        (
            """<ul class="lesson-bullet-list">
<li>Phản biện thóng tin: Khi tiếp nhận thông tin, mỗi người cần phân tích độ tin cậy</li>
</ul>
<p class="lesson-p">và đánh giá khả năng đó là những nội dung sai lệch được tạo ra bởi AI. Đồng thời,</p>
<p class="lesson-p">cần có trách nhiệm báo cáo hoặc cảnh báo tới những người có liên quan để tránh gây ra tác động xâu.</p>
<ul class="lesson-bullet-list">
<li>Xây dụng văn hóa ứng xử số: Mỗi người cần biết tôn trọng sự khác biệt, ứng xử</li>
</ul>
<p class="lesson-p">văn minh, tránh lan truyền thông tin độc hại hoác lời nói gây chia rẽ trong cộng đồng trực tuyến, từ đó cùng xây dựng không gian mạng lành mạnh.

- Chia sẻ tri thức và kĩ năng: Mỗi cá nhân có thể lan tỏa hiểu biết của minh về</p>
<p class="lesson-p">công nghệ và AI đến bạn bè, người thân, cộng đồng để giúp mọi người biết cách sử dụng các công cụ an toàn và hiệu quả hờn.</p>
<ul class="lesson-bullet-list">
<li>Tham gia hoạt động cộng đồng: Công dân số có thể ứng dụng hoặc tạo ra sản</li>
</ul>
<p class="lesson-p">phẩm Ai để hỗ trợ những hoạt động xã hội như giáo dục, bào vệ môi trường, chăm sóc sức khỏe hay hỗ trợ những nhóm yếu thế, qua đó góp phần lan tỏa giá trị nhân văn của công nghệ</p>""",
            """<ul class="lesson-bullet-list">
<li>Phản biện thông tin: Khi tiếp nhận thông tin, mỗi người cần phân tích độ tin cậy và đánh giá khả năng đó là những nội dung sai lệch được tạo ra bởi AI. Đồng thời, cần có trách nhiệm báo cáo hoặc cảnh báo tới những người có liên quan để tránh gây ra tác động xấu.</li>
<li>Xây dựng văn hóa ứng xử số: Mỗi người cần biết tôn trọng sự khác biệt, ứng xử văn minh, tránh lan truyền thông tin độc hại hoặc lời nói gây chia rẽ trong cộng đồng trực tuyến, từ đó cùng xây dựng không gian mạng lành mạnh.</li>
<li>Chia sẻ tri thức và kĩ năng: Mỗi cá nhân có thể lan tỏa hiểu biết của mình về công nghệ và AI đến bạn bè, người thân, cộng đồng để giúp mọi người biết cách sử dụng các công cụ an toàn và hiệu quả hơn.</li>
<li>Tham gia hoạt động cộng đồng: Công dân số có thể ứng dụng hoặc tạo ra sản phẩm AI để hỗ trợ những hoạt động xã hội như giáo dục, bảo vệ môi trường, chăm sóc sức khỏe hay hỗ trợ những nhóm yếu thế, qua đó góp phần lan tỏa giá trị nhân văn của công nghệ.</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">Sự phát triển mạnh mẽ của công nghệ, đặc biệt là AI, không chỉ đem lại nhiều cơ hội mới mà còn đặt ra những thách thức</p>\n'
            '<p class="lesson-p">chưa từng có cho xã hội. Trước bối cảnh đó, mỗi chúng ta cần phát huy vai trò và trách nhiệm của mình để cùng nhau giữ gìn, xây dựng xã hội văn minh, an loàn và phát triển bền vững.</p>',
            '<p class="lesson-p">Sự phát triển mạnh mẽ của công nghệ, đặc biệt là AI, không chỉ đem lại nhiều cơ hội mới mà còn đặt ra những thách thức chưa từng có cho xã hội. Trước bối cảnh đó, mỗi chúng ta cần phát huy vai trò và trách nhiệm của mình để cùng nhau giữ gìn, xây dựng xã hội văn minh, an toàn và phát triển bền vững.</p>',
        ),
        (
            '<p class="lesson-p">LUYỆN TẠP</p>',
            '</div></section>' + section_open("exercise-section", "sec-luyện-tập", "✏️", "LUYỆN TẬP"),
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Sử dụng AI để tạo ra những câu chuyện giải trí để chía sẻ mà không chú thích</h4>\n<p class="lesson-p">rõ rằng.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">a)</span> Sử dụng AI để tạo ra những câu chuyện giải trí để chia sẻ mà không chú thích rõ ràng.</h4>',
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">b)</span> Cung cấp nhiều thông tin chi tiết về bản thân và những người xung quanh</h4>\n<p class="lesson-p">để AI hiểu rõ minh hơn.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">b)</span> Cung cấp nhiều thông tin chi tiết về bản thân và những người xung quanh để AI hiểu rõ mình hơn.</h4>',
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">d)</span> Thoài mái chia sẻ mọi kết quả do AI tạo ra vì máy móc thông minh luôn</h4>\n<p class="lesson-p">chính xác.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">d)</span> Thoải mái chia sẻ mọi kết quả do AI tạo ra vì máy móc thông minh luôn chính xác.</h4>',
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">e)</span> Báo cáo cho nhà phát triển khi phát hiện AI đưa ra thông tin sai lệch hoặc</h4>\n<p class="lesson-p">độc hại.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">e)</span> Báo cáo cho nhà phát triển khi phát hiện AI đưa ra thông tin sai lệch hoặc độc hại.</h4>',
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">h)</span> Sử dụng AI tạo ra các đề tự luyện trước khi thì học kì rồi nhờ giáo viên chữa bài,</h4>\n<p class="lesson-p">chấm điểm.</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">h)</span> Sử dụng AI tạo ra các đề tự luyện trước khi thi học kì rồi nhờ giáo viên chữa bài, chấm điểm.</h4>',
        ),
        (
            '<p class="lesson-p">2. Để chia sẻ rộng rãi tới mọi người trong khu phố về công nghệ AI, An và Bình đã xin phép bác tổ trường tố dân phố làm một ẩn phẩm truyền thông đề dán tại nhà văn hóa và các địa điểm công cộng thường tập trung đông người. Để tăng mức độ thu hút và mong muốn mọi người quan tâm mạnh mẽ hơn đến vấn đề này, hai bạn đã quyết định đưa ra những thông điệp mạnh mẽ, như: "AI luôn biết tất</p>\n'
            '<p class="lesson-p">cả mọi thứ chính xác"; "AI sẽ thay thể hoàn toàn con người",...</p>',
            '<p class="lesson-p">2. Để chia sẻ rộng rãi tới mọi người trong khu phố về công nghệ AI, An và Bình đã xin phép bác tổ trưởng tổ dân phố làm một ấn phẩm truyền thông để dán tại nhà văn hóa và các địa điểm công cộng thường tập trung đông người. Để tăng mức độ thu hút và mong muốn mọi người quan tâm mạnh mẽ hơn đến vấn đề này, hai bạn đã quyết định đưa ra những thông điệp mạnh mẽ, như: "AI luôn biết tất cả mọi thứ chính xác"; "AI sẽ thay thế hoàn toàn con người",...</p>',
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">c)</span> Nếu là An và Bình, em sẽ lựa chọn những nội dung gi để giới thiệu về AI cho</h4>\n<p class="lesson-p">mọi người nơi em sinh sống?</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">c)</span> Nếu là An và Bình, em sẽ lựa chọn những nội dung gì để giới thiệu về AI cho mọi người nơi em sinh sống?</h4>',
        ),
        (
            "sáng tạo các nội dung nhỏ AI. Vao ki nghi lê, bạn ây nay ra ý tưởng là sử dụng hình ảnh của Lan - một bạn nữ xinh xăn trong trường - đê nhờ AI tạo ra những đoạn video kế chuyện dành cho các em nhỏ. Các video có giọng đọc truyền cảm với hình ảnh minh họa sống động và mang nhiều thông điệp ý nghĩa. Nhờ vậy, chúng nhanh chóng được chia sé rộng rãi, nhận được nhiều lời khen và sự yêu thích lừ mọi người.",
            "sáng tạo các nội dung nhờ AI. Vào kì nghỉ lễ, bạn ấy nảy ra ý tưởng là sử dụng hình ảnh của Lan - một bạn nữ xinh xắn trong trường - để nhờ AI tạo ra những đoạn video kể chuyện dành cho các em nhỏ. Các video có giọng đọc truyền cảm với hình ảnh minh họa sống động và mang nhiều thông điệp ý nghĩa. Nhờ vậy, chúng nhanh chóng được chia sẻ rộng rãi, nhận được nhiều lời khen và sự yêu thích từ mọi người.",
        ),
        (
            '<h4 class="subheading-h4"><span class="h4-letter">c)</span> Theo em, việc làm của Cường và cách xử lí của Lan có thể tạo ra những lợi ích</h4>\n<p class="lesson-p">hay hậu quả gì?</p>',
            '<h4 class="subheading-h4"><span class="h4-letter">c)</span> Theo em, việc làm của Cường và cách xử lí của Lan có thể tạo ra những lợi ích hay hậu quả gì?</h4>',
        ),
        (
            """<p class="lesson-p">A</p>
<p class="lesson-p">CHỦ ĐỀ 4. PHÁT TRIỂN SẢN PHẨM</p>
<p class="lesson-p">VÀ ỨNG DỤNG AI</p>
<p class="lesson-p">11111.</p>
<p class="lesson-p">Al</p>""",
            "",
        ),
    ],
    "bai-10-ai-va-nghe-nghiep": [
        ("tạo ra những co hội mới.", "tạo ra những cơ hội mới."),
        (
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Vì sao con người càng cần học hỏi và phát triển kĩ năng trong thời đại AI?</h3>',
            '<p class="lesson-p">2. Vì sao con người càng cần học hỏi và phát triển kĩ năng trong thời đại AI?</p>',
        ),
        ('<span class="h3-num">1.</span> ẠI tạo ra thay đổi và định hướng nghề nghiệp mới</h3>', '<span class="h3-num">1.</span> AI tạo ra thay đổi và định hướng nghề nghiệp mới</h3>'),
        (
            "Trong hình huống Khởi động, bạn Đức thắc mắc về vai trò của con người khi AI có thể làm được nhiều việc. Trong thực tế, AI đang góp mặt trong nhiều lĩnh vực và đảm nhận một số công việc vốn do con người thực hiện. Ví dụ, ở siêu thị, máy tự động thanh toán giúp khách hàng không cần chờ xếp hàng lâu; trong trung tâm chăm sóc khách hàng, chatbot có thể trả lời Hình 10.1. Tác động của AI đền việc làm các câu hỏi thường gặp; trong nhà máy, robot giúp phân loại và đóng gói sản phẩm nhanh chóng: trong ngành truyền thông, AI có thể tạo bản tin ngắn hoặc hình ánh minh hoạ dựa trên nội dung</p>",
            "Trong tình huống Khởi động, bạn Đức thắc mắc về vai trò của con người khi AI có thể làm được nhiều việc. Trong thực tế, AI đang góp mặt trong nhiều lĩnh vực và đảm nhận một số công việc vốn do con người thực hiện. Ví dụ, ở siêu thị, máy tự động thanh toán giúp khách hàng không cần chờ xếp hàng lâu; trong trung tâm chăm sóc khách hàng, chatbot có thể trả lời các câu hỏi thường gặp; trong nhà máy, robot giúp phân loại và đóng gói sản phẩm nhanh chóng; trong ngành truyền thông, AI có thể tạo bản tin ngắn hoặc hình ảnh minh hoạ dựa trên nội dung đầu vào.</p>",
        ),
        ("Tác động của AI đền việc làm", "Tác động của AI đến việc làm"),
        ("trả lời các câu hỏi phố biến như", "trả lời các câu hỏi phổ biến như"),
        ("Cùng với đó. AI cũng góp phần mờ ra những nghề nghiệp mới.", "Cùng với đó, AI cũng góp phần mở ra những nghề nghiệp mới."),
        ("kiếm tra độ tin cậy của nội dung", "kiểm tra độ tin cậy của nội dung"),
        ('<span class="h3-num">2.</span> Học hỏi để đồng hành cùng A</h3>', '<span class="h3-num">2.</span> Học hỏi để đồng hành cùng AI</h3>'),
        ("Học hồi để đồng hành cùng AI:", "Học hỏi để đồng hành cùng AI"),
        (
            '<p class="lesson-p">này sẽ giúp con người khai thác tối sức mạnh của AI thay vì bị phụ thuộc hoặc bị</p>',
            '<p class="lesson-p">này sẽ giúp con người khai thác tốt sức mạnh của AI thay vì bị phụ thuộc hoặc bị thay thế.</p>',
        ),
        (
            '<p class="lesson-p">Ví dụ, nếu một nhân viên văn phòng không câp nhât kĩ năng sử dụng công nghê.\n\nhọ có thể gặp khó khăn',
            '<p class="lesson-p">Ví dụ, nếu một nhân viên văn phòng không cập nhật kĩ năng sử dụng công nghệ, họ có thể gặp khó khăn',
        ),
        (
            '<p class="lesson-p">cần chủ động học hỏi và rèn luyện các kĩ năng như tư duy phản biện, giải quyết vấn đề, sáng tạo và sử dụng công</p>',
            '<p class="lesson-p">cần chủ động học hỏi và rèn luyện các kĩ năng như tư duy phản biện, giải quyết vấn đề, sáng tạo và sử dụng công cụ số.</p>',
        ),
        (
            '<p class="lesson-p">LUYỆN TẬP (</p>',
            '</div></section>' + section_open("exercise-section", "sec-luyện-tập", "✏️", "LUYỆN TẬP"),
        ),
        ("1. Phát biểu nào sau đảy phản ánh đúng", "1. Phát biểu nào sau đây phản ánh đúng"),
        ("không cần học lập về chuyên môn.", "không cần học tập về chuyên môn."),
        ("D. AI chỉ ảnh hưởng đến lĩnh vực kĩ thuật và lập trình</p>", "D. AI chỉ ảnh hưởng đến lĩnh vực kĩ thuật và lập trình.</p>"),
        ("ngày càng trờ nên quan trọng", "ngày càng trở nên quan trọng"),
        ("B. Vì cộng nghệ AI luôn thay đổi,", "B. Vì công nghệ AI luôn thay đổi,"),
        ("kĩ năng mới chỉ cân thiết với người", "kĩ năng mới chỉ cần thiết với người"),
        (
            '<h3 class="subheading-h3"><span class="h3-num">1.</span> Nghề nghiệp đó có thể bị ảnh hưởng như thế nào bởi sự phát triển của AI?</h3>\n'
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> lại cần chuẩn bị những kĩ năng gì để theo đuổi nghề nghiệp đỏ trong thời</h3>',
            '<p class="lesson-p">1. Nghề nghiệp đó có thể bị ảnh hưởng như thế nào bởi sự phát triển của AI?</p>\n'
            '<p class="lesson-p">2. Em cần chuẩn bị những kĩ năng gì để theo đuổi nghề nghiệp đó trong thời đại AI?</p>',
        ),
    ],
    "bai-11-moi-truong-phat-trien-san-pham-ai": [
        ('<p class="lesson-p">SẢN PHẨM AI</p>\n', ""),
        ("Trong một hoạt động ngoại khoa,", "Trong một hoạt động ngoại khoá,"),
        ("Minh đã từng thử dùng một công cụ", "Mình đã từng thử dùng một công cụ"),
        ("sản phẩm AI như vậy thi em có thể", "sản phẩm AI như vậy thì em có thể"),
        (
            '<h3 class="subheading-h3"><span class="h3-num">2.</span> Cần làm gì để bắt đầu thử nghiệm tạo sản phẩm đơn giản với AI?</h3>',
            '<p class="lesson-p">2. Cần làm gì để bắt đầu thử nghiệm tạo sản phẩm đơn giản với AI?</p>',
        ),
        ("đó là Google Colab và Kaggle cùng thuộc sở hữu</p>", "đó là Google Colab và Kaggle cùng thuộc sở hữu của Google.</p>"),
        (
            """<ul class="lesson-bullet-list">
<li>Google Colab (viết tất của Colaboratory) là một nền tầng lập trình trực tuyến</li>
</ul>
<p class="lesson-p">miễn phí do Google phát triển. Với Google Colab, em có thể viết và chạy mã lập trình bằng ngôn ngữ Python ngay trên trình duyệt, má không cần cài đặt phần mềm phức tạp. Google Colab hoạt động như một số tay điện lử gồm nhiều ô (cell), trong đó mỗi ô có thể chứa mã lệnh hoặc ghi chú giải thích. Em có thể</p>
<p class="lesson-p">chạy từng ô để xem ngay kết quả, rất thuận tiện cho việc học và thực hành</p>
<ul class="lesson-bullet-list">
<li>Kaggle là một nền tảng trực tuyến thuộc Google, thường được biết đến như</li>
</ul>
<p class="lesson-p">một cộng đồng Khoa học dữ liệu. Bên cạnh việc tổ chức các cuộc thi về dữ liệu, Kaggle cũng cung cấp môi trường lập trình trực tuyến đề viết và chạy mã</p>
<p class="lesson-p">Python trong các số tay (notebook). Giao diện làm việc của Kaggle tương tự Google Colab, đồng thời cho phép truy cập nhanh đến các bộ dữ liệu mẫu và dễ dàng chia sẻ kết quả với cộng đồng</p>""",
            """<ul class="lesson-bullet-list">
<li>Google Colab (viết tắt của Colaboratory) là một nền tảng lập trình trực tuyến miễn phí do Google phát triển. Với Google Colab, em có thể viết và chạy mã lập trình bằng ngôn ngữ Python ngay trên trình duyệt, mà không cần cài đặt phần mềm phức tạp. Google Colab hoạt động như một sổ tay điện tử gồm nhiều ô (cell), trong đó mỗi ô có thể chứa mã lệnh hoặc ghi chú giải thích. Em có thể chạy từng ô để xem ngay kết quả, rất thuận tiện cho việc học và thực hành lập trình.</li>
<li>Kaggle là một nền tảng trực tuyến thuộc Google, thường được biết đến như một cộng đồng Khoa học dữ liệu. Bên cạnh việc tổ chức các cuộc thi về dữ liệu, Kaggle cũng cung cấp môi trường lập trình trực tuyến để viết và chạy mã Python trong các sổ tay (notebook). Giao diện làm việc của Kaggle tương tự Google Colab, đồng thời cho phép truy cập nhanh đến các bộ dữ liệu mẫu và dễ dàng chia sẻ kết quả với cộng đồng.</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">Nhiệm vụ 1: Làm quen với giao diện Google Colab</p>\n<p class="lesson-p">Hướng dẫn:</p>',
            '<p class="lesson-p">Nhiệm vụ 1: Làm quen với giao diện Google Colab</p>\n'
            '<p class="lesson-p">Hướng dẫn:</p>\n'
            '<p class="lesson-p">(Hình ảnh và hướng dẫn sau đây sử dụng phần mềm Google Colab của Google.)</p>\n'
            '<p class="lesson-p">Bước 1. Mở ứng dụng Google Colab và tạo một sổ tay mới.</p>\n'
            '<ul class="lesson-bullet-list">\n'
            '<li>Mở trình duyệt, truy cập trang web: https://colab.research.google.com.</li>\n'
            '<li>Em cần đăng nhập bằng tài khoản Google cá nhân hoặc tài khoản được cung cấp.</li>\n'
            '<li>Sau khi đăng nhập, chọn nút + New notebook ở góc dưới bên phải để tạo một tệp Colab mới.</li>\n'
            '</ul>\n'
            '<p class="lesson-p">Bước 2. Làm quen với giao diện Google Colab.</p>\n'
            '<p class="lesson-p">Sau khi tạo mới sẽ có giao diện như sau:</p>',
        ),
        ("chạy mã, thêm chú thích,....,", "chạy mã, thêm chú thích,...;"),
        ('<p class="lesson-p">(7): Một ô viết mã</p>', '<p class="lesson-p">(7): Một ô viết mã.</p>'),
        (
            """<p class="lesson-p">3 Xin chào Google Colab khác nhau.</p>
<p class="lesson-p">Bước 3. Viết và chạy các lệnh ở các ô mã</p>
<p class="lesson-p">= 13) print/"Xin cho Google Colab")</p>
<p class="lesson-p">Nháy chọn nút hợp phím Shift mỗi ô mã và xem</p>
<p class="lesson-p">hoặc nhấn tố Enter để chạy kết quả (ví dụ</p>
<p class="lesson-p">print/"Tông của a và b ta:", a</p>
<p class="lesson-p">Đ Tổng của • và b la: 12</p>""",
            '<p class="lesson-p">Bước 3. Viết và chạy các lệnh ở các ô mã khác nhau.</p>\n'
            '<p class="lesson-p">Nháy chọn nút ▶ hoặc nhấn tổ hợp phím Shift + Enter để chạy mỗi ô mã và xem kết quả (ví dụ Hình 11.2).</p>',
        ),
        (
            """<figcaption class="figure-caption"><strong>Hình 11.2.</strong> Ví dụ kết quả chạy hai ô mã của Google Colab</figcaption>
</figure>
<figure class="lesson-figure-box figure-highlight">""",
            """<figcaption class="figure-caption"><strong>Hình 11.2.</strong> Ví dụ kết quả chạy hai ô mã của Google Colab</figcaption>
</figure>
<p class="lesson-p">Bước 4. Thêm ghi chú.</p>
<p class="lesson-p">Chọn ô + Text sau đó nhập nội dung ghi chú. Ví dụ: Đây là bài thực hành đầu tiên của em với Google Colab (Hình 11.3).</p>
<figure class="lesson-figure-box figure-highlight">""",
        ),
        (
            """<figcaption class="figure-caption"><strong>Hình 11.3.</strong> Giao diện code, kết quả, ghi chú trong Google Colab</figcaption>
</figure>

                    <figure class="lesson-figure-box figure-highlight">""",
            """<figcaption class="figure-caption"><strong>Hình 11.3.</strong> Giao diện code, kết quả, ghi chú trong Google Colab</figcaption>
</figure>
<p class="lesson-p">Bước 5. Lưu và chia sẻ.</p>
<ul class="lesson-bullet-list">
<li>Chọn File → Save a copy in Drive để lưu vào Google Drive cá nhân.</li>
<li>Chọn Share, sau đó cài đặt quyền truy cập nếu muốn chia sẻ với bạn bè hoặc thầy cô giáo.</li>
</ul>
<p class="lesson-p"><strong>Nhiệm vụ 2: Làm quen với giao diện Kaggle</strong></p>
<p class="lesson-p">Hướng dẫn:</p>
<p class="lesson-p">(Hình ảnh và hướng dẫn sau đây sử dụng phần mềm Kaggle của Google.)</p>
<p class="lesson-p">Bước 1. Truy cập Kaggle và tạo một sổ tay mới.</p>
<ul class="lesson-bullet-list">
<li>Mở trình duyệt, truy cập trang web: https://www.kaggle.com/code.</li>
<li>Sau khi đăng nhập, chọn nút + New notebook hoặc vào Create chọn New Notebook để tạo một sổ tay mới.</li>
</ul>
                    <figure class="lesson-figure-box figure-highlight">""",
        ),
        (
            """<p class="lesson-p">notebook 3024... an e Ven Hel</p>
<p class="lesson-p">This Python 3 environmet coes with aary helpfal analytian Libraries Laralle</p>
<p class="lesson-p">For eruple, reeleg thie (by eltching run of pressing airtiester) all list all Pales und</p>\n""",
            "",
        ),
        ("Giai thích các chủ thích trong Hình 11.5:", "Giải thích các chú thích trong Hình 11.5:"),
        (
            """<p class="lesson-p">(1): Thanh tiêu đề trên cùng và menu:

- notebookff3d2d4339: Tên mặc định của số tay bạn đang làm việc (có thể</p>
<p class="lesson-p">đổi tên).</p>
<ul class="lesson-bullet-list">
<li>Draft saved: Cho biết số tay của bạn đã được lưu tạm thời (chế độ nháp).

- Thanh bảng chọn:</li>
</ul>
<p class="lesson-p">+ File: Tạo mới, lưu, tải về, xoa,... một tệp số tay.</p>
<p class="lesson-p">+ Edit: Cắt, dẫn, xoá 6,....</p>
<p class="lesson-p">+ View: Hiển thị/ẩn một số thành phần trên giao diện,</p>""",
            """<p class="lesson-p">(1): Thanh tiêu đề trên cùng và menu:</p>
<ul class="lesson-bullet-list">
<li>notebookff3d2d4339: Tên mặc định của sổ tay bạn đang làm việc (có thể đổi tên).</li>
<li>Draft saved: Cho biết sổ tay của bạn đã được lưu tạm thời (chế độ nháp).</li>
<li>Thanh bảng chọn:</li>
</ul>
<p class="lesson-p">+ File: Tạo mới, lưu, tải về, xoá,... một tệp sổ tay.</p>
<p class="lesson-p">+ Edit: Cắt, dán, xoá ô,...</p>
<p class="lesson-p">+ View: Hiển thị/ẩn một số thành phần trên giao diện.</p>""",
        ),
        (
            """<p class="lesson-p">(2): Thanh công cụ cung cấp các nút chức năng để thao tác nhanh với các ô:

- Thêm ô mới.</p>
<ul class="lesson-bullet-list">
<li>Cắt, sao chép, dán, xóa ô.</li>
<li>Chạy toàn bộ sổ tay.</li>
<li>Chọn kiểu ô là Code (mã lệnh) hay Markdown (văn bản chú thích).</li>
<li>Hiển thị trạng thái của phiên làm việc (Session chưa được kích hoạt nếu chưa</li>
</ul>
<p class="lesson-p">chạy bất kì ô nào).</p>""",
            """<p class="lesson-p">(2): Thanh công cụ cung cấp các nút chức năng để thao tác nhanh với các ô:</p>
<ul class="lesson-bullet-list">
<li>Thêm ô mới.</li>
<li>Cắt, sao chép, dán, xoá ô.</li>
<li>Chạy toàn bộ sổ tay.</li>
<li>Chọn kiểu ô là Code (mã lệnh) hay Markdown (văn bản chú thích).</li>
<li>Hiển thị trạng thái của phiên làm việc (Session chưa được kích hoạt nếu chưa chạy bất kì ô nào).</li>
</ul>""",
        ),
        ('<p class="lesson-p">(4): Nút chạy một ô mã</p>', '<p class="lesson-p">(4): Nút chạy một ô mã.</p>'),
        ('<span class="h3-num">2.</span> Thực hành: AI chuyến đoạn văn thành giọng nói</h3>', '<span class="h3-num">2.</span> Thực hành: AI chuyển đoạn văn thành giọng nói</h3>'),
        (
            """<p class="lesson-p">Nhiệm vụ: Sử dụng Google Colab để thử nghiệm AI chuyển đoạn văn</p>
<p class="lesson-p">thành giọng nói.</p>
<p class="lesson-p">Hướng dẫn:</p>

                    <figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-11/hinh-11-6.webp" alt="Hình 11.6. Minh họa bài học 11.6" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 11.6.</strong> Minh họa bài học 11.6</figcaption>
</figure>""",
            """<p class="lesson-p">Nhiệm vụ: Sử dụng Google Colab để thử nghiệm AI chuyển đoạn văn thành giọng nói.</p>
<p class="lesson-p">Hướng dẫn:</p>
<p class="lesson-p">(Hình ảnh và hướng dẫn sau đây sử dụng phần mềm Google Colab của Google.)</p>
<p class="lesson-p">Bước 1. Mở Google Colab và tạo một sổ tay mới.</p>
<p class="lesson-p">Vào trang web: https://colab.research.google.com, sau đó đăng nhập bằng tài khoản Google hoặc tài khoản được cung cấp. Chọn nút + New notebook hoặc chọn Create → New Notebook để tạo một sổ tay mới.</p>
<p class="lesson-p">Bước 2. Tạo hai ô mã lệnh.</p>
<p class="lesson-p">– Ô mã 1: Cài đặt thư viện:</p>"""
            + BAI11_CODE_BLOCK1
            + """<p class="lesson-p">gTTS (Google Text-to-Speech) là một thư viện Python cho phép chuyển văn bản thành giọng nói bằng cách sử dụng dịch vụ đọc tự động của Google. Công cụ này hỗ trợ nhiều ngôn ngữ, trong đó có tiếng Việt và thường được dùng để tạo tệp âm thanh từ văn bản một cách nhanh chóng.</p>
<p class="lesson-p">– Ô mã 2: Thử nghiệm.</p>"""
            + BAI11_CODE_BLOCK2
            + """<p class="lesson-p">Bước 3. Chạy các ô mã.</p>
<p class="lesson-p">Kết quả khi chạy các ô mã ở Bước 2 như Hình 11.6.</p>
                    <figure class="lesson-figure-box figure-highlight">
    <img src="assets/images/lop-10/bai-11/hinh-11-6.webp" alt="Hình 11.6. Kết quả chuyển từ chữ sang giọng nói" class="lesson-img" loading="lazy" />
    <figcaption class="figure-caption"><strong>Hình 11.6.</strong> Kết quả chuyển từ chữ sang giọng nói</figcaption>
</figure>""",
        ),
        (
            """<p class="lesson-p">Gợi ý mở rộng:

- So sánh kết quả khi thay đổi ngôn ngữ (ví dụ lang='en' cho tiếng Anh).</p>
<ul class="lesson-bullet-list">
<li>Dùng đoạn văn dài hơn để tạo bài thuyết trình có giọng nói.</li>
<li>Thử nhiều giọng khác nhau với các thư viện năng cao (nếu quan tâm).</li>
</ul>
<p class="lesson-p">C</p>""",
            """<p class="lesson-p">Gợi ý mở rộng:</p>
<ul class="lesson-bullet-list">
<li>So sánh kết quả khi thay đổi ngôn ngữ (ví dụ lang='en' cho tiếng Anh).</li>
<li>Dùng đoạn văn dài hơn để tạo bài thuyết trình có giọng nói.</li>
<li>Thử nhiều giọng khác nhau với các thư viện nâng cao (nếu quan tâm).</li>
</ul>""",
        ),
        ("A. Trên máy tính không cần kết nổi Internet.", "A. Trên máy tính không cần kết nối Internet."),
        ('<p class="lesson-p">C. Trong tệp tài liệu Word,</p>', '<p class="lesson-p">C. Trong tệp tài liệu Word.</p>'),
        (
            '<p class="lesson-p">VẠN DỤNG</p>',
            '</div></section>' + section_open("apply-section", "sec-vận-dụng", "🚀", "VẬN DỤNG"),
        ),
        (
            """<p class="lesson-p">Nhiệm vụ: Sử dụng Google Colab và thư viện gTTS (thư viện Python cho phép chuyển văn bản thành giọng nói bằng cách sử dụng dịch vụ đọc tự động của</p>
<p class="lesson-p">Google) đề thực hiện đoạn giới thiệu bằng giọng nói cho hoạt động "Ngày hội học sinh sáng tạo".

Yêu cầu:</p>
<ul class="lesson-bullet-list">
<li>Viết một đoạn giới thiệu ngắn gọn (khoảng từ 4 đến 6 câu) giới thiệu về hoạt</li>
</ul>
<p class="lesson-p">động: tên sự kiện, thời gian, địa điểm, điểm thú vị và lời mời tham gia.</p>
<ul class="lesson-bullet-list">
<li>Sử dụng Google Colab để viết mã chuyển đoạn văn đó thành giọng nói (dùng</li>
</ul>
<p class="lesson-p">thư viện gTTS).</p>
<ul class="lesson-bullet-list">
<li>Ghi chú những điều em đã chỉnh sửa trong nội dung để đoạn âm thanh dễ nghe</li>
</ul>
<p class="lesson-p">(ví dụ: tách câu dài, dùng từ phố thông, tránh dấu câu khó đọc,....).</p>
<ul class="lesson-bullet-list">
<li>Chia sẻ âm thanh cho bạn cùng lớp nghe thử và ghi nhận phản hồi trước khi</li>
</ul>
<p class="lesson-p">hoàn thiện sản phẩm bàn giao cho Nhà trường.</p>""",
            """<p class="lesson-p">Nhiệm vụ: Sử dụng Google Colab và thư viện gTTS (thư viện Python cho phép chuyển văn bản thành giọng nói bằng cách sử dụng dịch vụ đọc tự động của Google) để thực hiện đoạn giới thiệu bằng giọng nói cho hoạt động "Ngày hội học sinh sáng tạo".</p>
<p class="lesson-p">Yêu cầu:</p>
<ul class="lesson-bullet-list">
<li>Viết một đoạn giới thiệu ngắn gọn (khoảng từ 4 đến 6 câu) giới thiệu về hoạt động: tên sự kiện, thời gian, địa điểm, điểm thú vị và lời mời tham gia.</li>
<li>Sử dụng Google Colab để viết mã chuyển đoạn văn đó thành giọng nói (dùng thư viện gTTS).</li>
<li>Ghi chú những điều em đã chỉnh sửa trong nội dung để đoạn âm thanh dễ nghe (ví dụ: tách câu dài, dùng từ phổ thông, tránh dấu câu khó đọc,...).</li>
<li>Chia sẻ âm thanh cho bạn cùng lớp nghe thử và ghi nhận phản hồi trước khi hoàn thiện sản phẩm bàn giao cho Nhà trường.</li>
</ul>""",
        ),
    ],
    "bai-12-bai-tap-du-an": [
        ("kết hợp LLM và công cụ Ai tạo ảnh.", "kết hợp LLM và công cụ AI tạo ảnh."),
        ("những yếu tố minh hoa nào cho một sản phẩm dự án?", "những yếu tố minh hoạ nào cho một sản phẩm dự án?"),
        ('<span class="h3-num">1.</span> Quy trình sử dụng Ai tạo sinh để hỗ trợ sáng tạo sản phẩm cá nhân</h3>', '<span class="h3-num">1.</span> Quy trình sử dụng AI tạo sinh để hỗ trợ sáng tạo sản phẩm cá nhân</h3>'),
        ("theo một quy trình đàm bảo đạt được", "theo một quy trình đảm bảo đạt được"),
        (
            '<p class="lesson-p">Ví dụ: Nhóm ban An xác định mục tiêu là giới thiệu cuộc thi tranh biện và gây hứng thú cho học sinh loàn khối. Các bạn thống nhất tạo các nội dung như:\n\nkhẩu hiệu, bài đáng mạng xã hội, kịch bản video,....</p>',
            '<p class="lesson-p">Ví dụ: Nhóm bạn An xác định mục tiêu là giới thiệu cuộc thi tranh biện và gây hứng thú cho học sinh toàn khối. Các bạn thống nhất tạo các nội dung như: khẩu hiệu, bài đăng mạng xã hội, kịch bản video,...</p>',
        ),
        ("hỗ trợ em hiệu quả trong sáng tạo</p>", "hỗ trợ em hiệu quả trong sáng tạo.</p>"),
        (
            '<p class="lesson-p">Ví dụ: Sau khi xác định mục tiêu, nhóm bạn An nhập prompt cụ thể: "Viết khẩu hiệu truyền cảm hừng cho cuộc thi tranh biên với chủ đề: Trí tuệ nhân tạo có làm</p>\n'
            '<p class="lesson-p">giảm khả năng sáng tạo của học sinh?". Nhóm tiếp tục yêu cầu gợi ý poster, tiêu đề, mô tả ngắn hấp dẫn. Các phàn hồi được đánh giá và lựa chọn theo tiêu</p>\n'
            '<p class="lesson-p">chí gần gũi với học sinh.</p>',
            '<p class="lesson-p">Ví dụ: Sau khi xác định mục tiêu, nhóm bạn An nhập prompt cụ thể: "Viết khẩu hiệu truyền cảm hứng cho cuộc thi tranh biện với chủ đề: Trí tuệ nhân tạo có làm giảm khả năng sáng tạo của học sinh?". Nhóm tiếp tục yêu cầu gợi ý poster, tiêu đề, mô tả ngắn hấp dẫn. Các phản hồi được đánh giá và lựa chọn theo tiêu chí gần gũi với học sinh.</p>',
        ),
        ("cần thiết để đàm bảo nội dung Ai tạo ra", "cần thiết để đảm bảo nội dung AI tạo ra"),
        ("giúp em phát triển kĩ nắng tư duy,", "giúp em phát triển kĩ năng tư duy,"),
        ("đánh giá phần hồi và kể chuyện", "đánh giá phản hồi và kể chuyện"),
        ("em gặp phiên bằn tương lai của chính minh từ tình huống sau:", "em gặp phiên bản tương lai của chính mình từ tình huống sau:"),
        ("Giác mơ ấy khiến Linh nhận ra", "Giấc mơ ấy khiến Linh nhận ra"),
        ("Để thực hiện truyên tranh,", "Để thực hiện truyện tranh,"),
        (
            """<ul class="lesson-bullet-list">
<li>Sử dụng Gemini (mô hình ngôn ngữ lớn - LLM) để xây dựng nội dung, viết lời</li>
</ul>
<p class="lesson-p">thoại, mô tả từng cảnh và tạo prompt phù hợp cho công cụ AI tạo ảnh.</p>
<ul class="lesson-bullet-list">
<li>Sử dụng ChatGPT để tạo hình ảnh minh hoa cho từng trang truyện.</li>
</ul>""",
            """<ul class="lesson-bullet-list">
<li>Sử dụng Gemini (mô hình ngôn ngữ lớn - LLM) để xây dựng nội dung, viết lời thoại, mô tả từng cảnh và tạo prompt phù hợp cho công cụ AI tạo ảnh.</li>
<li>Sử dụng ChatGPT để tạo hình ảnh minh hoạ cho từng trang truyện.</li>
</ul>""",
        ),
        (
            '<p class="lesson-p">Cung cấp thông tin để AI tạo sinh tạo bố cục truyện tranh từ ý tưởng của Linh.\n\nPrompt tham khảo:</p>',
            '<p class="lesson-p">Cung cấp thông tin để AI tạo sinh tạo bố cục truyện tranh từ ý tưởng của Linh.</p>\n<p class="lesson-p">Prompt tham khảo:</p>',
        ),
        (
            '<p class="lesson-p">Tạo một truyện tranh kĩ thuật số gồm 5 trang, kể lại hành trình nhận thức của một nữ sinh trung học về vai trò của AI, nhấn mạnh thông điệp: "AI không phải là mói</p>\n'
            '<p class="lesson-p">đe doa, mà là công cụ hỗ trợ. Quan trọng là con người cần chủ động học hỏi, thích nghì để làm chủ công nghệ."</p>',
            '<p class="lesson-p">Tạo một truyện tranh kĩ thuật số gồm 5 trang, kể lại hành trình nhận thức của một nữ sinh trung học về vai trò của AI, nhấn mạnh thông điệp: "AI không phải là mối đe doạ, mà là công cụ hỗ trợ. Quan trọng là con người cần chủ động học hỏi, thích nghi để làm chủ công nghệ."</p>',
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Nhân vật chính là Linh, nữ sinh lớp 10 người Việt Nam, tóc dài buộc gọn phía</li>
</ul>
<p class="lesson-p">sau, mặc đông phục học sinh hiện đại.</p>
<ul class="lesson-bullet-list">
<li>Linh cảm thấy mông lung về tương lai và có nhiều băn khoăn về tác động của</li>
</ul>
<p class="lesson-p">AI đổi với nghề nghiệp, học tập.</p>
<ul class="lesson-bullet-list">
<li>Trong một giấc mơ, Linh thấy minh lạc vào thế giới nơi công nghệ và AI hiện</li>
</ul>
<p class="lesson-p">diện khắp nơi.</p>
<ul class="lesson-bullet-list">
<li>Cô gặp chính minh trong tương lai - một người tự tin, đang làm việc, sáng tạo</li>
</ul>
<p class="lesson-p">cùng AI.</p>
<ul class="lesson-bullet-list">
<li>Cuộc gặp gỡ giúp Linh nhận ra rằng Ai không thay thế con người, mà cần được</li>
</ul>
<p class="lesson-p">con người làm chủ, định hướng.</p>
<ul class="lesson-bullet-list">
<li>Khi tỉnh dậy, Linh quyết định bắt đầu hành trình mới, kể lại giấc mơ ấy bằng một</li>
</ul>
<p class="lesson-p">truyện tranh bằng cách kết hợp công nghệ.</p>""",
            """<ul class="lesson-bullet-list">
<li>Nhân vật chính là Linh, nữ sinh lớp 10 người Việt Nam, tóc dài buộc gọn phía sau, mặc đồng phục học sinh hiện đại.</li>
<li>Linh cảm thấy mông lung về tương lai và có nhiều băn khoăn về tác động của AI đối với nghề nghiệp, học tập.</li>
<li>Trong một giấc mơ, Linh thấy mình lạc vào thế giới nơi công nghệ và AI hiện diện khắp nơi.</li>
<li>Cô gặp chính mình trong tương lai – một người tự tin, đang làm việc, sáng tạo cùng AI.</li>
<li>Cuộc gặp gỡ giúp Linh nhận ra rằng AI không thay thế con người, mà cần được con người làm chủ, định hướng.</li>
<li>Khi tỉnh dậy, Linh quyết định bắt đầu hành trình mới, kể lại giấc mơ ấy bằng một truyện tranh bằng cách kết hợp công nghệ.</li>
</ul>""",
        ),
        ('<p class="lesson-p">Thông tin bổ sung.</p>', '<p class="lesson-p">Thông tin bổ sung:</p>'),
        ("em cần điều chính lại prompt.", "em cần điều chỉnh lại prompt."),
        (
            '<ul class="lesson-bullet-list">\n<li>Tạo hình anh từ prompt đã hoàn chỉnh: Em sử dụng công cụ tạo ảnh bằng AI</li>\n</ul>\n<p class="lesson-p">để tạo hình ảnh dựa trên prompt vừa tạo.</p>',
            '<ul class="lesson-bullet-list">\n<li>Tạo hình ảnh từ prompt đã hoàn chỉnh: Em sử dụng công cụ tạo ảnh bằng AI để tạo hình ảnh dựa trên prompt vừa tạo.</li>\n</ul>',
        ),
        (
            """<p class="lesson-p">+ Nếu hình ảnh tạo ra chưa thể hiện đúng đặc điểm nhân vật hoặc chưa phủ</p>
<p class="lesson-p">hợp với nội dung truyện, em cần quay lại và chỉnh sửa prompt.</p>
<p class="lesson-p">+ Ví dụ: Trong truyện, bạn Linh có mái tóc đen, dài và thường buộc tóc lên.</p>
<p class="lesson-p">Nếu AI tạo ra hình ảnh bạn Linh với tóc thả, em cần bổ sung mỏ tả chi tiết vào prompt để đảm bảo hình ảnh đúng với nhân vật.

- Tạo lại hình ảnh (nếu cần):</p>
<p class="lesson-p">Sau khi điều chỉnh prompt, em tiếp tục tạo lại hình ảnh. Khi đã có kết quả ưng ý, em chuyển sang thực hiện hình ảnh cho trang tiếp theo (trang 2). Em có thể để tiếp tục điều chỉnh đến khi đạt được kết quả mong muốn.</p>""",
            """<p class="lesson-p">+ Nếu hình ảnh tạo ra chưa thể hiện đúng đặc điểm nhân vật hoặc chưa phù hợp với nội dung truyện, em cần quay lại và chỉnh sửa prompt.</p>
<p class="lesson-p">+ Ví dụ: Trong truyện, bạn Linh có mái tóc đen, dài và thường buộc tóc lên. Nếu AI tạo ra hình ảnh bạn Linh với tóc thả, em cần bổ sung mô tả chi tiết vào prompt để đảm bảo hình ảnh đúng với nhân vật.</p>
<ul class="lesson-bullet-list">
<li>Tạo lại hình ảnh (nếu cần):</li>
</ul>
<p class="lesson-p">Sau khi điều chỉnh prompt, em tiếp tục tạo lại hình ảnh. Khi đã có kết quả ưng ý, em chuyển sang thực hiện hình ảnh cho trang tiếp theo (trang 2). Em có thể tiếp tục điều chỉnh đến khi đạt được kết quả mong muốn.</p>""",
        ),
        ("Bước 3. Tương tác có định hướng với AI và kiếm tra,", "Bước 3. Tương tác có định hướng với AI và kiểm tra,"),
        (
            """<p class="lesson-p">+ Em sử dụng ChatGPT để tạo prompt phù hợp với nội dung của truyện tranh,</p>
<p class="lesson-p">nhằm tạo ra hình ảnh minh hoa cho trang thứ hai.</p>
<p class="lesson-p">+ Nếu kết quả trà về chưa phù hợp với nội dung hoặc chưa phần ánh đúng ý</p>
<p class="lesson-p">tưởng truyện, em cần điều chỉnh lại prompt.</p>
<p class="lesson-p">+ Ví dụ trong trang 2 em cần có nhiều khung thay vì 1 ảnh như trang 1, em cần</p>
<p class="lesson-p">bồ sung số lượng khung và chi tiết các khung nếu muốn.</p>
<p class="lesson-p">+ Khi cảm thấy prompt đã rõ ràng, đày đù và hợp lI, em chuyển sang bước tạo</p>
<p class="lesson-p">hình ảnh.</p>""",
            """<p class="lesson-p">+ Em sử dụng ChatGPT để tạo prompt phù hợp với nội dung của truyện tranh, nhằm tạo ra hình ảnh minh hoạ cho trang thứ hai.</p>
<p class="lesson-p">+ Nếu kết quả trả về chưa phù hợp với nội dung hoặc chưa phản ánh đúng ý tưởng truyện, em cần điều chỉnh lại prompt.</p>
<p class="lesson-p">+ Ví dụ trong trang 2 em cần có nhiều khung thay vì 1 ảnh như trang 1, em cần bổ sung số lượng khung và chi tiết các khung nếu muốn.</p>
<p class="lesson-p">+ Khi cảm thấy prompt đã rõ ràng, đầy đủ và hợp lí, em chuyển sang bước tạo hình ảnh.</p>""",
        ),
        ("<li>Tạo hình ảnh từ prompt đã hoàn chinh:</li>", "<li>Tạo hình ảnh từ prompt đã hoàn chỉnh:</li>"),
        ("trang phục, kiều tóc, sắc thái khuôn mặt", "trang phục, kiểu tóc, sắc thái khuôn mặt"),
        ('<p class="lesson-p">Chao em, Linh của</p>\n<p class="lesson-p">ngày hôm qua!</p>\n', ""),
        (
            """<ul class="lesson-bullet-list">
<li>Mô tả chi tiết nhân vật chính và nhân vật phụ: đầm báo trang phục, kiểu tóc,</li>
</ul>
<p class="lesson-p">biểu cảm và tư thế giống với hình ảnh ở các trang 1 và 2, chiều cao của hai nhân vật cần phù hợp.</p>
<ul class="lesson-bullet-list">
<li>Bồi cảnh truyện cần phù hợp với nội dung của trang 3, có thể là không gian làm</li>
</ul>
<p class="lesson-p">việc, màu sắc tổng thể</p>
<ul class="lesson-bullet-list">
<li>Bổ sung lời thoại, hành động hoặc nét mặt để tăng tính biều cảm cho</li>
</ul>
<p class="lesson-p">nhân vật.</p>
<ul class="lesson-bullet-list">
<li>Lựa chọn phong cách hình ảnh phù hợp và nhất quán với loàn bộ truyện.</li>
</ul>""",
            """<ul class="lesson-bullet-list">
<li>Mô tả chi tiết nhân vật chính và nhân vật phụ: đảm bảo trang phục, kiểu tóc, biểu cảm và tư thế giống với hình ảnh ở các trang 1 và 2, chiều cao của hai nhân vật cần phù hợp.</li>
<li>Bối cảnh truyện cần phù hợp với nội dung của trang 3, có thể là không gian làm việc, màu sắc tổng thể.</li>
<li>Bổ sung lời thoại, hành động hoặc nét mặt để tăng tính biểu cảm cho nhân vật.</li>
<li>Lựa chọn phong cách hình ảnh phù hợp và nhất quán với toàn bộ truyện.</li>
</ul>""",
        ),
        (
            """<p class="lesson-p">AI không làm thay tát cà.

nhưng nếu em hiểu và làm chủ nó.</p>
<p class="lesson-p">em sẽ tạo ra điều tuyệt với.</p>
<p class="lesson-p">AI</p>\n""",
            "",
        ),
        (
            """<ul class="lesson-bullet-list">
<li>Giữ sư nhất quản về tạo hình của các nhân vật với ba trang trước, bao gồm</li>
</ul>
<p class="lesson-p">trang phục, kiểu tóc, nét mặt và tư thế.</p>
<ul class="lesson-bullet-list">
<li>Trạng 4 thường là cao trào của câu chuyện. vi vậy dần trể hiện rõ cảm xi..</li>
</ul>
<p class="lesson-p">hanh. động hoặc tương lắc giữa các nhận. rà nhằm truyền lải nội dung rrfi.</p>
<p class="lesson-p">cách rõ ràng và sinh động.</p>
<ul class="lesson-bullet-list">
<li>Lựa chọn bố cục hình ảnh phù hợp để thể hiện được mạch truyện một cách rõ ràng,</li>
</ul>
<p class="lesson-p">Diễn biến: Có thể kết hợp thêm lời thoại, biểu cảm nhân vật để tăng tính thuyết phục..</p>
<ul class="lesson-bullet-list">
<li>Nếu xuất hiện thêm nhân vật phụ hoặc yếu tố mới, em cần mà tà rõ ràng rong</li>
</ul>
<p class="lesson-p">prompt để đảm bảo hình ảnh chính xác và hài hòa với tổng thể câu chuyện</p>
<p class="lesson-p">.°</p>
<p class="lesson-p">1%., ....4?. Trang 4 trong câu chuyện của bạn Linh</p>
<p class="lesson-p">Bước 6. Tương tác với AI và kiểm tra, hiệu chỉnh kết quả tạo ảnh</p>
<p class="lesson-p">Trang 5 là trang rét "i'n? :j4 tanh, thường mang tính tổng kết, truyền thông điệp hoặc thể hig 1!... 2. ién si, truyện. Em tiếp túc thực hiện các bước tương tự như ở những tá !,: 1'r. "rg tren chú ý các điềm sau:</p>
<ul class="lesson-bullet-list">
<li>Duy tri su th !; "%i vh, 1, einin, bài cánh và phong cách hình ảnh với toàn bộ</li>
</ul>
<p class="lesson-p">thuyện tranh.</p>
<ul class="lesson-bullet-list">
<li>Nếu có kới tạc a rệt ". 12.1134, thông điệp, cần bổ sung vào prompt để Ai tạo ra</li>
</ul>
<p class="lesson-p">hình ảnh phi irr</p>
<ul class="lesson-bullet-list">
<li>Hình ánh kến ríx, "k7 T4n :uon rở cầm xúc tích cục (vui về, tự tin, gắn kết,...)</li>
</ul>
<p class="lesson-p">đh gay an turris in sín, ig ri vem hiểu rõ thông điệp của truyện.</p>""",
            """<ul class="lesson-bullet-list">
<li>Giữ sự nhất quán về tạo hình của các nhân vật với ba trang trước, bao gồm trang phục, kiểu tóc, nét mặt và tư thế.</li>
<li>Trang 4 thường là cao trào của câu chuyện, vì vậy cần thể hiện rõ cảm xúc, hành động hoặc tương tác giữa các nhân vật nhằm truyền tải nội dung một cách rõ ràng và sinh động.</li>
<li>Lựa chọn bố cục hình ảnh phù hợp để thể hiện được mạch truyện một cách dễ hiểu, có thể kết hợp thêm lời thoại hoặc biểu cảm nhân vật để tăng tính thuyết phục.</li>
<li>Nếu xuất hiện thêm nhân vật phụ hoặc yếu tố mới, em cần mô tả rõ ràng trong prompt để đảm bảo hình ảnh chính xác và hài hoà với tổng thể câu chuyện.</li>
</ul>
<p class="lesson-p">Bước 6. Tương tác có định hướng với AI và kiểm tra, hiệu chỉnh kết quả tạo ảnh trang 5.</p>
<p class="lesson-p">Trang 5 là trang kết của truyện tranh, thường mang tính tổng kết, truyền thông điệp hoặc thể hiện kết quả của câu chuyện. Em tiếp tục thực hiện các bước tương tự như ở những trang trước, đồng thời chú ý các điểm sau:</p>
<ul class="lesson-bullet-list">
<li>Duy trì sự thống nhất về tạo hình, bối cảnh và phong cách hình ảnh với toàn bộ truyện tranh.</li>
<li>Nếu có lời thoại, lời chúc hoặc thông điệp, cần bổ sung vào prompt để AI tạo ra hình ảnh phù hợp.</li>
<li>Hình ảnh kết thúc nên thể hiện rõ cảm xúc tích cực (vui vẻ, tự tin, gắn kết,...) để gây ấn tượng tốt và giúp người xem hiểu rõ thông điệp của truyện.</li>
</ul>""",
        ),
        ("trong cầu chuyện của ban Linh", "trong câu chuyện của bạn Linh"),
        ("Bước 7. Biên lập lời dẫn cho truyện", "Bước 7. Biên tập lời dẫn cho truyện."),
        (
            "Sau khi đã hoàn thành các hình ánh minh hoa cho các trang truyện, sm tiến hành biên lập phần lời dẫn đế bổ sung cho mỗi khung truyện, giúp càu chuyện trà nên mạch lạc, dể hiếu và truyền tải được thông điệp rõ ràng.",
            "Sau khi đã hoàn thành các hình ảnh minh hoạ cho các trang truyện, em tiến hành biên tập phần lời dẫn để bổ sung cho mỗi khung truyện, giúp câu chuyện trở nên mạch lạc, dễ hiểu và truyền tải được thông điệp rõ ràng.",
        ),
        ("Một số lưu ý khi biên lập lời dẫn:", "Một số lưu ý khi biên tập lời dẫn:"),
        (
            """<ul class="lesson-bullet-list">
<li>Lời dẫn cần ngắn gọn, rõ ràng và phú hợp với nội dung lừng khung hình. Em</li>
</ul>
<p class="lesson-p">có thể viết dưới dạng lời kế, lời thoại nhân vật hoặc chủ thích (nếu cần)</p>
<ul class="lesson-bullet-list">
<li>Giữ đúng giọng điệu phù hợp với truyện. Ví dụ, nếu truyện mang tính nhẹ</li>
</ul>
<p class="lesson-p">nhàng, cảm xúc thì lời dẫn nên mềm mại, gần gũi; nếu truyện hai hước thi lời dẫn có thể đi đơm, sinh động</p>
<ul class="lesson-bullet-list">
<li>Lới dẫn cần bảm sát hành động, cảm xúc của nhân vật va mạch truyền. Không</li>
</ul>
<p class="lesson-p">nên viết quá dài hoặc vượt quá những gì hình ảnh đang thể hiện</p>
<ul class="lesson-bullet-list">
<li>Đảm bảo lời dẫn giữa các trang có sự liên kết. Em nên dọc lái toan bộ truyện</li>
</ul>
<p class="lesson-p">để kiểm tra xem các đoạn chuyển cảnh, lới thoại và kết thúc có trội cháy, hợp lí chưa.</p>
<ul class="lesson-bullet-list">
<li>Sử dụng ngôn ngữ trong sáng, đễ hiểu, phú hợp với lửa luổi học sinh. Tránh</li>
</ul>
<p class="lesson-p">dũng từ ngữ quá phức tạp hoặc mang tính suy luận cao.</p>
<p class="lesson-p">Sâu khi biên tập xong, em có thể người khác đọc lại toàn bộ lới dẫn để góp ý.

chỉnh sửa vả hoàn thiện truyện tranh.</p>""",
            """<ul class="lesson-bullet-list">
<li>Lời dẫn cần ngắn gọn, rõ ràng và phù hợp với nội dung từng khung hình. Em có thể viết dưới dạng lời kể, lời thoại nhân vật hoặc chú thích (nếu cần).</li>
<li>Giữ đúng giọng điệu phù hợp với truyện. Ví dụ, nếu truyện mang tính nhẹ nhàng, cảm xúc thì lời dẫn nên mềm mại, gần gũi; nếu truyện hài hước thì lời dẫn có thể dí dỏm, sinh động.</li>
<li>Lời dẫn cần bám sát hành động, cảm xúc của nhân vật và mạch truyện. Không nên viết quá dài hoặc vượt quá những gì hình ảnh đang thể hiện.</li>
<li>Đảm bảo lời dẫn giữa các trang có sự liên kết. Em nên đọc lại toàn bộ truyện để kiểm tra xem các đoạn chuyển cảnh, lời thoại và kết thúc có trôi chảy, hợp lí chưa.</li>
<li>Sử dụng ngôn ngữ trong sáng, dễ hiểu, phù hợp với lứa tuổi học sinh. Tránh dùng từ ngữ quá phức tạp hoặc mang tính suy luận cao.</li>
</ul>
<p class="lesson-p">Sau khi biên tập xong, em có thể nhờ người khác đọc lại toàn bộ lời dẫn để góp ý, chỉnh sửa và hoàn thiện truyện tranh.</p>""",
        ),
        (
            '<p class="lesson-p">Để thực hiện một sản phẩm sáng tạo có sử dụng AI, em cần xác định rõ mục tiêu, tương tác có định hướng với AI, kiểm tra và chỉnh sửa kết quả đầu ra, đảm bảo đạo đức khi sử dụng</p>\n'
            '<p class="lesson-p">công cụ và phát triển kì năng cá nhân trong quá trình thực hiện.</p>',
            '<p class="lesson-p">Để thực hiện một sản phẩm sáng tạo có sử dụng AI, em cần xác định rõ mục tiêu, tương tác có định hướng với AI, kiểm tra và chỉnh sửa kết quả đầu ra, đảm bảo đạo đức khi sử dụng công cụ và phát triển kĩ năng cá nhân trong quá trình thực hiện.</p>',
        ),
        ('như "một cô gái" đề AI linh hoạt hơn.', 'như "một cô gái" để AI linh hoạt hơn.'),
        (
            '<p class="lesson-p">B. Thêm mô tả rõ ràng về vị trí chữ trong prompt, ví dụ: "không đặt chữ trên áo</p>',
            '<p class="lesson-p">B. Thêm mô tả rõ ràng về vị trí chữ trong prompt, ví dụ: "không đặt chữ trên áo nhân vật".</p>',
        ),
        ("C. Xoa prompt cũ và viết lại hoàn toàn prompt mới.", "C. Xoá prompt cũ và viết lại hoàn toàn prompt mới."),
        (
            """<ul class="lesson-bullet-list">
<li>Có cốt truyện rõ ràng, truyền cảm hứng</li>
</ul>
<p class="lesson-p">tích cực;</p>
<p class="lesson-p">A</p>
<ul class="lesson-bullet-list">
<li>Tối thiểu 3 trang, tối đa 5 (rang;</li>
<li>Gửi kèm lời thoại hoặc lời dẫn ngắn cho</li>
</ul>
<p class="lesson-p">mỗi trang.</p>""",
            """<ul class="lesson-bullet-list">
<li>Có cốt truyện rõ ràng, truyền cảm hứng tích cực;</li>
<li>Tối thiểu 3 trang, tối đa 5 trang;</li>
<li>Gửi kèm lời thoại hoặc lời dẫn ngắn cho mỗi trang.</li>
</ul>""",
        ),
    ],
    "bang-giai-thich-thuat-ngu": [
        (
            """<p class="lesson-p">BẢNG GIẢI THÍCH THUẬT NGƯ</p>
<p class="lesson-p">Thuật ngữ Giải thích</p>
<p class="lesson-p">Trang</p>
<p class="lesson-p">AI tạo sinh (Generative AI)</p>
<p class="lesson-p">Loại trí tuệ nhân tạo có khả năng tạo ra nội dung</p>
<p class="lesson-p">mới dạng văn bản, hình ảnh, âm thanh, video, mã chương trình,...</p>
<p class="lesson-p">Bịa đặt (Hallucination)</p>
<p class="lesson-p">Hiện lượng AI tạo sinh tạo ra thông tin sai lệch nhưng có thể thấy đúng hoặc hợp lí, dù không có dữ liệu hỗ trợ.</p>
<p class="lesson-p">Sử dụng AI để tạo ra hình ảnh, video hoặc âm thanh, khiến người xem tưởng rắng ai đó đã nói hoặc làm điều gì đó mà ho thực tế chưa từng làm.</p>
<p class="lesson-p">Giả mao (Deepfake)</p>
<p class="lesson-p">Mạng nơ-ron nhân tạo</p>
<p class="lesson-p">Hệ thống phần mềm mô phỏng cách hoạt động của não người, gồm nhiều "nút" (gọi là no-ron nhân tạo) kết nối với nhau.</p>
<p class="lesson-p">Một loại mạng nơ-ron nhân tạo, được thiết kể chủ yếu đề xử lí hình ảnh. Nó có thể tự động lim ra các đặc điểm thông tin như hình dạng, màu sắc trong ảnh, hoặc âm thanh trong dữ liệu giọng nói, bằng cách xử lí dữ liệu có cấu trúc dạng lưới hoặc chuối.</p>
<p class="lesson-p">Mạng nơ-ron tích chập (CNN)</p>
<p class="lesson-p">AI đưa ra kết quả không công bằng, nghiêng về một phía, do dữ liệu mà nó học bị thiếu cản bằng hoặc sai lệch.</p>
<p class="lesson-p">Thiên vị (Bias)</p>
<p class="lesson-p">Trí tuệ nhân tạo (AI - Artificial Intelligence)</p>
<p class="lesson-p">Ngành khoa học và công nghệ giúp máy móc có thể suy nghĩ, học tập và giải quyết vấn đề giống con người.</p>
<p class="lesson-p">Lĩnh vực của trí tuệ nhân tạo giúp máy tính hiểu,</p>
<p class="lesson-p">phân tích và tạo ra ngôn ngữ của con người, như tiếng Việt hay tiếng Anh. Nhờ NLP, máy có thể</p>
<p class="lesson-p">x</p>
<p class="lesson-p">Xử lí ngôn ngữ tự nhiên (NLP)</p>
<p class="lesson-p">dịch văn bản, trả lời câu hỏi, kiểm tra chính tả hay trò chuyên với người dùng như ChatGPT.</p>""",
            GLOSSARY_CLEAN_BODY,
        ),
    ],
    "thong-tin-xuat-ban-bia-sau": [
        (
            """<p class="lesson-p">Trân trọng cảm m các tác giả có tác phẩm,</p>
<p class="lesson-p">tự liệu được sử dụng, trích dẫn</p>
<p class="lesson-p">trong cuốn sách nùy.</p>""",
            '<p class="lesson-p">Trân trọng cảm ơn các tác giả có tác phẩm, tư liệu được sử dụng, trích dẫn trong cuốn sách này.</p>',
        ),
        ("Chịu trách nhiệm nội dụng:", "Chịu trách nhiệm nội dung:"),
        ("Tổng biên tập PHẠM VINH THAI", "Tổng biên tập PHẠM VĨNH THÁI"),
        ("Phó Tông biên tập VŨ TRUNG CHINH", "Phó Tổng biên tập VŨ TRUNG CHÍNH"),
        (
            '<p class="lesson-p">Phó Tổng biên lập - Hoạ sĩ trường ĐINH GIA LÊ Tổng Giám đốc Công ty CP Đầu tư và Phát triển Giáo dục Phương Nam LE PHƯƠNG MAI</p>',
            '<p class="lesson-p">Phó Tổng biên tập – Hoạ sĩ trưởng ĐINH GIA LÊ</p>\n<p class="lesson-p">Tổng Giám đốc Công ty CP Đầu tư và Phát triển Giáo dục Phương Nam LÊ PHƯƠNG MAI</p>',
        ),
        (
            '<p class="lesson-p">Biến lập mĩ thuật, thiết kế sách, bla và minh hoạ: ĐẠNG DUY TIỀN - NGUYỄN THẾ PHI Sửa bản in: LƯU THẾ SƠN - NGUYỄN THANH GIẢNG</p>',
            '<p class="lesson-p">Biên tập mĩ thuật, thiết kế sách, bìa và minh hoạ: ĐẶNG DUY TIẾN – NGUYỄN THẾ PHI</p>\n<p class="lesson-p">Sửa bản in: LƯU THẾ SƠN – NGUYỄN THANH GIANG</p>',
        ),
        ("quyền tác giá.", "quyền tác giả."),
        ("lưu trữ, chuyến thể dưới bất kì hình thức nào", "lưu trữ, chuyển thể dưới bất kì hình thức nào"),
        ("khó 19 x 26,5 cm", "khổ 19 x 26,5 cm"),
        (
            '<p class="lesson-p">Đơn vị in : Công ty Có phần In & Bao bì Đồng Tháp Địa chỉ : 212 Lê Lợi, Phường Sa Đéc, Tinh Đồng Tháp Số ĐKXB : 416-2026/CXBIPH/34-168/GD</p>\n'
            '<p class="lesson-p">Số QĐXB : 118/QĐXB-GD ngày 11 tháng 02 năm 2026 In xong và nộp lưu chiều tháng 03 năm 2026</p>\n'
            '<p class="lesson-p">Mã số ISBN : 978-604-0-46630-3</p>\n'
            '<p class="lesson-p">TAPIANKO GA CE MANAO</p>\n'
            '<p class="lesson-p">ISBN 978-604-0-46630-3</p>\n'
            '<p class="lesson-p">VÀ PHÁT TRIỂN GIÁO DỤC PHƯƠNG NAM SEDIDCO 9 786040 466303 Giá: 40.000đ</p>\n'
            '<p class="lesson-p">CÔNG TY CỔ PHÁN ĐẦU TƯ</p>',
            '<p class="lesson-p">Đơn vị in: Công ty Cổ phần In &amp; Bao bì Đồng Tháp</p>\n'
            '<p class="lesson-p">Địa chỉ: 212 Lê Lợi, Phường Sa Đéc, Tỉnh Đồng Tháp</p>\n'
            '<p class="lesson-p">Số ĐKXB: 416-2026/CXBIPH/34-168/GD</p>\n'
            '<p class="lesson-p">Số QĐXB: 118/QĐXB-GD ngày 11 tháng 02 năm 2026</p>\n'
            '<p class="lesson-p">In xong và nộp lưu chiểu tháng 03 năm 2026</p>\n'
            '<p class="lesson-p">Mã số ISBN: 978-604-0-46630-3</p>\n'
            '<p class="lesson-p">CÔNG TY CỔ PHẦN ĐẦU TƯ VÀ PHÁT TRIỂN GIÁO DỤC PHƯƠNG NAM – SEDIDCO</p>\n'
            '<p class="lesson-p">ISBN 978-604-0-46630-3 | 9 786040 466303 | Giá: 40.000đ</p>',
        ),
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
    lessons_path = DATA_DIR / "lessons-lop-10.json"
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
                unmatched.append((les_id, idx, old[:90]))
            else:
                content = content.replace(old, new)
                total_applied += cnt

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

    books_path = DATA_DIR / "books.json"
    books_data = json.loads(books_path.read_text(encoding="utf-8"))
    books_list = books_data.get("books", books_data)
    updated_toc_items = 0
    for bk in books_list:
        if bk["id"] == "lop-10":
            for grp in bk.get("toc", []):
                for it in grp.get("items", []):
                    if it.get("id") in summaries_by_id:
                        it["summary"] = summaries_by_id[it["id"]]
                        updated_toc_items += 1
    books_path.write_text(json.dumps(books_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {updated_toc_items} summaries in {books_path}")

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
    search_path = DATA_DIR / "search-lop-10.json"
    search_path.write_text(json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt {search_path} with {len(search_data)} entries.")


if __name__ == "__main__":
    main()
