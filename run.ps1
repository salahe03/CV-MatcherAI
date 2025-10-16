# CV-to-Job Matcher - Run Script
# This script starts the FastAPI server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting CV-to-Job Matcher API Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment if it exists
if (Test-Path "venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Start the server
Write-Host "Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "Interactive API docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
