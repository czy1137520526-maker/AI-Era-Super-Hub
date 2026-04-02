# 启动 Celery Worker 脚本

Write-Host "启动 ManjuFlow AI Celery Worker..." -ForegroundColor Cyan
Write-Host ""

# 进入后端目录
Set-Location backend

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& .\venv\Scripts\activate

# 启动 Celery Worker
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Celery Worker 已启动" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Broker: redis://localhost:6379/0" -ForegroundColor Cyan
Write-Host "Backend: redis://localhost:6379/0" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

celery -A app.workers.celery_app worker --loglevel=info
