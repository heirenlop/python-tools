import os
import re
from slugify import slugify  # pip install python-slugify

def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有 TOML front matter (以+++包裹)
    if not content.strip().startswith('+++'):
        print(f'Skipped (no TOML front matter): {filepath}')
        return

    # 提取 front matter 内容
    toml_match = re.search(r'^\+\+\+\n(.*?)\n\+\+\+', content, re.DOTALL)
    if not toml_match:
        print(f'Skipped (TOML format mismatch): {filepath}')
        return

    toml_content = toml_match.group(1)

    # 已存在 url 字段
    if re.search(r'^url\s*=.*$', toml_content, re.MULTILINE):
        print(f'Skipped (already has url): {filepath}')
        return

    # 提取 title 字段
    title_match = re.search(r'^title\s*=\s*["\'](.*?)["\']', toml_content, re.MULTILINE)
    if not title_match:
        print(f'Skipped (no title): {filepath}')
        return

    title = title_match.group(1).strip()
    slug = slugify(title)

    # 判断是否是英文版（以 .en.md 结尾）
    if filepath.endswith('.en.md'):
        url_line = f'url = "/work/en/{slug}/"'
    else:
        url_line = f'url = "/work/{slug}/"'

    # 插入 url 行（插在 title 行之后）
    lines = toml_content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('title'):
            lines.insert(i + 1, url_line)
            break

    new_toml = '\n'.join(lines)
    new_content = content.replace(toml_content, new_toml)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'✅ Updated: {filepath}')


def process_all_md_files(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_md_file(os.path.join(root, file))


if __name__ == '__main__':
    folder_path = '/home/heirenlop/workspace/heirenlop.github.io/content/work'  # ← 修改成你的目录路径
    process_all_md_files(folder_path)

