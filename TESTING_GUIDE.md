# ManjuFlow AI - 测试和开发指南

## 环境要求

### 必需软件
1. **Python 3.10+** - 后端开发
2. **Node.js 18+ & npm** - 前端开发
3. **Docker & Docker Compose** - 容器化服务
4. **PostgreSQL 14+** - 数据库 (可选,可通过 Docker 启动)
5. **Redis 6+** - 缓存和消息队列 (可选,可通过 Docker 启动)
6. **Git** - 版本控制

### 可选软件
- **ComfyUI** - AI 工作流引擎 (本地运行)
- **GPU Driver** - NVIDIA GPU + CUDA (用于加速 AI 生成)

---

## 安装依赖

### 1. 安装 Python

#### Windows
```powershell
# 使用 winget 安装
winget install Python.Python.3.11

# 或访问 https://www.python.org/downloads/ 下载安装
# 安装时勾选 "Add Python to PATH"
```

#### 验证安装
```powershell
python --version
pip --version
```

### 2. 安装 Node.js

#### Windows
```powershell
# 使用 winget 安装
winget install OpenJS.NodeJS.LTS

# 或访问 https://nodejs.org/ 下载 LTS 版本
```

#### 验证安装
```powershell
node --version
npm --version
```

### 3. 安装 Docker Desktop

#### Windows
1. 访问 https://www.docker.com/products/docker-desktop
2. 下载并安装 Docker Desktop for Windows
3. 启动 Docker Desktop
4. 确保启用 WSL 2 后端

#### 验证安装
```powershell
docker --version
docker-compose --version
```

---

## 启动开发环境

### 方式一: 使用 Docker Compose (推荐)

#### 1. 启动所有服务
```powershell
cd c:\Users\czy\WorkBuddy\Claw\docker
docker-compose up -d
```

这会启动:
- PostgreSQL (端口 5432)
- Redis (端口 6379)
- MinIO (端口 9000)
- ComfyUI (端口 8188)

#### 2. 初始化数据库
```powershell
# 等待 PostgreSQL 启动 (约 10-20 秒)
docker exec -it manjuflow-postgres psql -U manju -d manjuflow -f /docker-entrypoint-initdb.d/schema.sql

# 或手动执行
cd c:\Users\czy\WorkBuddy\Claw
psql -h localhost -U manju -d manjuflow -f db/schema.sql
```

#### 3. 创建虚拟环境并安装后端依赖
```powershell
cd c:\Users\czy\WorkBuddy\Claw\backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 4. 配置环境变量
```powershell
# 创建 .env 文件
cd c:\Users\czy\WorkBuddy\Claw
copy .env.example .env

# 编辑 .env 文件 (根据需要修改配置)
notepad .env
```

#### 5. 启动后端服务
```powershell
cd c:\Users\czy\WorkBuddy\Claw\backend

# 确保虚拟环境已激活
.\venv\Scripts\activate

# 启动 FastAPI
python -m app.main
```

后端将在 http://localhost:8000 启动

#### 6. 启动 Celery Worker
```powershell
# 在新的 PowerShell 窗口中
cd c:\Users\czy\WorkBuddy\Claw\backend
.\venv\Scripts\activate

# 启动 Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
```

#### 7. 启动前端开发服务器
```powershell
# 在新的 PowerShell 窗口中
cd c:\Users\czy\WorkBuddy\Claw\frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 启动

### 方式二: 本地开发 (不使用 Docker)

#### 1. 启动 PostgreSQL
```powershell
# 使用 PostgreSQL 安装版或 Docker
docker run -d --name manjuflow-postgres -e POSTGRES_USER=manju -e POSTGRES_PASSWORD=manju123 -e POSTGRES_DB=manjuflow -p 5432:5432 postgres:14
```

#### 2. 启动 Redis
```powershell
docker run -d --name manjuflow-redis -p 6379:6379 redis:6
```

#### 3. 初始化数据库
```powershell
psql -h localhost -U manju -d manjuflow -f c:\Users\czy\WorkBuddy\Claw\db\schema.sql
```

#### 4-7. 同方式一的步骤 4-7

---

## 测试 API

