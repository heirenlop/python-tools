import os

def convert_html_to_md(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                html_path = os.path.join(root, filename)
                md_path = os.path.join(root, filename[:-5] + ".md")

                # 读取 HTML 文件内容
                with open(html_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 写入新的 MD 文件（内容不变）
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(content)

                # 删除原 HTML 文件
                os.remove(html_path)

                print(f"✅ 转换：{html_path} → {md_path}")

if __name__ == "__main__":
    # 🚩 这里填写你要处理的路径（支持相对路径或绝对路径）
    folder = "/home/heirenlop/workspace/heirenlop.github.io/content/daily"

    if os.path.isdir(folder):
        convert_html_to_md(folder)
        print("🎉 所有 .html 文件已成功转换为 .md")
    else:
        print(f"❌ 目录不存在：{folder}")
