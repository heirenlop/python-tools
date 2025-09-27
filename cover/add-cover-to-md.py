import os
import re
from pypinyin import lazy_pinyin

# === 配置 ===
md_folder = "./"  # ← 替换成你的 Markdown 文件夹路径
cover_prefix = "/images/cover/"      # 写入的 cover 路径前缀

# === 处理函数 ===
def generate_cover_filename(md_filename):
    name = os.path.splitext(md_filename)[0]
    if name.endswith(".en"):
        name = name[:-3]
    pinyin = ''.join(lazy_pinyin(name))  # 将“重庆”变为“chongqing”
    return f'{cover_prefix}{pinyin}.jpg'

# === 遍历所有 .md 文件 ===
for filename in os.listdir(md_folder):
    if not (filename.endswith(".md") or filename.endswith(".en.md")):
        continue

    path = os.path.join(md_folder, filename)

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if lines[0].strip() != '+++':
        print(f"⏭️ 跳过非 front matter 文件：{filename}")
        continue

    # 查找 url 所在行，并判断是否已有 cover 字段
    has_cover = any('cover =' in line for line in lines)
    if has_cover:
        print(f"✔️ 已有 cover，跳过：{filename}")
        continue

    new_lines = []
    inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.strip().startswith('url ='):
            # 在 url 下方插入 cover 行
            cover_line = f'cover = "{generate_cover_filename(filename)}"\n'
            new_lines.append(cover_line)
            inserted = True

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"✅ 已添加 cover 到：{filename}")

