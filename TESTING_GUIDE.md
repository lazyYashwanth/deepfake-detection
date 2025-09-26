# 🚀 COMPLETE TESTING SETUP GUIDE

## Quick Start (2 Steps)

### Step 1: Start Backend Server
1. Double-click: `start_simple_server.bat`
2. Wait for the message: "Running on http://localhost:7860"
3. Keep this terminal window open

### Step 2: Start Frontend Server
1. Double-click: `start_frontend.bat` 
2. Wait for the message about serving at port 8000
3. Open your browser to: http://localhost:8000

## What You'll See

- **Frontend**: http://localhost:8000 (Your web interface)
- **Backend API**: http://localhost:7860 (The server processing videos)

## Testing the System

1. **Open Frontend**: Go to http://localhost:8000
2. **Check Status**: The status indicator should show "Online" 
3. **Upload Video**: Select any MP4/MOV/AVI video file
4. **Click Analyze**: Wait 2-3 seconds for mock results
5. **View Results**: See the prediction percentage and verdict

## Expected Results

Since we're using the simplified server (mock mode), you'll see:
- Random confidence scores (70-95%)
- Random "FAKE" or "REAL" verdicts  
- Instant processing (2 second delay)

## Files Overview

### Backend Files:
- `app_simple.py` - Simplified server (currently running)
- `app.py` - Full ML model server (needs dependency fixes)
- `start_simple_server.bat` - Start backend
- `requirements.txt` - All dependencies

### Frontend Files:
- `index.html` - Main webpage
- `script.js` - Frontend logic (configured for localhost)
- `style.css` - Styling
- `start_frontend.bat` - Start frontend server

## Troubleshooting

### Backend Issues:
- If backend won't start, check Python environment
- Port 7860 must be free
- Check terminal for error messages

### Frontend Issues:
- If frontend won't load, try: http://127.0.0.1:8000
- Check that both servers are running
- Look for CORS errors in browser console

### Connection Issues:
- Ensure both servers are running
- Check Windows Firewall if needed
- Frontend is configured to connect to localhost:7860

## Next Steps

Once testing works with mock server:
1. Fix ML dependencies in `app.py`
2. Switch to the full ML model
3. Deploy to Hugging Face Spaces

## Ready to Test!

1. Run: `start_simple_server.bat`
2. Run: `start_frontend.bat`  
3. Open: http://localhost:8000
4. Upload a video and test!

🎉 Your deepfake detection system is ready for testing!
