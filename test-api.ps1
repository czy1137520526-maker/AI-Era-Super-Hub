# ManjuFlow AI API 测试脚本
# 用于测试各个 API 端点

$baseUrl = "http://localhost:8000/api/v1"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ManjuFlow AI - API 测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 测试健康检查
Write-Host "1. 测试健康检查..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
    Write-Host "✓ 健康检查通过" -ForegroundColor Green
    Write-Host "  状态: $($response.StatusCode)" -ForegroundColor White
    $data = $response.Content | ConvertFrom-Json
    Write-Host "  版本: $($data.version)" -ForegroundColor White
} catch {
    Write-Host "✗ 健康检查失败" -ForegroundColor Red
    Write-Host "  错误: $_" -ForegroundColor Red
}

Write-Host ""

# 测试创建项目 (需要先实现项目 API)
Write-Host "2. 测试创建项目..." -ForegroundColor Yellow
Write-Host "! 需要先实现项目 API" -ForegroundColor Cyan

Write-Host ""

# 测试生成脚本
Write-Host "3. 测试生成脚本..." -ForegroundColor Yellow
Write-Host "! 需要 project_id" -ForegroundColor Cyan
Write-Host "  示例: POST $baseUrl/scripts/generate" -ForegroundColor White

Write-Host ""

# 测试创建角色
Write-Host "4. 测试创建角色..." -ForegroundColor Yellow
Write-Host "! 需要 project_id" -ForegroundColor Cyan
Write-Host "  示例: POST $baseUrl/characters/" -ForegroundColor White

Write-Host ""

# 测试图像生成
Write-Host "5. 测试图像生成..." -ForegroundColor Yellow
Write-Host "! 需要 project_id 和 scene_id" -ForegroundColor Cyan
Write-Host "  示例: POST $baseUrl/render/generate/image" -ForegroundColor White

Write-Host ""

# 交互式测试
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "交互式 API 测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "使用 curl 或 Postman 进行详细测试:" -ForegroundColor Yellow
Write-Host ""
Write-Host "生成脚本:" -ForegroundColor White
Write-Host "curl -X POST `"$baseUrl/scripts/generate`" -ForegroundColor Cyan
Write-Host "  -H `"Content-Type: application/json`"" -ForegroundColor Cyan
Write-Host "  -d `"{`"project_id`":1,`"input_text`":`"测试脚本`",`"num_scenes`":5}`""" -ForegroundColor Cyan
Write-Host ""
Write-Host "创建角色:" -ForegroundColor White
Write-Host "curl -X POST `"$baseUrl/characters/`" -ForegroundColor Cyan
Write-Host "  -H `"Content-Type: application/json`"" -ForegroundColor Cyan
Write-Host "  -d `"{`"project_id`":1,`"name`":`"测试角色`",`"role`":`"protagonist`"}\`""" -ForegroundColor Cyan
Write-Host ""

Write-Host "或使用 Postman 导入 API Collection:" -ForegroundColor Yellow
Write-Host "  访问: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "完成!" -ForegroundColor Green