### 1. 访问 API 文档
打开浏览器访问: http://localhost:8000/docs

### 2. 测试端点

#### 健康检查
```powershell
curl http://localhost:8000/health
```

#### 生成脚本 (需要先创建项目和角色)
```powershell
# POST /api/v1/scripts/generate
curl -X POST "http://localhost:8000/api/v1/scripts/generate" `
  -H "Content-Type: application/json" `
  -d '{
    "project_id": 1,
    "input_text": "小明去上学,路上遇到了小红",
    "style": "comic",
    "num_scenes": 5,
    "tone": "dramatic"
  }'
```

#### 创建角色
```powershell
# POST /api/v1/characters/
curl -X POST "http://localhost:8000/api/v1/characters/" `
  -H "Content-Type: application/json" `
  -d '{
    "project_id": 1,
    "name": "小明",
    "description": "主角",
    "role": "protagonist"
  }'
```

#### 生成图像
```powershell
# POST /api/v1/render/generate/image
curl -X POST "http://localhost:8000/api/v1/render/generate/image" `
  -H "Content-Type: application/json" `
  -d '{
    "project_id": 1,
    "scene_id": 1,
    "prompt": "小明走在上学的路上,阳光明媚",
    "width": 1024,
    "height": 1024,
    "num_inference_steps": 30,
    "guidance_scale": 7.5
  }'
```

#### 查询任务状态
```powershell
# GET /api/v1/render/jobs/{job_id}
curl http://localhost:8000/api/v1/render/jobs/1
```

---

## 测试前端

### 1. 访问应用
打开浏览器访问: http://localhost:3000

### 2. 测试功能
- 仪表盘页面 - 查看项目列表
- 项目详情页 - 查看工作流编辑器
- 切换 Tab - 测试剧本、角色、编辑器页面

### 3. 开发工具
- 打开浏览器开发者工具 (F12)
- 查看 Console 日志
- 检查 Network 请求

---

## 停止服务

### 停止 Docker 服务
```powershell
cd c:\Users\czy\WorkBuddy\Claw\docker
docker-compose down
```

### 停止后端和 Celery
在各自的 PowerShell 窗口中按 `Ctrl + C`

### 停止前端
在 PowerShell 窗口中按 `Ctrl + C`

---

## 常见问题

### 1. 端口冲突
如果端口被占用,修改 `.env` 文件中的端口配置:
```env
API_PORT=8001  # 改为其他端口
```

### 2. 数据库连接失败
确保 PostgreSQL 正在运行:
```powershell
docker ps | findstr postgres
```

### 3. Celery 无法连接 Redis
确保 Redis 正在运行:
```powershell
docker ps | findstr redis
```

### 4. 前端 npm install 失败
尝试清除缓存:
```powershell
cd c:\Users\czy\WorkBuddy\Claw\frontend
rm -rf node_modules package-lock.json
npm install
```

### 5. ComfyUI 连接失败
确保 ComfyUI 正在运行:
```powershell
curl http://localhost:8188
```

---

## 开发工具推荐

### VS Code 扩展
- Python - Python 语法高亮和调试
- ESLint - JavaScript/TypeScript 代码检查
- Prettier - 代码格式化
- Tailwind CSS IntelliSense - Tailwind CSS 自动完成
- REST Client - 测试 API

### Postman
- 用于测试 API 端点
- 下载: https://www.postman.com/downloads/

---

## 下一步开发

1. **用户认证** - 实现 JWT 登录注册
2. **WebSocket** - 实时进度推送
3. **LLM 集成** - 接入 Qwen/DeepSeek API
4. **ComfyUI 实际调用** - 测试 AI 生成流程
5. **前端 API 集成** - 完整的前后端通信
6. **文件上传** - MinIO 集成
7. **视频编辑器** - 实现时间轴编辑器

---

## 日志和调试

### 后端日志
FastAPI 日志会输出到控制台

### Celery 日志
Celery Worker 日志会输出到控制台

### Docker 日志
```powershell
# 查看所有容器日志
docker-compose logs

# 查看特定服务日志
docker-compose logs postgres
docker-compose logs redis
docker-compose logs comfyui
```

---

**祝开发顺利!** 🚀
