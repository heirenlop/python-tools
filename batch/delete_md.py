import os

def delete_md_files(folder, exclude_files):
    deleted = 0
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".md") and file not in exclude_files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"🗑️ 已删除：{file_path}")
                deleted += 1
            elif file in exclude_files:
                print(f"✅ 保留：{file}")
    print(f"\n共删除 {deleted} 个 .md 文件")

if __name__ == "__main__":
    # 👇 修改为你要处理的目录（相对路径或绝对路径都可以）
    target_folder = "/home/heirenlop/workspace/heirenlop.github.io/content/daily"

    # 👇 修改为你不想删除的文件（文件名，带 `.md` 后缀）
    exclude = [
        "_index.md",
        "_index.en.md"
    ]

    if os.path.isdir(target_folder):
        delete_md_files(target_folder, exclude)
    else:
        print(f"❌ 目录不存在：{target_folder}")
