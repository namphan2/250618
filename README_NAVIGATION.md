# Hướng Dẫn Sử Dụng Navigation System

## Tổng Quan
Navigation system này cho phép đọc danh sách thư mục động từ local filesystem, hiển thị trong dropdown menu và tạo biểu đồ so sánh coverage giữa các thư mục.

## Các File Quan Trọng

### 1. `index.html`
- File chính chứa navigation bar và biểu đồ
- Tự động load danh sách thư mục từ `folders.json`
- Tự động load dữ liệu coverage từ `coverage_data.json`
- Có fallback nếu không tìm thấy các file JSON

### 2. `folders.json`
- File JSON chứa danh sách thư mục
- Được tạo tự động bởi `scan_folders.py`
- Format: `["250528", "250618"]`

### 3. `coverage_data.json`
- File JSON chứa dữ liệu coverage từ các thư mục
- Được tạo tự động bởi `parse_coverage.py`
- Format: `{"250528": {"Class": 3.2, "Method": 3.2, ...}, ...}`

### 4. `scan_folders.py`
- Script Python để quét thư mục hiện tại
- Tìm các thư mục có file `index.html`
- Tạo file `folders.json`

### 5. `parse_coverage.py`
- Script Python để parse dữ liệu coverage
- Đọc các file `index.html` trong các thư mục
- Trích xuất các chỉ số: Class, Method, Branch, Line, Instruction
- Tạo file `coverage_data.json`

### 6. `update_folders.sh`
- Script shell để dễ dàng cập nhật cả thư mục và coverage
- Chạy cả `scan_folders.py` và `parse_coverage.py`

## Cách Sử Dụng

### Khi có thư mục mới:
1. Thêm thư mục mới vào project
2. Đảm bảo thư mục có file `index.html` với dữ liệu coverage
3. Chạy lệnh:
   ```bash
   ./update_folders.sh
   ```
   hoặc chạy riêng lẻ:
   ```bash
   python3 scan_folders.py
   python3 parse_coverage.py
   ```

### Khi mở trang web:
- Navigation sẽ tự động load danh sách thư mục từ `folders.json`
- Tab "Biểu đồ" sẽ hiển thị 5 biểu đồ so sánh coverage
- Nếu không có JSON files, sẽ sử dụng fallback
- Click vào thư mục trong dropdown để mở `index.html` của thư mục đó

## Tính Năng

### Navigation Bar
- **Tab 1**: Trang chủ (để trống)
- **Tab 2**: Thư mục (dropdown động)
- **Tab 3**: Biểu đồ (5 chart so sánh coverage)
- **Tab 4**: Hướng dẫn (nội dung cố định)

### Dropdown Menu
- Hiển thị tất cả thư mục có `index.html`
- Sắp xếp theo tên alphabet
- Hover để hiện menu
- Click để mở thư mục

### Biểu Đồ Coverage
- **5 biểu đồ cột** cho từng chỉ số coverage
- **Trục X**: Tên thư mục
- **Trục Y**: Giá trị coverage (%)
- **Màu sắc khác nhau** cho từng loại coverage
- **Responsive** và interactive với tooltip

### Các Chỉ Số Coverage
1. **Class Coverage**: Tỷ lệ class được kiểm thử
2. **Method Coverage**: Tỷ lệ method được kiểm thử
3. **Branch Coverage**: Tỷ lệ nhánh điều kiện được kiểm thử
4. **Line Coverage**: Tỷ lệ dòng lệnh được kiểm thử
5. **Instruction Coverage**: Tỷ lệ lệnh thực thi được kiểm thử

### Fallback System
- Nếu không có `folders.json`: sử dụng danh sách cứng
- Nếu không có `coverage_data.json`: hiển thị thông báo lỗi
- Dễ dàng cập nhật fallback list trong code

## Lưu Ý
- Chỉ thư mục có file `index.html` mới được hiển thị
- Thư mục bắt đầu bằng `.` sẽ bị bỏ qua
- File JSON được tạo tự động, không cần chỉnh sửa thủ công
- Script parse coverage sử dụng regex để tìm dữ liệu trong HTML
- Biểu đồ sử dụng Chart.js từ CDN

## Troubleshooting
- Nếu biểu đồ không hiển thị: chạy `python3 parse_coverage.py`
- Nếu dropdown trống: chạy `python3 scan_folders.py`
- Nếu cả hai: chạy `./update_folders.sh` 