# Tủ Sách Giáo Khoa Trí Tuệ Nhân Tạo THPT (Lớp 10 – 11 – 12)

🌐 **Bản web trực tuyến**: https://sach-tri-tue-nhan-tao.vercel.app  
📂 **Mã nguồn GitHub**: https://github.com/nongchuchuyen2021-svg/sach-tri-tue-nhan-tao

Website đọc sách giáo khoa điện tử **toàn văn văn bản HTML** cho bộ 3 cuốn sách **Trí tuệ nhân tạo** cấp Trung học phổ thông (Lớp 10, Lớp 11, Lớp 12) — Nhà xuất bản Giáo dục Việt Nam (Bộ Giáo dục và Đào tạo).

---

## 🌟 Tính năng nổi bật

### 1. Trích xuất toàn văn chữ (Text-First Reading)
- Không chỉ là hình ảnh lật trang thông thường: toàn bộ nội dung sách đã được trích xuất và cấu trúc hóa thành văn bản HTML ngữ nghĩa cao cấp.
- Cấu trúc chuẩn từng bài học theo chương trình phổ thông:
  - 🎯 **Mục tiêu**: Liệt kê các năng lực, kiến thức cần đạt sau bài học.
  - 💡 **Khởi động**: Tình huống dẫn dắt mở đầu bài học kèm câu hỏi gợi mở.
  - 🔍 **Khám phá**: Nội dung kiến thức cốt lõi chia theo mục số và mục chữ rõ ràng.
  - 📘 **Hộp kiến thức**: Các khung định nghĩa, khái niệm then chốt được đóng khung nổi bật dễ học.
  - 🛠️ **Thực hành**: Các bước thao tác, hướng dẫn công cụ AI, đoạn mã mẫu (Colab/Python) có nút sao chép nhanh một chạm.
  - ✏️ **Luyện tập**: Câu hỏi trắc nghiệm và bài tập củng cố.
  - 🚀 **Vận dụng**: Câu hỏi tình huống và bài toán thực tế.
  - 📋 **Bảng giải thích thuật ngữ**: Từ điển thuật ngữ AI song ngữ Việt - Anh ở cuối sách.

### 2. Trải nghiệm đọc hiện đại & Tiện ích
- **Tuỳ biến cỡ chữ**: Nút tăng / giảm cỡ chữ `A-` / `A+` mượt mà (14px - 22px).
- **Chế độ đọc đa dạng**: ☀️ Giao diện Sáng, 📜 Giấy ấm (Sepia dịu mắt), 🌙 Giao diện Tối (Dark mode).
- **Mục lục thông minh**: Danh mục theo Chủ đề & Bài học, tự động đánh dấu bài đang học và cuộn nhanh.
- **Mục lục trên trang (Page Outline)**: Thanh điều hướng nhanh đến từng phần của bài học bên phải màn hình.
- **Tìm kiếm toàn văn siêu tốc**: Tìm từ khoá (có dấu hoặc không dấu) hiển thị ngay đoạn văn trích dẫn.
- **Xem bản in gốc song song**: Bất cứ lúc nào học sinh hoặc giáo viên đều có thể bấm **"Xem bản in gốc"** để đối chiếu với trang sách in WebP độ phân giải cao.

---

## 📁 Cấu trúc thư mục

```
Sach AI/
├── index.html                   # Trang chủ Thư viện Tủ sách 3 lớp
├── reader.html                  # Giao diện đọc sách văn bản HTML hiện đại
├── assets/
│   ├── css/style.css            # Toàn bộ CSS hệ thống thiết kế và giao diện đọc sách
│   ├── js/library.js            # Xử lý logic trang chủ và tìm kiếm toàn cục
│   ├── js/reader.js             # Xử lý logic đọc sách chữ, mục lục, cỡ chữ, outline, modal
│   └── favicon.svg              # Biểu tượng tủ sách
├── data/
│   ├── books.json               # Metadata tổng quát 3 cuốn sách
│   ├── lessons-lop-10.json      # Toàn bộ 19 bài học Lớp 10 định dạng JSON & HTML
│   ├── lessons-lop-11.json      # Toàn bộ 20 bài học Lớp 11 định dạng JSON & HTML
│   ├── lessons-lop-12.json      # Toàn bộ 22 bài học Lớp 12 định dạng JSON & HTML
│   └── search-lop-*.json        # Chỉ mục tìm kiếm toàn văn
├── lessons/                     # Các file HTML từng bài học đã được dựng sẵn
├── books/                       # Ảnh WebP trang sách in phục vụ tính năng đối chiếu
└── scripts/                     # Bộ công cụ Python trích xuất và xử lý dữ liệu
    ├── build_all_lessons.py     # Script master trích xuất toàn bộ bài học sang HTML/JSON
    ├── lesson_html_builder.py   # Bộ dựng khối HTML ngữ nghĩa cho từng bài học
    └── ocr_cleaner.py           # Bộ chuẩn hoá chính tả tiếng Việt & OCR
```

---

## 🚀 Triển khai & Chạy thử nghiệm

Chạy trực tiếp bằng bất kì web server tĩnh nào (không cần cài đặt framework nặng nề):

```bash
# Sử dụng Python HTTP server có sẵn
python -m http.server 8080
```
Mở trình duyệt: `http://localhost:8080`

### Triển khai lên Vercel:
```bash
vercel --prod
```
