# 启动后端服务脚本

Write-Host "启动 ManjuFlow AI 后端服务..." -ForegroundColor Cyan
Write-Host ""

# 进入后端目录
Set-Location backend

# 检查虚拟环境
if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& .\venv\Scripts\activate

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
$missing = $false
try {
    $version = pip show fastapi
    if (-not $version) {
        Write-Host "安装依赖..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
} catch {
    Write-Host "安装依赖..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# 启动 FastAPI
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  FastAPI 服务器已启动" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "API 地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "ReDoc: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python -m app.main
