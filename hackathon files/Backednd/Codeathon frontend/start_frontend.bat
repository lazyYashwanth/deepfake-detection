@echo off
echo ========================================
echo  FRONTEND SERVER (http://localhost:8000)
echo ========================================
echo.
echo Starting frontend server...
echo Frontend will be available at: http://localhost:8000
echo.
echo Make sure the backend is running at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "C:\Users\aruna\Downloads\hackathon files\Backednd\Codeathon frontend"
python -m http.server 8000

pause
