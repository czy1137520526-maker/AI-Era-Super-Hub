# ManjuFlow AI 快速启动脚本
# 用于启动开发环境

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ManjuFlow AI - 开发环境启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "检查 Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python 未安装,请先安装 Python 3.10+" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
Write-Host "检查 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js 已安装: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js 未安装,请先安装 Node.js 18+" -ForegroundColor Red
    Write-Host "  下载地址: https://nodejs.org/" -ForegroundColor Cyan
    exit 1
}

# 检查 Docker (可选)
Write-Host "检查 Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✓ Docker 已安装: $dockerVersion" -ForegroundColor Green
    $dockerAvailable = $true
} catch {
    Write-Host "! Docker 未安装或未启动 (可选)" -ForegroundColor Yellow
    Write-Host "  用于运行 PostgreSQL, Redis, MinIO, ComfyUI" -ForegroundColor Cyan
    $dockerAvailable = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "选择启动模式:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 使用 Docker Compose (推荐)" -ForegroundColor White
Write-Host "2. 本地开发模式 (不使用 Docker)" -ForegroundColor White
Write-Host "3. 仅启动后端服务" -ForegroundColor White
Write-Host "4. 仅启动前端服务" -ForegroundColor White
Write-Host "0. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请选择 (0-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "启动 Docker Compose 服务..." -ForegroundColor Yellow

        if (-not $dockerAvailable) {
            Write-Host "✗ Docker 不可用,无法使用此模式" -ForegroundColor Red
            exit 1
        }

        Write-Host "启动 PostgreSQL, Redis, MinIO, ComfyUI..." -ForegroundColor Cyan
        Set-Location docker
        docker-compose up -d

        Write-Host ""
        Write-Host "等待服务启动..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10

        Write-Host ""
        Write-Host "✓ Docker 服务已启动" -ForegroundColor Green
        Write-Host "  - PostgreSQL: localhost:5432" -ForegroundColor White
        Write-Host "  - Redis: localhost:6379" -ForegroundColor White
        Write-Host "  - MinIO: localhost:9000" -ForegroundColor White
        Write-Host "  - ComfyUI: localhost:8188" -ForegroundColor White

        Write-Host ""
        Write-Host "下一步:" -ForegroundColor Cyan
        Write-Host "1. 在新终端启动后端: cd backend; python -m app.main" -ForegroundColor White
        Write-Host "2. 在新终端启动 Celery: cd backend; celery -A app.workers.celery_app worker" -ForegroundColor White
        Write-Host "3. 在新终端启动前端: cd frontend; npm run dev" -ForegroundColor White
    }

    "2" {
        Write-Host ""
        Write-Host "本地开发模式..." -ForegroundColor Yellow

        Write-Host ""
        Write-Host "请确保已启动以下服务:" -ForegroundColor Cyan
        Write-Host "  - PostgreSQL (localhost:5432)" -ForegroundColor White
        Write-Host "  - Redis (localhost:6379)" -ForegroundColor White
        Write-Host ""
        Write-Host "如未启动,可以使用 Docker 快速启动:" -ForegroundColor Yellow
        Write-Host "  docker run -d --name postgres -e POSTGRES_USER=manju -e POSTGRES_PASSWORD=manju123 -e POSTGRES_DB=manjuflow -p 5432:5432 postgres:14" -ForegroundColor White
        Write-Host "  docker run -d --name redis -p 6379:6379 redis:6" -ForegroundColor White

        Write-Host ""
        Write-Host "下一步:" -ForegroundColor Cyan
        Write-Host "1. 在新终端启动后端: cd backend; python -m app.main" -ForegroundColor White
        Write-Host "2. 在新终端启动 Celery: cd backend; celery -A app.workers.celery_app worker" -ForegroundColor White
        Write-Host "3. 在新终端启动前端: cd frontend; npm run dev" -ForegroundColor White
    }

    "3" {
        Write-Host ""
        Write-Host "启动后端服务..." -ForegroundColor Yellow

        Write-Host "检查后端依赖..." -ForegroundColor Cyan
        Set-Location backend

        if (-not (Test-Path "venv")) {
            Write-Host "创建虚拟环境..." -ForegroundColor Yellow
            python -m venv venv
        }

        Write-Host "激活虚拟环境..." -ForegroundColor Yellow
        & .\venv\Scripts\activate

        Write-Host "安装依赖..." -ForegroundColor Yellow
        pip install -r requirements.txt

        Write-Host ""
        Write-Host "启动 FastAPI 服务器..." -ForegroundColor Green
        Write-Host "访问: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""

        python -m app.main
    }

    "4" {
        Write-Host ""
        Write-Host "启动前端服务..." -ForegroundColor Yellow

        Set-Location frontend

        Write-Host "检查前端依赖..." -ForegroundColor Cyan
        if (-not (Test-Path "node_modules")) {
            Write-Host "安装依赖..." -ForegroundColor Yellow
            npm install
        }

        Write-Host ""
        Write-Host "启动 Next.js 开发服务器..." -ForegroundColor Green
        Write-Host "访问: http://localhost:3000" -ForegroundColor Cyan
        Write-Host ""

        npm run dev
    }

    "0" {
        Write-Host ""
        Write-Host "退出" -ForegroundColor Yellow
        exit 0
    }

    default {
        Write-Host ""
        Write-Host "✗ 无效选择" -ForegroundColor Red
        exit 1
    }
}
