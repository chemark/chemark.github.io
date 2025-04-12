#!/usr/bin/env python3
"""
从Pages文件更新博客的脚本

使用方法:
python3 update_blog_from_pages.py Pages文件路径.md.pages 文章URL名称 文章日期

例如:
python3 update_blog_from_pages.py ~/Documents/ChatGPT眼中的星树浩.md.pages chatgpt-view "2025年04月12日"
"""

import sys
import os
import re
import glob
import subprocess
from datetime import datetime
import json
import tempfile
import zipfile
import xml.etree.ElementTree as ET

# 检查参数
if len(sys.argv) < 4:
    print("使用方法: python3 update_blog_from_pages.py Pages文件路径.md.pages 文章URL名称 文章日期")
    print('例如: python3 update_blog_from_pages.py ~/Documents/ChatGPT眼中的星树浩.md.pages chatgpt-view "2025年04月12日"')
    sys.exit(1)

# 获取参数
pages_file_path = os.path.expanduser(sys.argv[1])
article_url_name = sys.argv[2]
article_date = sys.argv[3]

# 检查文件是否存在
if not os.path.exists(pages_file_path):
    print(f"错误: 文件 {pages_file_path} 不存在")
    sys.exit(1)

# 从Pages文件提取Markdown内容
def extract_markdown_from_pages(pages_file):
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 解压Pages文件（实际上是一个zip文件）
        try:
            with zipfile.ZipFile(pages_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 查找index.xml文件
            index_xml_path = os.path.join(temp_dir, 'index.xml')
            if not os.path.exists(index_xml_path):
                print("错误: 无法在Pages文件中找到index.xml")
                return None
            
            # 解析XML
            tree = ET.parse(index_xml_path)
            root = tree.getroot()
            
            # 提取文本内容
            # 注意：这是一个简化的实现，可能需要根据实际Pages文件结构调整
            text_elements = root.findall(".//sf:text", namespaces={'sf': 'http://developer.apple.com/namespaces/sf'})
            if not text_elements:
                # 尝试不同的命名空间
                text_elements = root.findall(".//*[local-name()='text']")
            
            if text_elements:
                content = ''.join(elem.text or '' for elem in text_elements)
                # 尝试提取标题
                title_match = re.search(r'^#\s+(.+?)(?:\n|$)', content)
                if title_match:
                    title = title_match.group(1)
                    return content, title
                else:
                    # 如果找不到Markdown标题，尝试从文件名提取
                    base_name = os.path.basename(pages_file)
                    title = os.path.splitext(base_name)[0].replace('.md', '')
                    # 在内容前添加标题
                    content = f"# {title}\n\n{content}"
                    return content, title
        except Exception as e:
            print(f"提取Pages内容时出错: {e}")
            
    # 如果无法提取内容，尝试使用文件名作为标题
    base_name = os.path.basename(pages_file)
    title = os.path.splitext(base_name)[0].replace('.md', '')
    return f"# {title}\n\n无法从Pages文件提取内容。请手动添加内容。", title

# 尝试从Pages文件提取Markdown内容
try:
    md_content, article_title = extract_markdown_from_pages(pages_file_path)
    if not md_content:
        print("错误: 无法从Pages文件中提取内容")
        sys.exit(1)
except Exception as e:
    print(f"处理Pages文件时出错: {e}")
    # 使用文件名作为标题
    base_name = os.path.basename(pages_file_path)
    article_title = os.path.splitext(base_name)[0].replace('.md', '')
    md_content = f"# {article_title}\n\n无法从Pages文件提取内容。请手动添加内容。"

# 如果无法从Pages文件提取内容，我们可以创建一个基本的Markdown文件
# 并提示用户手动编辑
if "无法从Pages文件提取内容" in md_content:
    print("警告: 无法自动提取Pages文件内容")
    print("创建基本Markdown文件，您可以稍后手动编辑HTML内容")

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

# 按日期排序文章（使用timestamp字段）
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

    <div class="article-content">
      {md_content.replace('# ' + article_title, '').strip()}
    </div>

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

# 提交并推送更改
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"添加新文章: {article_title}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("已提交并推送更改到GitHub")
except subprocess.CalledProcessError as e:
    print(f"Git操作失败: {e}")

print(f"文章已成功添加: {article_title}")
print(f"您可以在以下地址访问: https://chemark.github.io/posts/{article_url_name}/")
