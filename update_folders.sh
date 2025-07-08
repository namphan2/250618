#!/bin/bash

# Script để cập nhật danh sách thư mục và dữ liệu coverage cho navigation
# Chạy script này mỗi khi có thư mục mới được thêm vào

echo "Đang cập nhật danh sách thư mục..."

# Chạy script Python để quét thư mục
python3 scan_folders.py

echo "Đang cập nhật dữ liệu coverage..."

# Chạy script Python để parse coverage
python3 parse_coverage.py

echo "Cập nhật hoàn thành!"
echo "Bạn có thể mở index.html để xem danh sách thư mục và biểu đồ coverage mới." 