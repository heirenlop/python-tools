import os
import re

# === 配置你的图片路径 ===
folder_path = './'  # 修改成你的路径

# 支持的扩展名
valid_ext = ['.jpg', '.jpeg', '.png', '.webp']

# 遍历文件夹
for filename in os.listdir(folder_path):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in valid_ext:
        continue

    # 用正则删除末尾数字，如 changbaishan1 → changbaishan
    new_name = re.sub(r'\d+$', '', name)
    new_filename = new_name + ext.lower()
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_filename)

    # 避免重名覆盖
    if filename == new_filename:
        continue
    elif os.path.exists(dst):
        print(f"⚠️ 跳过：{new_filename} 已存在")
        continue

    os.rename(src, dst)
    print(f"✅ 重命名：{filename} → {new_filename}")

