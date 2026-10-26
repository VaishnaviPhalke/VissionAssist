$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    throw "Virtual environment missing. Run scripts\setup_windows.ps1 first."
}
if (-not (Test-Path .\models\yolov8n.pt)) {
    .\.venv\Scripts\python.exe scripts\download_model.py
}

Start-Process "http://localhost:8000"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
