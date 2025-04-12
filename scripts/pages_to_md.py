#!/usr/bin/env python3
"""
将Pages文件转换为Markdown文件的辅助脚本

使用方法:
python3 pages_to_md.py Pages文件路径.md.pages

例如:
python3 pages_to_md.py ~/Documents/ChatGPT眼中的星树浩.md.pages
"""

import sys
import os
import subprocess
import tempfile

# 检查参数
if len(sys.argv) < 2:
    print("使用方法: python3 pages_to_md.py Pages文件路径.md.pages")
    print('例如: python3 pages_to_md.py ~/Documents/ChatGPT眼中的星树浩.md.pages')
    sys.exit(1)

# 获取参数
pages_file_path = os.path.expanduser(sys.argv[1])

# 检查文件是否存在
if not os.path.exists(pages_file_path):
    print(f"错误: 文件 {pages_file_path} 不存在")
    sys.exit(1)

# 获取文件名（不包括扩展名）
base_name = os.path.basename(pages_file_path)
file_name = os.path.splitext(base_name)[0]
if file_name.endswith('.md'):
    file_name = file_name[:-3]  # 移除 .md 后缀

# 创建输出文件路径
output_file = f"{file_name}.md"

print(f"正在将 {pages_file_path} 转换为 {output_file}...")

# 使用textutil命令（macOS自带）将Pages文件转换为纯文本
try:
    with tempfile.NamedTemporaryFile(suffix='.txt') as temp_file:
        subprocess.run(['textutil', '-convert', 'txt', '-output', temp_file.name, pages_file_path], check=True)
        
        # 读取转换后的文本
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有Markdown标题
        if not content.strip().startswith('# '):
            # 如果没有标题，添加一个基于文件名的标题
            content = f"# {file_name}\n\n{content}"
        
        # 保存为Markdown文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"转换完成！Markdown文件已保存为: {output_file}")
        print(f"现在您可以使用以下命令将文章添加到博客:")
        print(f"python3 scripts/update_blog.py {output_file} {file_name.lower().replace(' ', '-')} \"YYYY年MM月DD日\"")
        
except subprocess.CalledProcessError as e:
    print(f"转换失败: {e}")
    print("请尝试手动在Pages中导出为Markdown格式。")
except Exception as e:
    print(f"发生错误: {e}")
    print("请尝试手动在Pages中导出为Markdown格式。")
