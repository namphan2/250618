import os
import shutil
from pathlib import Path

# Lấy danh sách tất cả folder con (không tính file, folder ẩn)
def get_subfolders(base_dir):
    return [f for f in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, f)) and not f.startswith('.')]

def main():
    base_dir = Path('.')
    folders = get_subfolders(base_dir)
    if not folders:
        print("Không tìm thấy folder con nào.")
        return

    # Lọc các folder có tên là số (theo format ví dụ 250709)
    numeric_folders = [f for f in folders if f.isdigit()]
    if not numeric_folders:
        print("Không có folder nào có tên dạng số.")
        return

    # Tìm folder mới nhất (lớn nhất theo tên)
    newest_folder = max(numeric_folders)
    print(f"Folder mới nhất (full): {newest_folder}")

    for folder in numeric_folders:
        folder_path = base_dir / folder
        if folder == newest_folder:
            print(f"Giữ nguyên folder: {folder}")
            continue  # Giữ nguyên folder mới nhất
        print(f"Xử lý folder: {folder}")
        # Giữ lại file index.html nếu có, xoá các file/thư mục khác
        for item in folder_path.iterdir():
            if item.name == 'index.html':
                continue
            if item.is_file() or item.is_symlink():
                try:
                    item.unlink()
                    print(f"  Đã xoá file: {item.name}")
                except Exception as e:
                    print(f"  Lỗi khi xoá file {item.name}: {e}")
            elif item.is_dir():
                try:
                    shutil.rmtree(item)
                    print(f"  Đã xoá thư mục: {item.name}")
                except Exception as e:
                    print(f"  Lỗi khi xoá thư mục {item.name}: {e}")

if __name__ == "__main__":
    main() 