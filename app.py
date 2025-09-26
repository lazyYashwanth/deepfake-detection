"""
Deepfake Digital Evidence Verifier - Backend API

This Flask server provides a single endpoint /predict that receives video files,
processes them through a deepfake detection model, and returns JSON results.

Built for hackathon deployment on Hugging Face Spaces.
"""

import os
import cv2
import torch
import numpy as np
import torch.nn as nn
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from torchvision import transforms
from facenet_pytorch import MTCNN
from efficientnet_pytorch import EfficientNet

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# ML Model Setup (One-time initialization)
# -------------------------
print("🔹 Initializing Deepfake Detection Model...")

# Device setup
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# Load MTCNN face detector
print("🔹 Loading MTCNN face detector...")
mtcnn = MTCNN(keep_all=True, device=DEVICE)

# Build EfficientNet-B0 model
print("🔹 Building EfficientNet-B0...")
model = EfficientNet.from_name("efficientnet-b0")
model._fc = nn.Linear(model._fc.in_features, 1)

# Optional: Custom weights path
WEIGHT_PATH = "efficientnet_b0_epoch_15_loss_0.158.pth"
if os.path.exists(WEIGHT_PATH):
    print(f"✅ Loading custom weights from {WEIGHT_PATH}")
    state_dict = torch.load(WEIGHT_PATH, map_location=DEVICE)
    model.load_state_dict(state_dict)
else:
    print("⚠️ No custom weights found. Using ImageNet-pretrained EfficientNet instead.")
    model = EfficientNet.from_pretrained("efficientnet-b0")
    model._fc = nn.Linear(model._fc.in_features, 1)

model = model.to(DEVICE)
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

print("✅ Model initialization complete!")

# -------------------------
# Helper Functions
# -------------------------
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_on_video(video_path, max_frames=50):
    """
    Real deepfake detection function using EfficientNet and MTCNN.
    
    Args:
        video_path (str): Path to the video file to analyze
        max_frames (int): Maximum number of frames to process
        
    Returns:
        str: Prediction result string
        
    Raises:
        Exception: If processing fails
    """
    print(f"🔹 Processing video: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Could not open video file")
        
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_process = min(max_frames, frame_count)
    
    predictions = []
    idx = 0
    
    print(f"🔹 Processing {frames_to_process} frames...")
    
    while idx < frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break
        idx += 1
        
        # Detect faces
        try:
            boxes, _ = mtcnn.detect(frame)
            if boxes is None:
                continue
                
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                
                # Ensure coordinates are within frame bounds
                h, w = frame.shape[:2]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                face = frame[y1:y2, x1:x2]
                if face.size == 0:
                    continue
                    
                face_tensor = transform(face).unsqueeze(0).to(DEVICE)
                
                with torch.no_grad():
                    output = model(face_tensor)
                    pred = torch.sigmoid(output).item()
                    predictions.append(pred)
                    
        except Exception as face_error:
            print(f"Warning: Face detection error on frame {idx}: {face_error}")
            continue
    
    cap.release()
    
    if not predictions:
        return "⚠️ No face detected in video."
    
    avg_score = np.mean(predictions)
    confidence = avg_score * 100
    
    # Format result similar to mock function
    if avg_score > 0.5:
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
    
    Expected request: POST with multipart/form-data containing 'file' key
    Returns: JSON response with prediction result or error message
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
            # Process the video through the deepfake detection model
            prediction_result = predict_on_video(file_path)
            
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
        'device': DEVICE,
        'model_loaded': True
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'service': 'Deepfake Digital Evidence Verifier API',
        'version': '1.0.0',
        'model': 'EfficientNet-B0 + MTCNN',
        'device': DEVICE,
        'endpoints': {
            'predict': 'POST /predict - Upload video for deepfake detection',
            'health': 'GET /health - Health check',
        },
        'usage': 'Send POST request to /predict with video file in multipart/form-data format'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DEEPFAKE DETECTION API SERVER")
    print("=" * 60)
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📊 Max file size: {MAX_CONTENT_LENGTH / (1024*1024)}MB")
    print(f"📹 Allowed extensions: {ALLOWED_EXTENSIONS}")
    print(f"🖥️ Device: {DEVICE}")
    print(f"🧠 Model: EfficientNet-B0 + MTCNN")
    print("=" * 60)
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',  # Accept connections from any IP (required for deployment)
        port=7860,       # Default port for Hugging Face Spaces
        debug=True       # Enable debug mode for development
    )
