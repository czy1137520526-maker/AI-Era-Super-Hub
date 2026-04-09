# 🤖 AI Era Super-Hub — 国内外 AI 模型导航

> 一站式发现、对比、直达国内外主流 AI 模型，支持地区分类、搜索过滤与用户自定义提交

## 项目简介

**AI Era Super-Hub** 是一个纯静态的 AI 模型导航网站（单文件 `index.html`），帮助用户快速找到并访问国内外主流大语言模型、绘图模型等 AI 工具。无需后端，部署极简，打开即用。

## ✨ 核心功能

- 🇨🇳🌍 **国内外分类展示** — 内置 region 字段，默认双栏并排展示国内与国外模型
- 🔍 **多维搜索** — 支持按名称、简介、标签、地区关键词搜索（如：输入「国内 绘图」精准筛选）
- 🏷️ **地区筛选 Tab** — 全部 / 国内 / 国外 三档快速切换
- ➕ **用户提交模型** — 表单支持填写名称、官网、简介、地区、能力标签，数据本地持久化
- ✏️ **编辑 / 报错** — 卡片悬停即可对自定义模型编辑，对内置模型一键反馈报错
- 📱 **全响应式** — 桌面 / 平板 / 手机三档断点，移动端友好

## 🗂️ 预置模型数据

### 🇨🇳 国内模型

| 模型 | 公司 | 能力标签 |
|------|------|----------|
| DeepSeek | 深度求索 | 推理、代码、文本 |
| Kimi（月之暗面） | 月之暗面 | 文本、多模态、写作 |
| 通义千问 | 阿里云 | 文本、代码、多模态 |
| 豆包 | 字节跳动 | 文本、写作、多模态 |
| 文心一言 | 百度 | 文本、绘图、代码 |
| 智谱清言 | 智谱AI | 文本、推理、代码 |
| 讯飞星火 | 科大讯飞 | 文本、语音、多模态 |
| 混元 | 腾讯 | 文本、搜索、多模态 |
| MiniMax / 海螺 | MiniMax | 视频、语音、绘图 |

### 🌍 国外模型

| 模型 | 公司 | 能力标签 |
|------|------|----------|
| ChatGPT | OpenAI | 文本、代码、写作 |
| Claude | Anthropic | 文本、推理、写作 |
| Gemini | Google | 多模态、搜索、文本 |
| Copilot | Microsoft | 代码、写作、搜索 |
| Llama | Meta | 文本、代码、推理 |
| Perplexity | Perplexity AI | 搜索、文本 |
| Midjourney | Midjourney | 绘图 |
| Stable Diffusion | Stability AI | 绘图 |
| Grok | xAI | 搜索、文本、推理 |

## 🚀 快速开始

无需安装任何依赖，直接打开 `index.html` 即可在浏览器运行。

```bash
# 克隆仓库
git clone https://github.com/czy1137520526-maker/AI-Era-Super-Hub.git

# 直接用浏览器打开
open index.html        # macOS
start index.html       # Windows
xdg-open index.html    # Linux
```

## 📁 项目结构

```
AI-Era-Super-Hub/
├── index.html          # 网站主文件（全部功能集成于此）
├── .env.example        # 环境变量模板（供参考，静态站无需配置）
├── README.md           # 项目说明
└── .gitignore          # Git 忽略规则
```

## 🛠️ 技术实现

- **纯原生 HTML / CSS / JavaScript** — 零依赖，无框架，无构建步骤
- **localStorage** — 用户自定义提交的模型数据本地持久化（键：`ai_hub_custom_tools_v2`）
- **响应式布局** — CSS Grid + Media Query，支持 900 / 600 / 380px 三档断点
- **实时搜索** — 关键词拆分后对 name / desc / tags / region 多字段联合匹配

## 📦 数据格式

每个模型条目的数据结构如下：

```js
{
  id: 'deepseek',           // 唯一标识符
  name: 'DeepSeek',         // 显示名称
  logo: '🔮',               // 展示 emoji
  region: 'CN',             // 'CN' 国内 | 'Global' 国外
  desc: '...',              // 简介
  tags: ['推理', '代码'],    // 能力标签
  url: 'https://...'        // 官网链接
}
```

## 🤝 贡献方式

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feat/add-new-model`）
3. 在 `index.html` 的 `AI_TOOLS_DB` 数组中按格式添加模型数据
4. 提交并推送（`git commit -m 'feat: 添加 xxx 模型'`）
5. 发起 Pull Request

也可以直接在网页上使用「➕ 提交新模型」功能，在本地添加模型。

## 📄 许可证

MIT License

---

**AI Era Super-Hub** — 让发现 AI 工具更简单 🚀
