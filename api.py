from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow import keras
import os

app = FastAPI(title="Construction Defect Detection API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None
MODEL_PATH = "model.keras"

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize to model input size (adjust if your model uses different size)
    image = image.resize((224, 224))
    
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_defect(img_array: np.ndarray) -> dict:
    """Make prediction using the loaded model"""
    if model is None:
        raise Exception("Model not loaded")
    
    # Get prediction
    prediction = model.predict(img_array, verbose=0)
    
    # Assuming binary classification: 0 = No Defect, 1 = Defect
    # Adjust based on your model's output
    has_defect = bool(prediction[0][0] > 0.5)
    confidence = float(prediction[0][0])
    
    return {
        "has_defect": has_defect,
        "confidence": confidence,
        "prediction": "Defect Detected" if has_defect else "No Defect"
    }

@app.on_event("startup")
async def load_model():
    """Load the model on startup"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = keras.models.load_model(MODEL_PATH)
            print(f"✓ Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"⚠ Warning: Model file not found at {MODEL_PATH}")
    except Exception as e:
        print(f"✗ Error loading model: {str(e)}")

@app.get("/")
def root():
    return {
        "message": "Construction Defect Detection API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "single_predict": "/predict",
            "bulk_predict": "/predict/bulk"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH
    }

@app.post("/predict")
async def predict_single(file: UploadFile = File(...)):
    """
    Single image prediction endpoint.
    Returns: prediction result
    """
    try:
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img_array = preprocess_image(image)
        
        # Make prediction
        result = predict_defect(img_array)
        
        return {
            "success": True,
            "prediction": result["prediction"],
            "has_defect": result["has_defect"],
            "confidence": result["confidence"]
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.post("/predict/bulk")
async def predict_bulk(files: List[UploadFile] = File(...)):
    """
    Bulk image prediction endpoint.
    Returns: JSON with image names and predictions
    """
    try:
        results = []
        
        for file in files:
            try:
                # Read and preprocess image
                contents = await file.read()
                image = Image.open(io.BytesIO(contents))
                img_array = preprocess_image(image)
                
                # Make prediction
                prediction_result = predict_defect(img_array)
                
                results.append({
                    "image_name": file.filename,
                    "prediction": prediction_result["prediction"]
                })
                
            except Exception as e:
                results.append({
                    "image_name": file.filename,
                    "prediction": f"Error: {str(e)}"
                })
        
        return {
            "success": True,
            "total_images": len(files),
            "results": results
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )