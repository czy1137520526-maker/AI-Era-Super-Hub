# ManjuFlow AI (漫剧智造局) - 项目总结

## 项目概述

**ManjuFlow AI** 是一个从"剧本输入"到"动态漫剧成片"的全自动化AI漫剧制作平台,核心解决角色/画风一致性与多模态流程闭环问题。

---

## 技术架构

### 前端技术栈
- **框架**: Next.js 15 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **动画**: Framer Motion
- **节点编辑器**: React Flow
- **UI组件**: Radix UI + shadcn/ui
- **状态管理**: Zustand

### 后端技术栈
- **框架**: FastAPI (Python)
- **异步任务**: Celery + Redis
- **AI引擎**: ComfyUI (底层工作流执行)
- **数据库**: PostgreSQL
- **向量数据库**: Pinecone/Milvus
- **对象存储**: MinIO (S3兼容)
- **编排**: LangChain

### 基础设施
- **容器化**: Docker + Docker Compose
- **编排**: Kubernetes (K8s)
- **GPU**: NVIDIA A100/H100 集群集成

---

## 项目目录结构

```
c:\Users\czy\WorkBuddy\Claw\
├── backend/                          # 后端服务
│   ├── app/
│   │   ├── api/v1/                  # API 路由
│   │   │   ├── scripts.py           # 剧本生成 API
│   │   │   ├── characters.py        # 角色管理 API
│   │   │   ├── render.py            # 渲染/生成 API
│   │   │   └── __init__.py
│   │   ├── core/                    # 核心配置
│   │   │   └── config.py            # 应用配置
│   │   ├── db/                      # 数据库
│   │   │   └── session.py           # 数据库会话管理
│   │   ├── models/                  # SQLAlchemy ORM
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── character.py
│   │   │   ├── scene.py
│   │   │   ├── asset.py
│   │   │   └── render.py
│   │   ├── schemas/                 # Pydantic 模型
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── character.py
│   │   │   ├── scene.py
│   │   │   ├── script.py
│   │   │   ├── asset.py
│   │   │   └── render.py
│   │   ├── services/                # 业务逻辑服务
│   │   │   ├── comfy_service.py     # ComfyUI 集成
│   │   │   ├── script_service.py    # 剧本生成
│   │   │   └── character_service.py # 角色一致性
│   │   ├── workers/                 # Celery 异步任务
│   │   │   ├── celery_app.py        # Celery 配置
│   │   │   └── tasks.py            # 任务定义
│   │   └── main.py                 # FastAPI 入口
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                         # 前端应用
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/           # 仪表盘页面
│   │   │   ├── projects/[id]/      # 项目详情页
│   │   │   ├── globals.css         # 全局样式
│   │   │   ├── layout.tsx          # 根布局
│   │   │   └── page.tsx            # 首页
│   │   ├── components/
│   │   │   └── workflow/           # 工作流组件
│   │   │       ├── WorkflowEditor.tsx    # 核心节点编辑器
│   │   │       ├── ScriptNode.tsx       # 剧本生成节点
│   │   │       ├── ImageGenNode.tsx     # 图像生成节点
│   │   │       ├── VideoGenNode.tsx     # 视频生成节点
│   │   │       └── LoraTrainNode.tsx    # LoRA训练节点
│   │   ├── lib/
│   │   │   └── utils.ts            # 工具函数
│   │   └── types/
│   │       └── index.ts             # TypeScript 类型定义
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── Dockerfile
│
├── comfyui/                          # ComfyUI 配置
│   └── workflows/                   # 工作流 JSON 配置
│       ├── image_generation.json
│       ├── video_generation.json
│       ├── character_lora.json
│       └── script_to_scene.json
│
├── db/
│   └── schema.sql                    # 数据库初始化脚本
│
├── docker/
│   └── docker-compose.yml            # 容器编排配置
│
└── k8s/                             # Kubernetes 配置
    ├── deployments/
    ├── services/
    └── ingress/
```

---

## 核心模块

### 1. 剧本与分镜智能工坊
- **功能**: 接收用户文本/大纲,调用 LLM 生成结构化 JSON 脚本
- **API**: `POST /api/v1/scripts/generate`
- **输出格式**: `{ scene_id, description, characters, emotion, camera_angle, dialogue }`
- **UI**: WorkflowEditor 中的 ScriptNode

### 2. 角色与资产一致性中心
- **核心逻辑**:
  - 用户上传参考图 → 自动训练轻量级 LoRA
  - 使用 IP-Adapter + FaceID 锁定角色面部特征
  - 建立"资产库",存储角色三视图及常用背景素材
- **API**:
  - `POST /api/v1/characters/` - 创建角色
  - `POST /api/v1/characters/{id}/train-lora` - 训练 LoRA

### 3. 高精度画面生成引擎
- **集成**: 对接 ComfyUI 后端工作流
- **工作流**: 加载角色LoRA → 应用ControlNet → FLUX.1 生成 → 自动修复
- **API**: `POST /api/v1/render/generate/image`

### 4. 动态化与视频合成
- **技术**: LTX-2.3 视频生成模型
- **功能**: 静态图转微动效,唇形同步,自动运镜
- **API**: `POST /api/v1/render/generate/video`

