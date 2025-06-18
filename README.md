# Hướng Dẫn Đọc Report HTML của Kover (Kotlin) 👓

## 1. Trang Tổng Quan (index.html)

- **Ngay khi mở báo cáo**, bạn sẽ thấy bảng tổng hợp các chỉ số bao phủ:
  - **Class Coverage**: Tỷ lệ class đã được kiểm thử
  - **Method Coverage**: Tỷ lệ method đã được kiểm thử
  - **Line Coverage**: Tỷ lệ dòng lệnh đã được kiểm thử
  - **Branch Coverage**: Tỷ lệ nhánh điều kiện đã được kiểm thử
  - **Instruction Coverage**: Tỷ lệ lệnh thực thi đã được kiểm thử

- **Mỗi chỉ số** đều có phần trăm rõ ràng, giúp bạn đánh giá nhanh mức độ kiểm thử của dự án.

---

## 2. Màu Sắc Thể Hiện Độ Bao Phủ

- **Xanh lá** 🍀: Đã kiểm thử đầy đủ (fully covered)
- **Vàng** 🌕: Được kiểm thử một phần (partially covered)
- **Đỏ** 🔴: Chưa kiểm thử (uncovered)

> **Nhìn vào màu sắc, bạn sẽ biết ngay phần nào của mã nguồn đã được kiểm thử kỹ lưỡng và phần nào còn thiếu sót.**

---

## 3. Xem Chi Tiết Theo File/Class

- **Nhấp vào tên package, class hoặc file** để xem chi tiết.
- **Bảng chi tiết** sẽ hiện ra:
  - Danh sách các method và dòng lệnh
  - Số lượng và tỷ lệ dòng/method được kiểm thử

- **Các dòng mã** sẽ được đánh dấu màu tương ứng:
  - Xanh: đã chạy qua khi test
  - Đỏ: chưa chạy qua khi test
  - Vàng: chỉ một phần được test (thường là các nhánh điều kiện)

---

## 4. Điều Hướng Nhanh

- **Thanh bên trái** (hoặc trên cùng) giúp bạn chuyển nhanh giữa các package, class, file.
- **Nhấp vào từng mục** để soi kỹ từng phần của dự án.

---

## 5. Một Số Mẹo Đọc Báo Cáo Hiệu Quả

- **Tập trung vào các vùng màu đỏ/vàng** để bổ sung test.
- **So sánh các chỉ số coverage** giữa các class để xác định điểm yếu trong kiểm thử.
- **Kiểm tra các nhánh điều kiện** (if/else, when...) vì đây là nơi dễ bị bỏ sót test nhất.

---

> **Tóm lại:**  
> Chỉ cần mở báo cáo, nhìn màu sắc và các chỉ số phần trăm, sau đó nhấp vào từng file/class để xem chi tiết là bạn đã nắm được toàn bộ độ bao phủ kiểm thử của dự án mình!

