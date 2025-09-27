#!/bin/bash

# 设置要替换的路径
LOCAL_PATH="/images/work-record"
CDN_PREFIX="https://cdn.heirenlop.com/work-record"

# 设置你要遍历的文件夹路径（修改为你的实际路径）
TARGET_DIR="/home/heirenlop/workspace/heirenlop.github.io/content/work"

# 查找并替换
find "$TARGET_DIR" -type f \( -name "*.html" -o -name "*.md" \) | while read -r file; do
  echo "🛠️ 处理文件: $file"

  # 使用 sed 替换 href 和 src 两个位置的路径
  sed -i "s|href=\"$LOCAL_PATH|href=\"$CDN_PREFIX|g" "$file"
  sed -i "s|src=\"$LOCAL_PATH|src=\"$CDN_PREFIX|g" "$file"
done

echo "✅ 全部替换完成。"

