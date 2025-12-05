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
import json

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
LABEL_MAP_PATH = "label_map.json"

# Class labels mapping (will be loaded from file)
class_labels = {}
idx_to_label = {}

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction - matches training preprocessing exactly"""
    # Convert to RGB if necessary (same as ImageDataGenerator)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize to 128x128 (same as IMAGE_SIZE in notebook)
    image = image.resize((128, 128))
    
    # Convert to array and normalize to [0, 1] (same as rescale=1./255)
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_defect(img_array: np.ndarray) -> dict:
    """Make prediction using the loaded model"""
    if model is None:
        raise Exception("Model not loaded")
    
    # Log input shape for debugging
    print(f"Input array shape: {img_array.shape}, range: [{img_array.min():.3f}, {img_array.max():.3f}]")
    
    # Get prediction - returns probabilities for all 7 classes
    prediction = model.predict(img_array, verbose=0)
    
    # Log raw predictions
    print(f"Raw predictions: {prediction[0]}")
    print(f"Sum of probabilities: {prediction[0].sum():.4f}")
    
    # Get the class with highest probability
    predicted_class_idx = int(np.argmax(prediction[0]))
    confidence = float(np.max(prediction[0]))
    
    # Map index to class name
    predicted_class = idx_to_label.get(predicted_class_idx, "Unknown")
    
    print(f"Predicted: {predicted_class} (index {predicted_class_idx}) with confidence {confidence:.4f}")
    
    # Determine if it's a defect (anything except 'normal')
    has_defect = (predicted_class.lower() != "normal")
    
    return {
        "has_defect": has_defect,
        "defect_type": predicted_class,
        "confidence": confidence,
        "prediction": f"{predicted_class.replace('_', ' ').title()}" + (" (Defect Detected)" if has_defect else " (No Defect)"),
        "all_probabilities": {
            idx_to_label[i]: float(prediction[0][i]) for i in range(len(prediction[0]))
        }
    }

@app.on_event("startup")
async def load_model():
    """Load the model and label mapping on startup"""
    global model, class_labels, idx_to_label
    try:
        # Load model
        if os.path.exists(MODEL_PATH):
            model = keras.models.load_model(MODEL_PATH)
            print(f"✓ Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"⚠ Warning: Model file not found at {MODEL_PATH}")
        
        # Load label mapping
        if os.path.exists(LABEL_MAP_PATH):
            with open(LABEL_MAP_PATH, 'r') as f:
                class_labels = json.load(f)
                # Create reverse mapping: index -> label
                idx_to_label = {v: k for k, v in class_labels.items()}
                print(f"✓ Label mapping loaded: {class_labels}")
        else:
            print(f"⚠ Warning: Label map not found at {LABEL_MAP_PATH}")
            # Fallback labels
            idx_to_label = {0: "algae", 1: "major_crack", 2: "minor_crack", 
                          3: "normal", 4: "peeling", 5: "spalling", 6: "stain"}
            
    except Exception as e:
        print(f"✗ Error loading model/labels: {str(e)}")

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
        "model_path": MODEL_PATH,
        "classes": list(class_labels.keys()) if class_labels else []
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
            "defect_type": result["defect_type"],
            "confidence": result["confidence"],
            "all_probabilities": result["all_probabilities"]
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
                    "prediction": prediction_result["prediction"],
                    "defect_type": prediction_result["defect_type"],
                    "confidence": prediction_result["confidence"],
                    "has_defect": prediction_result["has_defect"]
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