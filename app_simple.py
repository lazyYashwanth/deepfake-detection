"""
Simplified Deepfake Detection API for Testing

This version removes OpenCV dependencies to test basic Flask functionality
and can serve as a fallback while resolving ML model issues.
"""

import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# Helper Functions
# -------------------------
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def mock_predict_on_video(video_path):
    """
    Mock prediction function for testing the API without ML dependencies.
    """
    import random
    import time
    
    print(f"🔹 Processing video: {video_path}")
    
    # Simulate processing time
    time.sleep(2)
    
    # Simulate prediction
    confidence = random.uniform(70, 95)
    is_fake = random.choice([True, False])
    
    if is_fake:
        return f"Video is {confidence:.2f}% likely to be a FAKE."
    else:
        return f"Video is {(100-confidence):.2f}% likely to be REAL."

# -------------------------
# API Routes
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint that handles video upload and deepfake detection.
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request.'}), 400
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            return jsonify({'error': 'No file selected for upload.'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename to avoid conflicts
        unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the uploaded file
        file.save(file_path)
        print(f"📁 File saved to: {file_path}")
        
        try:
            # Process the video (using mock for now)
            prediction_result = mock_predict_on_video(file_path)
            
            # Return successful prediction
            response = {'prediction_result': prediction_result}
            print(f"✅ Prediction successful: {prediction_result}")
            
        except Exception as inference_error:
            # Handle model inference errors
            error_message = f"Model inference failed: {str(inference_error)}"
            print(f"❌ Inference error: {error_message}")
            response = {'error': error_message}
            return jsonify(response), 500
            
        finally:
            # Clean up: Delete the temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🗑️ Cleaned up file: {file_path}")
            except OSError as cleanup_error:
                print(f"⚠️ Warning: Could not delete file {file_path}: {cleanup_error}")
        
        return jsonify(response), 200
        
    except Exception as e:
        # Handle any unexpected errors
        error_message = f"Server error: {str(e)}"
        print(f"❌ Unexpected error: {error_message}")
        return jsonify({'error': error_message}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'deepfake-detection-api',
        'version': '1.0.0',
        'mode': 'testing'
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'service': 'Deepfake Digital Evidence Verifier API',
        'version': '1.0.0',
        'mode': 'Testing Mode (Mock Predictions)',
        'endpoints': {
            'predict': 'POST /predict - Upload video for deepfake detection',
            'health': 'GET /health - Health check',
        },
        'usage': 'Send POST request to /predict with video file in multipart/form-data format'
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DEEPFAKE DETECTION API SERVER (TESTING MODE)")
    print("=" * 60)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📊 Max file size: {MAX_CONTENT_LENGTH / (1024*1024)}MB")
    print(f"📹 Allowed extensions: {ALLOWED_EXTENSIONS}")
    print("⚠️  Mode: Testing with mock predictions")
    print("=" * 60)
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',  # Accept connections from any IP
        port=7860,       # Default port for Hugging Face Spaces
        debug=True       # Enable debug mode for development
    )
