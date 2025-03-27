import os
import re
"将博客文件中的图片格式转换为 Fancybox 格式"
# 设定博客文件目录
blog_dir = '/home/heirenlop/workspace/my_repo/heirenlop.github.io/content/work'  # 修改为您的博客文件目录

def convert_images_to_fancybox(content):
    # 使用正则表达式匹配图片语法：Markdown 和 HTML 格式
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)|<img[^>]*src="([^"]+)"[^>]*>'

    # 替换为 Fancybox 格式
    def replace_img(match):
        if match.group(1) and match.group(2):  # Markdown 图片
            alt_text = match.group(1)
            img_url = match.group(2)
            return f'<a data-fancybox="gallery" href="{img_url}">\n    <img src="{img_url}" alt="{alt_text}" loading="lazy">\n</a>'
        elif match.group(3):  # HTML 图片
            img_url = match.group(3)
            return f'<a data-fancybox="gallery" href="{img_url}">\n    <img src="{img_url}" loading="lazy">\n</a>'
        return match.group(0)

    # 替换所有图片
    return re.sub(img_pattern, replace_img, content)

def process_blog_files(blog_dir):
    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(blog_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.html'):  # 处理md和html文件
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 将文件中的图片格式转换为fancybox
                new_content = convert_images_to_fancybox(content)

                # 将更新后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Processed: {file_path}')

if __name__ == '__main__':
    process_blog_files(blog_dir)

