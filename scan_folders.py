#!/usr/bin/env python3
"""
Script để quét thư mục hiện tại và tạo file folders.json
Chạy script này để cập nhật danh sách thư mục cho navigation
"""

import os
import json
from pathlib import Path

def scan_folders():
    """Quét thư mục hiện tại để tìm các thư mục con"""
    current_dir = Path('.')
    folders = []
    
    # Lấy tất cả thư mục con
    for item in current_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Kiểm tra xem thư mục có file index.html không
            index_file = item / 'index.html'
            if index_file.exists():
                folders.append(item.name)
    
    # Sắp xếp theo tên
    folders.sort()
    return folders

def create_folders_json():
    """Tạo file folders.json với danh sách thư mục"""
    folders = scan_folders()
    
    # Tạo file JSON
    with open('folders.json', 'w', encoding='utf-8') as f:
        json.dump(folders, f, ensure_ascii=False, indent=2)
    
    print(f"Đã tạo file folders.json với {len(folders)} thư mục:")
    for folder in folders:
        print(f"  - {folder}")
    
    return folders

if __name__ == "__main__":
    print("Đang quét thư mục...")
    create_folders_json()
    print("Hoàn thành!") 