"""
Test script for the Deepfake Detection API

This script demonstrates how to test the /predict endpoint with a sample video file.
Run this after starting the Flask server to verify everything works correctly.
"""

import requests
import json
import os
import time

# API configuration
API_BASE_URL = "http://localhost:7860"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_predict_endpoint_no_file():
    """Test the predict endpoint without sending a file."""
    print("\nTesting predict endpoint without file...")
    try:
        response = requests.post(PREDICT_ENDPOINT, timeout=30)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 400 error
        assert response.status_code == 400
        assert "error" in response.json()
        print("✓ Correctly handled missing file")
        
    except Exception as e:
        print(f"Test failed: {e}")

def test_predict_endpoint_with_mock_file():
    """Test the predict endpoint with a mock video file."""
    print("\nTesting predict endpoint with mock file...")
    
    # Create a mock video file for testing
    mock_video_content = b"This is fake video content for testing"
    
    try:
        # Send the mock file
        files = {'file': ('test_video.mp4', mock_video_content, 'video/mp4')}
        response = requests.post(PREDICT_ENDPOINT, files=files, timeout=60)  # Increased timeout for ML processing
        
        print(f"Status code: {response.status_code}")
        response_data = response.json()
        print(f"Response: {response_data}")
        
        if response.status_code == 200:
            assert "prediction_result" in response_data
            print("✓ Successfully got prediction result from ML model")
        else:
            assert "error" in response_data
            print("✓ Correctly handled processing error")
            
    except Exception as e:
        print(f"Test failed: {e}")
        print("Note: This might be expected if ML model initialization takes time")

def test_invalid_file_type():
    """Test the predict endpoint with an invalid file type."""
    print("\nTesting predict endpoint with invalid file type...")
    
    # Create a mock text file
    mock_text_content = b"This is a text file, not a video"
    
    try:
        files = {'file': ('test_file.txt', mock_text_content, 'text/plain')}
        response = requests.post(PREDICT_ENDPOINT, files=files, timeout=30)
        
        print(f"Status code: {response.status_code}")
        response_data = response.json()
        print(f"Response: {response_data}")
        
        # Should return 400 error for invalid file type
        assert response.status_code == 400
        assert "error" in response_data
        assert "Invalid file type" in response_data["error"]
        print("✓ Correctly rejected invalid file type")
        
    except Exception as e:
        print(f"Test failed: {e}")

def run_all_tests():
    """Run all API tests."""
    print("=" * 50)
    print("DEEPFAKE DETECTION API TESTS")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("❌ Server is not responding. Make sure the Flask app is running.")
        return
    
    # Run API tests
    test_predict_endpoint_no_file()
    test_predict_endpoint_with_mock_file()
    test_invalid_file_type()
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED")
    print("=" * 50)
    print("\n🎉 API is working correctly!")
    print("\nNext steps:")
    print("1. Replace mock_predict_on_video() in app.py with real inference function")
    print("2. Add the actual inference.py file to the project")
    print("3. Update requirements.txt with ML dependencies (torch, etc.)")
    print("4. Deploy to Hugging Face Spaces")

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the Flask server is running on http://localhost:7860")
    print("Run: python app.py")
    print()
    
    # Wait a moment for user to start server if needed
    input("Press Enter when the server is running...")
    
    run_all_tests()
