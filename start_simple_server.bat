@echo off
echo ========================================
echo  DEEPFAKE DETECTION API SERVER
echo ========================================
echo.
echo Starting simplified server for testing...
echo Frontend can connect at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "C:\Users\aruna\Downloads\hackathon files\Backednd"
"C:\Users\aruna\Downloads\hackathon files\Backednd\.venv\Scripts\python.exe" app_simple.py

pause
