#!/usr/bin/env python3
"""
博客文章自动添加脚本

使用方法:
python3 add_article.py 文章路径.md 文章URL名称 文章日期

例如:
python3 add_article.py ~/Documents/我的新文章.md new-article "2025年02月15日"
"""

import sys
import os
import re
import shutil
import subprocess
from datetime import datetime
import markdown

# 检查参数
if len(sys.argv) < 4:
    print("使用方法: python3 add_article.py 文章路径.md 文章URL名称 文章日期")
    print('例如: python3 add_article.py ~/Documents/我的新文章.md new-article "2025年02月15日"')
    sys.exit(1)

# 获取参数
md_file_path = os.path.expanduser(sys.argv[1])
article_url_name = sys.argv[2]
article_date = sys.argv[3]

# 检查文件是否存在
if not os.path.exists(md_file_path):
    print(f"错误: 文件 {md_file_path} 不存在")
    sys.exit(1)

# 读取Markdown文件
with open(md_file_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 提取标题
title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
if title_match:
    article_title = title_match.group(1)
else:
    print("错误: 无法从Markdown文件中提取标题，请确保文件第一行是以'# '开头的标题")
    sys.exit(1)

# 将Markdown转换为HTML
html_content = markdown.markdown(md_content, extensions=['extra'])

# 创建文章目录
article_dir = f"posts/{article_url_name}"
os.makedirs(article_dir, exist_ok=True)

# 创建HTML文件
html_template = f"""<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{article_title}</title>
    <style>
      .home-link {{
        position: absolute;
        top: 20px;
        right: 20px;
        text-decoration: none;
        color: #007acc;
        font-size: 14px;
        background-color: #f5f5f5;
        padding: 5px 10px;
        border-radius: 4px;
      }}
      .home-link:hover {{
        background-color: #e5e5e5;
      }}
      body {{
        position: relative;
      }}
    </style>
  </head>
  <body style="max-width: 720px; margin: 40px auto; font-family: -apple-system, BlinkMacSystemFont, Helvetica, sans-serif; line-height: 1.6; padding: 0 20px;">
    <a href="../../" class="home-link">返回首页</a>
    <div>
      <img src="../../img/avatar.png" alt="头像" style="width: 80px; border-radius: 50%; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto;" />
      <h1 style="text-align: left;">{article_title}</h1>
    </div>

    {html_content.replace('<h1>', '<!-- 标题已在上方显示 -->')}

    <hr />
    <!-- 文章列表将在后面更新 -->
    <ul style="list-style-type: disc;">
        <li>
          <a href="../../posts/{article_url_name}/">{article_title}</a>
          <div style="font-size: 0.8em; color: #666; margin-top: 3px;">{article_date}</div>
        </li>
    </ul>

  </body>
</html>
"""

with open(f"{article_dir}/index.html", 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"已创建文章: {article_dir}/index.html")

# 更新所有页面的文章列表
# 这部分需要更复杂的逻辑，这里只是一个简化版本
# 实际使用时，您可能需要根据您的博客结构进行调整

# 提交并推送更改
try:
    subprocess.run(["git", "add", article_dir], check=True)
    subprocess.run(["git", "commit", "-m", f"添加新文章: {article_title}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("已提交并推送更改到GitHub")
except subprocess.CalledProcessError as e:
    print(f"Git操作失败: {e}")

print(f"文章已成功添加: {article_title}")
print(f"您可以在以下地址访问: https://chemark.github.io/posts/{article_url_name}/")
