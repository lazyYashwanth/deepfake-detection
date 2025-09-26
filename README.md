# Deepfake Digital Evidence Verifier - Backend API

A Flask-based REST API for deepfake detection in video files using **EfficientNet-B0 + MTCNN**. Built for hackathon deployment on Hugging Face Spaces.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The installation includes PyTorch, OpenCV, and other ML dependencies. This may take several minutes.

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:7860`

### 3. Test the API

```bash
python test_api.py
```

## 🧠 Model Architecture

- **Face Detection:** MTCNN (Multi-task CNN)
- **Deepfake Classification:** EfficientNet-B0
- **Processing:** Up to 50 frames per video
- **Input Resolution:** 224x224 pixels per face
- **Device Support:** CUDA (GPU) / CPU automatic detection

## 📡 API Endpoints

### POST `/predict`

Main endpoint for deepfake detection.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: File with key `file` containing the video

**Response:**

**Success (200 OK):**
```json
{
  "prediction_result": "Video is 87.34% likely to be a FAKE."
}
```

**Error (400/500):**
```json
{
  "error": "No file part in the request."
}
```

### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "deepfake-detection-api",
  "version": "1.0.0",
  "device": "cuda",
  "model_loaded": true
}
```

### GET `/`

Root endpoint with API information including model details.

## 🧪 Testing with cURL

### Upload a video file:
```bash
curl -X POST -F "file=@your_video.mp4" http://localhost:7860/predict
```

### Health check:
```bash
curl http://localhost:7860/health
```

## 📁 Project Structure

```
Backend/
├── app.py                          # Main Flask application with ML model
├── inference.py                    # Original ML script (reference)
├── requirements.txt                # Python dependencies (ML + Flask)
├── Dockerfile                      # Docker configuration for deployment
├── test_api.py                     # API testing script
├── model_weights_info.txt          # Model weights information
├── start_server.py/.bat/.ps1       # Server startup scripts
└── README.md                       # This file
```

## 🔧 Configuration

- **Upload folder:** `uploads/` (auto-created)
- **Max file size:** 100MB
- **Allowed formats:** mp4, avi, mov, mkv, webm
- **Default port:** 7860 (Hugging Face Spaces compatible)
- **Max frames processed:** 50 per video
- **Device:** Auto-detects CUDA/CPU

## 🎯 Model Weights

The application supports custom trained weights:

1. **Custom Weights:** Place `efficientnet_b0_epoch_15_loss_0.158.pth` in the project root
2. **Fallback:** Uses ImageNet-pretrained EfficientNet if custom weights not found
3. **Automatic Detection:** The app automatically detects and loads available weights

## 🚀 Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Upload all files to the Space
3. Add model weights file if available
4. The Docker container will automatically build and deploy

### Local Docker

```bash
docker build -t deepfake-api .
docker run -p 7860:7860 deepfake-api
```

## 🔄 Model Processing Pipeline

1. **Video Loading:** OpenCV loads and processes video frames
2. **Face Detection:** MTCNN detects faces in each frame
3. **Face Extraction:** Crops and resizes faces to 224x224
4. **Preprocessing:** Normalizes images for EfficientNet
5. **Inference:** EfficientNet classifies each face as real/fake
6. **Aggregation:** Averages predictions across all detected faces
7. **Result:** Returns confidence percentage and classification

## 🛠️ Features

- ✅ Real ML model integration (EfficientNet-B0 + MTCNN)
- ✅ GPU acceleration support (CUDA)
- ✅ Batch face processing per video
- ✅ Robust error handling for video/model issues
- ✅ Automatic device detection (GPU/CPU)
- ✅ File upload validation and cleanup
- ✅ Production-ready logging and monitoring
- ✅ Docker deployment configuration
- ✅ Comprehensive test suite

## 🔒 Security Notes

- Files are validated by extension and processed safely
- Temporary files are automatically cleaned up
- Model runs in evaluation mode (no training)
- File size limits prevent resource exhaustion
- GPU memory is managed automatically

## 🐛 Error Handling

The API handles various scenarios:

- **Missing file:** 400 error with JSON response
- **Invalid file type:** 400 error with allowed types
- **Video processing errors:** 500 error with details
- **No faces detected:** Informative message returned
- **Model inference failures:** Proper error logging and response
- **File cleanup issues:** Warning logs, doesn't affect response

## � Performance

- **Processing Speed:** ~2-10 seconds per video (depends on length, faces, device)
- **Memory Usage:** Optimized for server deployment
- **Scalability:** Stateless design allows horizontal scaling
- **Device Support:** Automatic CUDA/CPU switching

## 🎯 Production Ready

This backend is fully production-ready with:

- Real deepfake detection using state-of-the-art models
- Comprehensive error handling and logging
- Docker containerization for deployment
- Health monitoring endpoints
- Automatic resource cleanup
- GPU acceleration support
- Frontend integration ready
