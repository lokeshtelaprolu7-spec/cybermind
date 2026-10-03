# CyberMIND — Dual-Stack One-Click Launcher for Windows
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🛡️  CyberMIND Autonomous Cybersecurity Digital Twin" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Determine if running from noble-hubble root or cybermind folder
if (Test-Path "$ScriptDir\cybermind\backend") {
    $BackendDir = "$ScriptDir\cybermind\backend"
    $FrontendDir = "$ScriptDir\cybermind\frontend"
} else {
    $BackendDir = "$ScriptDir\backend"
    $FrontendDir = "$ScriptDir\frontend"
}

# 1. Start FastAPI Backend
Write-Host "[1/2] Launching Backend on http://localhost:8000..." -ForegroundColor Green
$BackendProcess = Start-Process -FilePath "$BackendDir\.venv\Scripts\python.exe" `
    -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" `
    -WorkingDirectory "$BackendDir" `
    -PassThru

# 2. Start Next.js Frontend
Write-Host "[2/2] Launching Frontend on http://localhost:3000..." -ForegroundColor Green
$env:Path = "C:\Program Files\nodejs;" + $env:Path
$FrontendProcess = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c npm start" `
    -WorkingDirectory "$FrontendDir" `
    -PassThru

Write-Host "`nCyberMIND is running!" -ForegroundColor Yellow
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "`nPress Ctrl+C or close the terminal to stop processes." -ForegroundColor Gray
