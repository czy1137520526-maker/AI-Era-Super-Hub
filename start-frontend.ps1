# 启动前端服务脚本

Write-Host "启动 ManjuFlow AI 前端服务..." -ForegroundColor Cyan
Write-Host ""

# 进入前端目录
Set-Location frontend

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "安装依赖..." -ForegroundColor Yellow
    npm install
}

# 启动 Next.js
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Next.js 开发服务器已启动" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "应用地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

npm run dev
