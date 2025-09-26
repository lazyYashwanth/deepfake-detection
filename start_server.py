"""
Development server startup script for Deepfake Detection API

This script sets up the environment and starts the Flask development server.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")
    try:
        import flask
        import werkzeug
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_upload_directory():
    """Ensure the upload directory exists."""
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print(f"✓ Created upload directory: {upload_dir}")
    else:
        print(f"✓ Upload directory exists: {upload_dir}")

def start_server():
    """Start the Flask development server."""
    print("\n" + "="*50)
    print("STARTING DEEPFAKE DETECTION API SERVER")
    print("="*50)
    
    if not check_dependencies():
        return False
    
    create_upload_directory()
    
    print("\n🚀 Starting Flask server...")
    print("📍 Server will be available at: http://localhost:7860")
    print("📝 API documentation at: http://localhost:7860/")
    print("🔍 Health check at: http://localhost:7860/health")
    print("\n⚠️  Note: Currently using MOCK inference function")
    print("   Replace mock_predict_on_video() with real ML model when ready")
    print("\n" + "="*50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(
            host='0.0.0.0',
            port=7860,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_server()
    sys.exit(0 if success else 1)
