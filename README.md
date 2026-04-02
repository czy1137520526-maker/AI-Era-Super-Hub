# ManjuFlow AI - 漫剧智造局

> 从"剧本输入"到"动态漫剧成片"的全自动化 AI 制作平台

## 项目概述

ManjuFlow AI 是一个基于 Web 的 SaaS 平台,通过 AI 技术解决角色/画风一致性问题,并提供完整的多模态流程闭环。

## 核心功能

- 📝 **剧本与分镜智能工坊** - LLM 驱动的结构化剧本生成,支持拖拽排序
- 🎭 **角色与资产一致性中心** - LoRA 训练 + IP-Adapter + FaceID,确保跨镜头一致性
- 🎨 **高精度画面生成引擎** - ComfyUI 工作流集成,ControlNet 控制,批量生成
- 🎬 **动态化与视频合成** - LTX-2.3,唇形同步,自动运镜
- 🎵 **多模态配音与音效** - TTS 情感配音,AI BGM,字幕对齐
- ✂️ **智能剪辑与发布** - 时间轴非线性编辑器,一键渲染 MP4
- 🔗 **节点式工作流编辑器** - React Flow 可视化节点编辑,预设模板
- 📊 **实时进度推送** - WebSocket 实时任务进度更新

## 技术栈

### 前端
- **框架**: Next.js 15 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS + Framer Motion
- **组件**: shadcn/ui + React Flow
- **状态管理**: React Hooks + Zustand

### 后端
- **框架**: FastAPI (Python)
- **异步任务**: Celery + Redis
- **AI 引擎**: ComfyUI (WebSocket API)
- **编排**: LangChain

### 数据库
- **主数据库**: PostgreSQL (用户/项目数据)
- **向量数据库**: Pinecone/Milvus (风格/角色检索)
- **对象存储**: MinIO (图片/视频)
- **缓存**: Redis (任务队列/缓存)

### 基础设施
- **容器**: Docker + Docker Compose
- **编排**: Kubernetes (预留)
- **GPU**: NVIDIA A100/H100 集成

## 项目结构

```
manjuflow-ai/
├── frontend/          # Next.js 前端项目
│   ├── src/
│   │   ├── app/      # 页面路由
│   │   ├── components/ # React 组件
│   │   └── lib/      # 工具库
│   ├── package.json
│   └── tsconfig.json
├── backend/           # FastAPI 后端项目
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # ORM 模型
│   │   ├── schemas/  # Pydantic 模型
│   │   ├── services/ # 业务逻辑
│   │   └── workers/  # Celery 任务
│   ├── requirements.txt
│   └── main.py
├── comfyui/           # ComfyUI 工作流配置
│   └── workflows/     # JSON 工作流
├── docker/            # Docker 配置
│   └── docker-compose.yml
├── k8s/              # Kubernetes 配置
├── db/               # 数据库脚本
│   └── schema.sql
├── .env              # 环境变量
├── start-dev.ps1      # 交互式启动脚本
├── TESTING_GUIDE.md   # 测试和开发指南
└── README.md
```

## 快速开始

### 前置要求

- Docker & Docker Compose (推荐)
- Node.js 18+
- Python 3.10+
- GPU (NVIDIA,推荐 A100/H100)

### 🚀 一键启动 (Windows PowerShell)

```powershell
# 运行交互式启动脚本
.\start-dev.ps1
```

### 📝 详细步骤

#### 方式一: 使用 Docker Compose (推荐)

```bash
# 1. 启动所有服务
cd docker
docker-compose up -d

# 2. 初始化数据库
docker exec -it manjuflow-postgres psql -U manju -d manjuflow -f /docker-entrypoint-initdb.d/schema.sql

# 3. 启动后端 (在新终端)
cd ../backend
.\start-backend.ps1

# 4. 启动 Celery Worker (在新终端)
.\start-celery.ps1

# 5. 启动前端 (在新终端)
cd ../frontend
.\start-frontend.ps1
```

#### 方式二: 本地开发 (不使用 Docker)

```bash
# 1. 安装依赖
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

# 2. 启动服务
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python -m app.main

# Terminal 2 - Celery
cd backend
.\venv\Scripts\activate
celery -A app.workers.celery_app worker

# Terminal 3 - Frontend
cd frontend
npm run dev
```

### 访问地址

- 🎨 **前端应用**: http://localhost:3000
- 🔌 **后端 API**: http://localhost:8000
- 📚 **API 文档**: http://localhost:8000/docs
- 📊 **ComfyUI**: http://localhost:8188
- 🗄️ **MinIO Console**: http://localhost:9001

### 🧪 测试 API

```powershell
# 运行 API 测试脚本
.\test-api.ps1
```

### 📖 详细文档

- **测试和开发指南**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **项目总结**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 核心设计

### 架构原则

1. **无状态后端** - 便于横向扩展 GPU 节点
2. **异步优先** - 所有 AI 任务通过 Celery 异步处理
3. **强一致性** - Project -> Character -> LoRA 强关联
4. **可视化编辑** - React Flow 节点编辑器 + 预设模板
5. **实时反馈** - WebSocket 进度推送

### 数据流

```
用户输入 → 剧本生成 → 分镜解析 → 角色训练 → 画面生成 → 视频合成 → 导出
    ↓          ↓          ↓          ↓          ↓          ↓          ↓
  LLM      JSON解析   LoRA训练   ComfyUI    LTX-2.3     FFmpeg    MP4
```

## 开发指南

### 后端开发

```bash
cd backend
# 运行测试
pytest
# 代码格式化
black app/
# 类型检查
mypy app/
```

### 前端开发

```bash
cd frontend
# 运行测试
npm test
# 类型检查
npm run type-check
# 构建
npm run build
```

### ComfyUI 工作流

工作流配置位于 `comfyui/workflows/` 目录,可通过 ComfyUI 可视化编辑器导出。

## 部署

### Docker Compose

```bash
cd docker
docker-compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress/
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件

## 联系我们

- 项目主页: https://github.com/manjuflow/manjuflow-ai
- 文档: https://docs.manjuflow.ai
- 邮箱: contact@manjuflow.ai

---

**ManjuFlow AI** - 让 AI 漫剧创作更简单 🚀