### 5. 多模态配音与音效
- **功能**: TTS 情感配音,AI BGM 生成,字幕对齐
- **状态**: 设计完成,待实现具体 API

### 6. 智能剪辑与发布
- **UI**: 基于时间轴的非线性编辑器 (类似简化版 Premiere)
- **输出**: 一键渲染 MP4,适配抖音 (9:16), B站 (16:9)

---

## 数据库设计

### 核心表结构

1. **users** - 用户信息
2. **projects** - 项目信息
3. **characters** - 角色及 LoRA 模型
4. **scenes** - 分镜场景
5. **assets** - 资产 (图片、视频等)
6. **render_jobs** - 渲染任务

**关联关系**:
- Users (1) → Projects (N)
- Projects (1) → Characters (N)
- Projects (1) → Scenes (N)
- Projects (1) → Assets (N)
- Projects (1) → RenderJobs (N)

---

## 关键特性

### ✅ 已实现功能
1. 完整的后端 FastAPI 框架
2. PostgreSQL 数据库 Schema
3. Pydantic 模型和 SQLAlchemy ORM
4. Celery 异步任务系统
5. ComfyUI 服务集成框架
6. React Flow 节点编辑器
7. 前端 Next.js 15 项目结构
8. Docker Compose 容器编排
9. ComfyUI 工作流 JSON 配置

### 🚧 待实现功能
1. 用户认证与授权 (JWT)
2. LLM 实际调用 (Qwen/DeepSeek)
3. WebSocket 实时进度推送
4. 前端 API 集成
5. 视频编辑器 UI
6. MinIO 文件上传/下载
7. Kubernetes 部署配置

---

## 快速开始

### 1. 启动所有服务 (Docker Compose)
```bash
cd docker
docker-compose up -d
```

### 2. 初始化数据库
```bash
psql -h localhost -U manju -d manjuflow -f ../db/schema.sql
```

### 3. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### 4. 启动前端开发服务器
```bash
cd frontend
npm install
npm run dev
```

### 5. 启动 Celery Worker
```bash
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### 6. 启动 ComfyUI
```bash
# 在单独的终端中
cd comfyui
python main.py --listen 0.0.0.0 --port 8188
```

---

## API 端点

### 剧本生成
- `POST /api/v1/scripts/generate` - 生成脚本
- `GET /api/v1/scripts/project/{project_id}` - 获取项目脚本

### 角色管理
- `POST /api/v1/characters/` - 创建角色
- `GET /api/v1/characters/{id}` - 获取角色
- `PUT /api/v1/characters/{id}` - 更新角色
- `DELETE /api/v1/characters/{id}` - 删除角色
- `POST /api/v1/characters/{id}/train-lora` - 训练 LoRA
- `GET /api/v1/characters/project/{project_id}` - 获取项目角色

### 渲染与生成
- `POST /api/v1/render/generate/image` - 生成图像
- `POST /api/v1/render/generate/video` - 生成视频
- `GET /api/v1/render/jobs/{job_id}` - 获取任务状态
- `GET /api/v1/render/project/{project_id}/jobs` - 获取项目任务列表

---

## 环境变量配置

参考 `.env.example` 文件配置以下环境变量:

```env
# Database
DATABASE_URL=postgresql+asyncpg://manju:manju123@localhost:5432/manjuflow

# Redis
REDIS_URL=redis://localhost:6379/0

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=manjuflow-assets

# ComfyUI
COMFYUI_URL=http://localhost:8188

# LLM
LLM_PROVIDER=qwen
QWEN_API_KEY=your_api_key
```

---

## 架构设计亮点

### 1. 节点式工作流
- 前端集成 React Flow,允许高级用户自定义 ComfyUI 节点连线
- 小白用户可使用预设模板

### 2. 异步处理
- 所有 AI 生成任务通过 Celery 异步处理
- 前端通过 WebSocket 接收实时进度推送

### 3. 一致性优先
- 数据库设计保证 `Project_ID` → `Character_ID` → `Style_LoRA` 的强关联
- 确保跨镜头一致性

### 4. 可扩展性
- 后端无状态服务设计,支持横向扩展 GPU 节点
- 微服务架构,每个模块可独立部署和扩展

---

## 后续开发计划

1. **优先级 P0**:
   - 实现用户认证系统 (JWT)
   - 完成 WebSocket 进度推送
   - 前端 API 客户端集成

2. **优先级 P1**:
   - 实际 LLM API 调用
   - ComfyUI 工作流实际测试
   - 视频编辑器 UI 实现

3. **优先级 P2**:
   - MinIO 文件管理
   - Kubernetes 部署
   - 性能优化和监控

---

## 技术参考

- [Next.js 15 Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Flow Documentation](https://reactflow.dev)
- [ComfyUI Documentation](https://docs.comfyanonymous.io)
- [Celery Documentation](https://docs.celeryproject.org)

---

**项目创建日期**: 2026-03-23
**当前版本**: 0.1.0 (MVP)
**维护者**: ManjuFlow AI Team
