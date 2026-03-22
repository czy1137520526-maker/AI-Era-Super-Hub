# AI Era Super-Hub · AI 时代超级导航

> 一个入口，连接所有 AI

聚合主流 AI 工具（通义千问、豆包、ChatGPT、Claude、Gemini 等）的高效搜索导航首页。

## ✨ 功能特性

- **Omni-Search 搜索框** — 打开即聚焦，输入直接跳转目标 AI
- **Tab 切换** — 一键切换搜索目标（通义千问、Perplexity、秘塔 AI 等）
- **快捷指令系统** — 输入 `/` 呼出跳转菜单，支持键盘导航
- **Bento Box 布局** — 模块化卡片，深色模式优先
- **自定义工具** — 前端界面添加自定义网址，LocalStorage 持久化
- **响应式设计** — 移动端双列，平板三列，桌面四列

## 🤖 已收录 AI 工具

| 分类 | 工具 |
|------|------|
| 💬 对话类 | ChatGPT · Claude · Gemini · 通义千问 · 豆包 · 海螺 AI |
| 🔍 搜索类 | Perplexity · 秘塔 AI |
| ⚡ 生产力 | Cursor · Notion AI · Gamma |

## ⌨️ 快捷指令

| 指令 | 目标 |
|------|------|
| `/gpt` | ChatGPT |
| `/ty` | 通义千问 |
| `/db` | 豆包 |
| `/pp` | Perplexity |
| `/mt` | 秘塔 AI |
| `/cur` | Cursor |

## 🚀 使用方式

直接用浏览器打开 `index.html` 即可，无需构建，无需服务器。

## 🗄️ 数据结构

兼容 QClaw / 腾讯云开发 `AI_Tools` 集合字段，支持迁移至云数据库。

```json
{
  "id": "string",
  "name": "string",
  "category": "chat | search | image | productivity",
  "logo_url": "string",
  "target_url": "string",
  "search_suffix": "string",
  "description": "string",
  "priority": "number"
}
```

## 🔌 API 扩展

代码中预留 `API_ADAPTERS` 接口，未来可直接接入豆包、通义千问 API 实现站内问答。

---

MIT License · Built with ❤️ by czy1137520526-maker
