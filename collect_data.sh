#!/bin/bash

# Bước 1: Di chuyển vào thư mục payx-sprint, Detect thay đổi git, stash nếu có; checkout branch sprint_YYYYMMDD/master lớn nhất hoặc theo user nhập
cd /Users/nam.phan2/Projects/momo-platform/payx-sprint || { echo "Không thể cd vào thư mục payx-sprint"; exit 1; }

# Lưu branch hiện tại để quay lại sau
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Kiểm tra thay đổi local
if [[ -n $(git status --porcelain) ]]; then
  echo ">>>>>>>>>>>>> Có thay đổi local, stash lại..."
  git stash push -u -m "Auto stash before switching branch"
else
  echo ">>>>>>>>>>>>> Không có thay đổi local."
fi

# Fetch remote để đảm bảo danh sách branch mới nhất
git fetch origin

# Tìm trước branch sprint_YYYYMMDD/master lớn nhất ở remote
default_branch=$(git branch -r | grep 'origin/sprint_[0-9]\{8\}/master' | grep -o 'sprint_[0-9]\{8\}/master' | sort -r | head -n1)
default_yymmdd=${default_branch:9:6}

# Hỏi tên sprint muốn sử dụng, gợi ý YYMMDD lớn nhất
read -p "Nhập sprint muốn sử dụng theo dạng YYMMDD (Enter để tự động chọn sprint lớn nhất: $default_yymmdd): " INPUT_SPRINT
if [[ -n "$INPUT_SPRINT" ]]; then
  BRANCH_LOCAL="sprint_20${INPUT_SPRINT}/master"
  # Kiểm tra tồn tại trên remote
  if git ls-remote --exit-code --heads origin "$BRANCH_LOCAL" >/dev/null 2>&1; then
    echo ">>>>>>>>>>>>> Sử dụng branch: $BRANCH_LOCAL ..."
    git checkout "$BRANCH_LOCAL"
  else
    echo "Branch $BRANCH_LOCAL không tồn tại trên remote! Dừng script."
    exit 1
  fi
else
  # Nếu user không nhập, dùng branch lớn nhất đã tìm được
  if [[ -z "$default_branch" ]]; then
    echo "Không tìm thấy branch sprint_YYYYMMDD/master nào trên remote!"; exit 1;
  fi
  BRANCH_LOCAL="$default_branch"
  echo ">>>>>>>>>>>>> Checkout branch $BRANCH_LOCAL ..."
  git checkout $BRANCH_LOCAL
fi

# Lấy YYYYMMDD từ branch đã checkout
if [[ $BRANCH_LOCAL =~ sprint_([0-9]{8})/ ]]; then
  DATE_PART=${BASH_REMATCH[1]}
  YYMMDD=${DATE_PART:2}
else
  echo "Không tìm thấy định dạng ngày trong tên branch ($BRANCH_LOCAL), dừng script."
  exit 1
fi

# Bước 2: chạy yarn all
cd /Users/nam.phan2/Projects/momo-platform/payx-sprint
echo ">>>>>>>>>>>>> Chạy yarn all ở thư mục payx-sprint..."
yarn all
cd ./packages/momo-compose || { echo "Không thể cd vào thư mục momo-compose"; exit 1; }

# Bước 3: Chỉnh sửa file MoMoCompose/build.gradle.kts
BUILD_FILE="MoMoCompose/build.gradle.kts"

# Thêm plugin kover ngay sau dòng plugins {
sed -i '' '/plugins[[:space:]]*{/a \
  id("org.jetbrains.kotlinx.kover") version "0.9.1"\
' "$BUILD_FILE"

# Thêm một dòng trống trước khi thêm block kover vào cuối file
echo "" >> "$BUILD_FILE"
cat <<EOL >> "$BUILD_FILE"
kover {
    reports {
        filters {
            includes {
                packages("vn.momo.compose.payment.*")
            }
        }
    }
}
EOL

# Bước 3.1: Chạy sync gradle ở thư mục android
cd ../../../android
echo ">>>>>>>>>>>>> Sync gradle ở thư mục android..."
./gradlew build --refresh-dependencies

# Bước 3.2: Chạy koverHtmlReport ở momo-compose
cd ../packages/momo-compose
echo ">>>>>>>>>>>>> Chạy koverHtmlReport ở momo-compose..."
./gradlew :MomoCompose:koverHtmlReport

# Bước 4: Đổi tên folder html thành YYMMDD từ branch đã checkout, rồi move về project html-doc
cd MoMoCompose/build/reports/kover || { echo "Không thể cd vào thư mục kover report"; exit 1; }
echo ">>>>>>>>>>>>> Đổi tên folder html thành $YYMMDD ..."
mv html "$YYMMDD"
echo ">>>>>>>>>>>>> Move thư mục $YYMMDD về project html-doc ..."
mv "$YYMMDD" /Users/nam.phan2/html-doc/

# Bước 5: Quay lại project html-doc và chạy update_folders
cd /Users/nam.phan2/html-doc
echo ">>>>>>>>>>>>> Chạy update_folders ..."
./update_folders.sh

# Bước 6.1: Commit và push folder vừa move với message là tên folder
if [[ -d "$YYMMDD" ]]; then
  git add .
  git commit -m "$YYMMDD"
  git push
else
  echo "Không tìm thấy thư mục $YYMMDD để commit."
fi

# Bước 6.2: Trở về payx-sprint, revert mọi thay đổi, checkout lại branch cũ và pop stash
cd /Users/nam.phan2/Projects/momo-platform/payx-sprint
echo ">>>>>>>>>>>>> Revert mọi thay đổi ở payx-sprint ..."
git restore .
git clean -fd
echo ">>>>>>>>>>>>> Quay lại branch cũ: $ORIGINAL_BRANCH ..."
git checkout $ORIGINAL_BRANCH
git stash pop || echo "Không có stash để pop hoặc pop stash lỗi."

# Kết thúc script 