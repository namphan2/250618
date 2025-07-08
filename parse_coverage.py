#!/usr/bin/env python3
"""
Script để parse dữ liệu coverage từ các file index.html
Tạo file coverage_data.json để hiển thị biểu đồ
"""

import os
import json
import re
from pathlib import Path

def parse_coverage_from_html(html_file_path):
    """Parse dữ liệu coverage từ file HTML"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        coverage_data = {}
        
        # Tìm bảng coverage summary chính
        # Pattern để tìm dòng "all classes" trong bảng đầu tiên
        summary_pattern = r'<td class="name">all classes</td>.*?<td class="coverageStat">\s*<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>.*?<td class="coverageStat">\s*<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>.*?<td class="coverageStat">\s*<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>.*?<td class="coverageStat">\s*<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>.*?<td class="coverageStat">\s*<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>'
        
        match = re.search(summary_pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            coverage_data['Class'] = float(match.group(1))
            coverage_data['Method'] = float(match.group(2))
            coverage_data['Branch'] = float(match.group(3))
            coverage_data['Line'] = float(match.group(4))
            coverage_data['Instruction'] = float(match.group(5))
            return coverage_data
        
        # Fallback: Tìm từng chỉ số riêng biệt trong bảng summary
        # Tìm dòng "all classes" và các giá trị tương ứng
        all_classes_pattern = r'<td class="name">all classes</td>(.*?)</tr>'
        all_classes_match = re.search(all_classes_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if all_classes_match:
            row_content = all_classes_match.group(1)
            
            # Tìm tất cả các giá trị percent trong dòng này
            percent_pattern = r'<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>'
            percent_matches = re.findall(percent_pattern, row_content, re.IGNORECASE)
            
            if len(percent_matches) >= 5:
                coverage_data['Class'] = float(percent_matches[0])
                coverage_data['Method'] = float(percent_matches[1])
                coverage_data['Branch'] = float(percent_matches[2])
                coverage_data['Line'] = float(percent_matches[3])
                coverage_data['Instruction'] = float(percent_matches[4])
                return coverage_data
        
        # Fallback cuối cùng: Tìm các chỉ số riêng lẻ
        patterns = [
            (r'Class,\s*%\s*</th>.*?<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>', 'Class'),
            (r'Method,\s*%\s*</th>.*?<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>', 'Method'),
            (r'Branch,\s*%\s*</th>.*?<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>', 'Branch'),
            (r'Line,\s*%\s*</th>.*?<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>', 'Line'),
            (r'Instruction,\s*%\s*</th>.*?<span class="percent">\s*(\d+(?:\.\d+)?)%\s*</span>', 'Instruction')
        ]
        
        for pattern, key in patterns:
            if key not in coverage_data:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    coverage_data[key] = float(match.group(1))
        
        return coverage_data
        
    except Exception as e:
        print(f"Lỗi khi parse {html_file_path}: {e}")
        return {}

def scan_and_parse_coverage():
    """Quét tất cả thư mục và parse dữ liệu coverage"""
    current_dir = Path('.')
    all_coverage = {}
    
    # Lấy danh sách thư mục từ folders.json nếu có
    folders = []
    if os.path.exists('folders.json'):
        with open('folders.json', 'r', encoding='utf-8') as f:
            folders = json.load(f)
    else:
        # Fallback: quét thư mục
        for item in current_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                index_file = item / 'index.html'
                if index_file.exists():
                    folders.append(item.name)
    
    print(f"Đang parse coverage từ {len(folders)} thư mục...")
    
    for folder in folders:
        index_file = current_dir / folder / 'index.html'
        if index_file.exists():
            print(f"  Đang xử lý {folder}...")
            coverage = parse_coverage_from_html(index_file)
            if coverage:
                all_coverage[folder] = coverage
                print(f"    Tìm thấy: {coverage}")
            else:
                print(f"    Không tìm thấy dữ liệu coverage")
    
    return all_coverage

def create_coverage_json():
    """Tạo file coverage_data.json"""
    coverage_data = scan_and_parse_coverage()
    
    # Tạo file JSON
    with open('coverage_data.json', 'w', encoding='utf-8') as f:
        json.dump(coverage_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nĐã tạo file coverage_data.json với dữ liệu từ {len(coverage_data)} thư mục:")
    for folder, data in coverage_data.items():
        print(f"  {folder}: {data}")
    
    return coverage_data

if __name__ == "__main__":
    print("Đang parse dữ liệu coverage...")
    create_coverage_json()
    print("Hoàn thành!") 