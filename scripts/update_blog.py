#!/usr/bin/env python3
"""
博客更新脚本

使用方法:
python3 update_blog.py 文章路径.md 文章URL名称 文章日期

例如:
python3 update_blog.py ~/Documents/我的新文章.md new-article "2025年02月15日"
"""

import sys
import os
import re
import glob
from datetime import datetime
import markdown
import json

# 检查参数
if len(sys.argv) < 4:
    print("使用方法: python3 update_blog.py 文章路径.md 文章URL名称 文章日期")
    print('例如: python3 update_blog.py ~/Documents/我的新文章.md new-article "2025年02月15日"')
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

# 创建文章元数据文件，用于存储文章信息
article_meta = {
    "title": article_title,
    "url": article_url_name,
    "date": article_date,
    "timestamp": datetime.now().isoformat()
}

# 确保metadata目录存在
os.makedirs("metadata", exist_ok=True)

# 保存文章元数据
with open(f"metadata/{article_url_name}.json", 'w', encoding='utf-8') as f:
    json.dump(article_meta, f, ensure_ascii=False, indent=2)

# 获取所有文章元数据
articles = []
for meta_file in glob.glob("metadata/*.json"):
    with open(meta_file, 'r', encoding='utf-8') as f:
        article_data = json.load(f)
        articles.append(article_data)

# 按日期排序文章（假设日期格式为"YYYY年MM月DD日"）
articles.sort(key=lambda x: x["timestamp"], reverse=True)

# 生成文章列表HTML
article_list_html = ""
for article in articles:
    article_list_html += f"""        <li>
          <a href="../../posts/{article['url']}/">{article['title']}</a>
          <div style="font-size: 0.8em; color: #666; margin-top: 3px;">{article['date']}</div>
        </li>
"""

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
    <ul style="list-style-type: disc;">
{article_list_html}
    </ul>

  </body>
</html>
"""

with open(f"{article_dir}/index.html", 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"已创建文章: {article_dir}/index.html")

# 更新首页
with open("index.html", 'r', encoding='utf-8') as f:
    index_content = f.read()

# 提取首页文章列表部分
list_pattern = r'<ul style="list-style-type: disc;">(.*?)</ul>'
list_match = re.search(list_pattern, index_content, re.DOTALL)

if list_match:
    # 生成首页文章列表HTML
    home_list_html = '<ul style="list-style-type: disc;">\n'
    for article in articles:
        home_list_html += f"""  <li>
    <a href="posts/{article['url']}/">{article['title']}</a>
    <div style="font-size: 0.8em; color: #666; margin-top: 3px;">{article['date']}</div>
  </li>
"""
    home_list_html += '</ul>'
    
    # 更新首页
    new_index_content = re.sub(list_pattern, home_list_html, index_content, flags=re.DOTALL)
    
    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(new_index_content)
    
    print("已更新首页文章列表")

# 更新所有文章页面的文章列表
for post_dir in glob.glob("posts/*/"):
    post_html_file = os.path.join(post_dir, "index.html")
    if os.path.exists(post_html_file):
        with open(post_html_file, 'r', encoding='utf-8') as f:
            post_content = f.read()
        
        # 提取文章列表部分
        post_list_match = re.search(list_pattern, post_content, re.DOTALL)
        
        if post_list_match:
            # 生成文章列表HTML
            post_list_html = '<ul style="list-style-type: disc;">\n'
            for article in articles:
                post_list_html += f"""        <li>
          <a href="../../posts/{article['url']}/">{article['title']}</a>
          <div style="font-size: 0.8em; color: #666; margin-top: 3px;">{article['date']}</div>
        </li>
"""
            post_list_html += '    </ul>'
            
            # 更新文章页面
            new_post_content = re.sub(list_pattern, post_list_html, post_content, flags=re.DOTALL)
            
            with open(post_html_file, 'w', encoding='utf-8') as f:
                f.write(new_post_content)
            
            print(f"已更新文章列表: {post_html_file}")

print(f"\n✅ 文章已成功添加: {article_title}")
print(f"📁 文章目录: {article_dir}/index.html")
print(f"🌐 发布后访问地址: https://chemark.github.io/posts/{article_url_name}/")
print(f"\n📝 下一步操作：")
print(f"1. 检查生成的文章是否正确")
print(f"2. 使用以下命令提交并推送到 GitHub：")
print(f"   git add .")
print(f"   git commit -m \"添加新文章: {article_title}\"")
print(f"   git push")
