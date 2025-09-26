# PowerShell script to start the Deepfake Detection API server
Write-Host "Starting Deepfake Detection API Server..." -ForegroundColor Green
Write-Host ""

# Change to the project directory
Set-Location "C:\Users\aruna\Downloads\hackathon files\Backednd"

# Check if virtual environment exists
$venvPath = "C:\Users\aruna\Downloads\hackathon files\Backednd\.venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found at: $venvPath" -ForegroundColor Red
    Write-Host "Please run: configure_python_environment first" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Starting Flask server..." -ForegroundColor Cyan
Write-Host "📍 Server will be available at: http://localhost:7860" -ForegroundColor Yellow
Write-Host "📝 API documentation at: http://localhost:7860/" -ForegroundColor Yellow
Write-Host "🔍 Health check at: http://localhost:7860/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Note: Currently using MOCK inference function" -ForegroundColor Magenta
Write-Host "   Replace mock_predict_on_video() with real ML model when ready" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "=" * 60

# Start the Flask server
& $venvPath app.py
