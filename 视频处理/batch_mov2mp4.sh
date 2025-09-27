#!/bin/bash

# 使用方法：./batch_mov2mp4.sh [目录路径]
# 如果不填目录，默认使用当前目录

TARGET_DIR="${1:-.}"

echo "📁 正在处理目录: $TARGET_DIR"

for movfile in "$TARGET_DIR"/*.mov "$TARGET_DIR"/*.MOV; do
    [ -e "$movfile" ] || continue

    filename=$(basename "$movfile")
    name="${filename%.*}"
    output="${TARGET_DIR}/${name}.mp4"

    echo "🎬 转换中: $filename → $name.mp4"

    ffmpeg -y -i "$movfile" \
        -c:v libx264 -crf 20 -preset slow \
        -vf scale=1920:-1 \
        -c:a aac -b:a 192k \
        -pix_fmt yuv420p \
        "$output"

    echo "✅ 完成: $output"
    echo "-----------------------------"
done

echo "🎉 所有 .mov 文件处理完成。"

