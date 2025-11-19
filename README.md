# 星树浩的博客

这是我的个人博客，使用纯静态 HTML 部署在 GitHub Pages 上。

🌐 **访问地址：** https://chemark.github.io

## 📁 项目结构

```
xingshuhao-blog/
├── 📁 img/               # 图片资源
├── 📁 posts/             # 博客文章（HTML格式）
│   ├── ai-coding-tools-setup/
│   ├── blog-guide/
│   ├── chatgpt-view/
│   ├── law-agent/
│   └── study/
├── 📁 scripts/           # 自动化脚本
│   └── update_blog.py    # 添加新文章的脚本
├── 📁 templates/         # 文章模板（本地）
├── 📁 metadata/          # 文章元数据（本地）
├── 📁 examples/          # 示例文件（本地）
├── 📄 index.html         # 博客首页
├── 📄 .gitignore         # Git 忽略配置
└── 📄 README.md          # 本文件
```

> **注意：** `templates/`, `metadata/`, `examples/` 文件夹仅在本地使用，不会推送到 GitHub。

## 🚀 如何添加新文章

### 1. 准备工作

确保已安装 Python 3 和必要的依赖：

```bash
pip install markdown
```

### 2. 编写 Markdown 文章

1. 使用任何文本编辑器（Obsidian、VSCode 等）编写 Markdown 文章
2. **重要：** 文章的第一行必须是 `# 标题` 格式，例如：
   ```markdown
   # 我的新文章标题

   这里是文章内容...
   ```
3. 保存为 `.md` 文件

💡 **提示：** 可以参考 `templates/article_template.md` 模板文件。

### 3. 使用脚本添加文章

运行 `update_blog.py` 脚本：

```bash
python3 scripts/update_blog.py 文章路径.md 文章URL名称 "文章日期"
```

**示例：**

```bash
python3 scripts/update_blog.py ~/Documents/我的新文章.md my-new-article "2025年11月19日"
```

**参数说明：**
- `文章路径.md` - Markdown 文件的完整路径
- `文章URL名称` - 文章的 URL 标识（英文，用连字符分隔），例如 `my-new-article`
- `文章日期` - 发布日期，格式：`YYYY年MM月DD日`

### 4. 脚本自动完成的工作

✅ 读取 Markdown 文件并提取标题
✅ 将 Markdown 转换为 HTML
✅ 创建文章目录 `posts/文章URL名称/index.html`
✅ 更新首页的文章列表
✅ 更新所有文章页面底部的文章列表
✅ 生成文章元数据文件（本地）

### 5. 检查并推送到 GitHub

脚本运行后会提示你下一步操作：

```bash
# 1. 检查生成的文章是否正确
# 2. 提交并推送到 GitHub：
git add .
git commit -m "添加新文章: 文章标题"
git push
```

### 6. 查看发布结果

等待 1-2 分钟让 GitHub Pages 部署，然后访问：
- 首页：https://chemark.github.io
- 新文章：https://chemark.github.io/posts/文章URL名称/

## 🛠️ 技术栈

- **托管平台：** GitHub Pages
- **内容格式：** 纯静态 HTML
- **文章编写：** Markdown
- **转换工具：** Python + markdown 库
- **版本控制：** Git

## 📝 注意事项

1. ⚠️ 文章的第一行必须是 `# 标题` 格式，否则脚本会报错
2. ⚠️ 文章 URL 名称建议使用英文和连字符，避免使用中文或特殊字符
3. ⚠️ 推送前请检查生成的 HTML 文件是否正确
4. ✅ `metadata/`, `templates/`, `examples/` 文件夹已在 `.gitignore` 中，不会被推送

## 📚 更多信息

详细的博客管理指南请参考 `博客搭建与管理指南.md`（本地文件）。
