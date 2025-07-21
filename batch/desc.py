import os
import re

def extract_description(content, is_en=False):
    """
    从 HTML 中提取引言第二段，支持中英文标题
    """
    if is_en:
        pattern = r"<h2>Introduction</h2>\s*<p>.*?</p>\s*<p>(.*?)</p>"
    else:
        pattern = r"<h2>引言</h2>\s*<p>.*?</p>\s*<p>(.*?)</p>"

    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 如果已有 description，则跳过
    if 'description =' in content:
        return

    is_en = file_path.endswith('.en.md')
    desc = extract_description(content, is_en)
    if not desc:
        return

    # 拆分 front matter
    parts = content.split('+++')
    if len(parts) < 3:
        print(f"⚠️ front matter 异常，跳过：{file_path}")
        return

    front_matter = parts[1].strip()
    rest = '+++'.join(parts[2:]).lstrip()

    # 添加 description 字段
    front_matter += f'\ndescription = "{desc}"\n'

    new_content = f"+++\n{front_matter}+++\n{rest}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 处理成功: {file_path}")

def scan_directory(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".md") or file.endswith(".en.md"):
                full_path = os.path.join(root, file)
                process_file(full_path)

# 执行处理
scan_directory("/home/heirenlop/workspace/heirenlop.github.io/content/daily")

