@echo off
echo ========================================
echo  DEEPFAKE DETECTION API SERVER
echo ========================================
echo Starting the backend server...
echo.

cd /d "C:\Users\aruna\Downloads\hackathon files\Backednd"

echo Loading ML models (this may take a minute)...
"C:\Users\aruna\Downloads\hackathon files\Backednd\.venv\Scripts\python.exe" app.py

pause
