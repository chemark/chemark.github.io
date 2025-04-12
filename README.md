# 星树浩的博客

这是我的个人博客，记录了我的一些想法和经验。

## 如何添加新文章

### 准备工作

1. 确保已安装Python 3和必要的依赖：

```bash
pip install markdown
```

### 使用Markdown编写文章

1. 在Pages或任何文本编辑器中使用Markdown格式编写文章
2. 文章的第一行必须是以`# `开头的标题，例如：`# 我的新文章标题`
3. 将文章保存为`.md`文件

### 使用脚本添加文章

使用`scripts/update_blog.py`脚本将Markdown文章添加到博客：

```bash
python3 scripts/update_blog.py 文章路径.md 文章URL名称 文章日期
```

例如：

```bash
python3 scripts/update_blog.py ~/Documents/我的新文章.md new-article "2025年02月15日"
```

参数说明：
- `文章路径.md`：Markdown文件的路径
- `文章URL名称`：文章在URL中的名称，例如`new-article`将生成`https://chemark.github.io/posts/new-article/`
- `文章日期`：文章的发布日期，格式为`YYYY年MM月DD日`

### 脚本功能

脚本会自动完成以下工作：

1. 读取Markdown文件并提取标题
2. 将Markdown转换为HTML
3. 创建文章目录和HTML文件
4. 更新所有页面的文章列表
5. 提交并推送更改到GitHub

### 文章模板

您可以使用`templates/article_template.md`作为编写新文章的模板。
