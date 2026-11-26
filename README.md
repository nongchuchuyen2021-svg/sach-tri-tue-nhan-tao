# Tủ Sách Trí Tuệ Nhân Tạo THPT (Lớp 10 – 11 – 12)

Website đọc sách điện tử HTML tĩnh cho bộ sách **Trí tuệ nhân tạo** cấp Trung học phổ thông (Lớp 10, Lớp 11, Lớp 12) — Nhà xuất bản Giáo dục Việt Nam.

## Tính năng chính
- **Kệ sách trực quan**: Hiển thị bìa 3 cuốn sách, thông tin chủ biên/NXB/ISBN, thống kê chủ đề – bài học – số trang, tiến độ đọc lưu tự động trên trình duyệt (`localStorage`).
- **Trình đọc sách chuẩn bản in**:
  - Tách đôi từng trang từ bản scan PDF, xoay chỉnh thẳng đứng và loại bỏ dải watermark CamScanner.
  - Ghép cặp trang chẵn (trái) – lẻ (phải) đúng như sách giấy khi mở ở chế độ **2 trang**, hỗ trợ chế độ **1 trang** và **Cuộn dọc liên tục**.
  - Mục lục theo từng Chủ đề & Bài học, tự động đánh dấu bài đang đọc.
  - Tìm kiếm toàn văn tiếng Việt (hỗ trợ cả có dấu và không dấu) trên từng cuốn và trên toàn bộ cả 3 cuốn.
  - Phóng to/thu nhỏ (50%–250%), kéo thả khi phóng to, đánh dấu trang (`Bookmark`), lưới xem nhanh tất cả trang, 3 chế độ màu đọc (`Sáng`, `Giấy ấm`, `Tối`), toàn màn hình, hỗ trợ phím tắt và thao tác vuốt trên điện thoại.

## Cấu trúc thư mục
- `index.html` — Trang Tủ sách và tìm kiếm toàn bộ 3 cuốn.
- `reader.html` — Trình đọc sách điện tử.
- `assets/` — Stylesheet (`css/style.css`), script (`js/library.js`, `js/reader.js`), `favicon.svg`.
- `data/` — Metadata & mục lục (`books.json`) và dữ liệu tìm kiếm (`search-lop-10.json`, `search-lop-11.json`, `search-lop-12.json`).
- `books/` — Ảnh trang sách WebP và ảnh thu nhỏ (`thumbs/`) cho từng lớp.
- `scripts/build_books.py` — Script Python tái tạo ảnh WebP và dữ liệu JSON từ các file PDF gốc.

## Tái tạo dữ liệu từ PDF
```bash
pip install pymupdf pillow numpy
python scripts/build_books.py
```
