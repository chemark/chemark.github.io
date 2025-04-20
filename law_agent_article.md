# 我如何用国产大模型构建一个法规智能体（并踩了 7 个坑）

> 一次从 0 到 1 的认知系统构建实验  
> by [chemark](https://github.com/chemark)

---

## 🧠 起点：一个理论引发的好奇

我在网上看到一个观点：Meta 把 Llama 称为"开源"，可能是因为欧盟《人工智能法案》（AI Act）对"开源模型"有特殊豁免条款，而这些豁免并不要求符合 OSI 的开源定义。

我不想只听别人说，我想自己验证。

于是我决定：

- 抓取 AI Act 的原文
- 提取所有提到 "open source" 的段落
- 用大模型分析它的定义、豁免条件、合规边界
- 全流程自己跑，不依赖 OpenAI，不用 ChatGPT 网页版

---

## 🛠️ 技术栈选型

- **MacBook 本地终端**：一切从命令行开始，干净、可控  
- **curl + lynx**：抓取并转为纯文本  
- **grep + ttok**：关键词提取 + token 估算  
- **SiliconFlow + DeepSeek-R1-Distill-Qwen-7B**：国产大模型，免费，支持 32K 上下文  
- **Python + OpenAI SDK（兼容接口）**：调用逻辑清晰，易于扩展  

---

## 🧩 全流程拆解 + 我踩过的坑

### 1. 抓取法规原文

```bash
curl 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689' > ai_act.html
lynx -dump ai_act.html > ai_act.txt
```

问题 1：lynx 报错找不到命令✅ 解决：先安装 Homebrew，再安装 lynx
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install lynx
```

### 2. 提取关键词段落
```bash
grep -i -C 5 'open source' ai_act.txt > open_source_mentions.txt
```

问题 2：提取结果是空的✅ 解决：改用更宽松的关键词
```bash
grep -i -C 5 'open' ai_act.txt > open_source_mentions.txt
```

### 3. 估算 token 数量
```bash
ttok < open_source_mentions.txt
```

问题 3：ttok 没装✅ 解决：
```bash
pip install ttok
```

### 4. 编写 Python 脚本调用模型
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.siliconflow.cn/v1",
    api_key="sk-你的密钥"
)

with open("open_source_mentions.txt", "r", encoding="utf-8") as f:
    content = f.read()

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    messages=[
        {"role": "system", "content": "你是一位法律分析助手，擅长从法规中提取结构化信息。"},
        {"role": "user", "content": f"""请总结以下段落中关于 open source 的定义、豁免条件、许可证要求、对模型发布者的影响：

{content}
"""}
    ],
    temperature=0.3,
    max_tokens=2048
)

print(response.choices[0].message.content)
```

### 5. 模型调用失败：400 错误

问题 4：BadRequestError: model does not exist✅ 解决：模型名必须精确写成：`model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"`

### 6. 脚本报错：SyntaxError: invalid decimal literal

问题 5：我写了 ‎⁠max_tokens = 16,384⁠✅ 解决：Python 不支持逗号分隔数字，改成：max_tokens = 16384

### 7. 模型输出为空

问题 6：终端没报错，但输出是空的✅ 解决：‎⁠open_source_mentions.txt⁠ 是空的，重新提取关键词并确认文件非空。

## ✅ 最终输出（节选）

模型输出了以下关键点：
- 法规中并未列出具体许可证（如 MIT、GPL），而是用功能性定义来界定"免费和开源"
- 如果模型的参数、架构、使用信息是公开的，并允许复制、修改、再分发，即可视为"开源"
- 即使要求署名或遵守相同分发条款，也不影响其"开源"地位
- 某些情况下，开源模型可豁免高风险 AI 系统的监管要求

## 🧠 我的思考

这次实验让我意识到：
- 大模型不是答案，它是认知压缩器
- 法规不是障碍，它是产品设计的边界条件
- 国产模型完全可以胜任结构化语义任务
- 构建认知系统的关键，不是 prompt，而是数据链 + 调度逻辑

## 🚀 下一步我想做什么？
- 把这套流程打包成 CLI 工具
- 支持多模型（OpenAI / Claude / DeepSeek）对比分析
- 做一个"法规摘要 API"，输入链接，输出结构化摘要
- 构建一个"模型许可证合规性检查器"

## 💬 如果你也想试试

欢迎 fork 我的 repo  https://github.com/chemark/chemark.github.io，或者留言交流。
