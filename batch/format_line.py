import re
"以在md文件的每个标题#前插入分割线---"
def insert_separator(filename):
    # 读取所有行
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    # 正则匹配以单个 '#' 开头（后面跟非 '#' 字符），忽略前导空白
    pattern = re.compile(r'^\s*#[^#]')
    
    for line in lines:
        # 如果当前行为以单个 '#' 开头的标题
        if pattern.match(line):
            # 检查 new_lines 中最后一个非空行是否为 '---'
            found_separator = False
            for prev_line in reversed(new_lines):
                if prev_line.strip() == "":
                    continue
                if prev_line.strip() == "---":
                    found_separator = True
                break
            # 如果没有 '---' 分割线，则插入空行、分割线和空行
            if not found_separator:
                new_lines.append("\n")
                new_lines.append("---\n")
                new_lines.append("\n")
        new_lines.append(line)
    
    # 将修改后的内容写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    # 固定处理文件 your_file.md
    insert_separator("/home/heirenlop/workspace/my_repo/heirenlop.github.io/content/work/vscode.md")
