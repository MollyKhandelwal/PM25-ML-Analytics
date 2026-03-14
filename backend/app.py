from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import os

app = FastAPI(
    title="PM2.5 Prediction API",
    description="Machine Learning API for PM2.5 Pollution Prediction",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PredictionRequest(BaseModel):
    year: int
    region: str
    geographic_mean_pm25: float
    population_coverage: float
    geographic_coverage: float
    pop_pct_5: float
    pop_pct_10: float
    pop_pct_15: float

class PredictionResponse(BaseModel):
    predicted_pm25: float
    region: str
    year: int
    model_name: str
    confidence: str

# Load model (placeholder)
model = None
encoder = None
features = None
model_name = "Random Forest"

@app.get("/")
def read_root():
    return {
        "message": "PM2.5 Prediction API",
        "endpoints": ["/predict", "/docs", "/health"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Get PM2.5 prediction for given parameters"""
    try:
        # Dummy prediction for demo
        base_pm25 = 10.5
        year_effect = (2024 - request.year) * 0.05
        region_effect = {"Northeast": 0.5, "Midwest": 1.0, "South": 0.8, "West": 1.5, "Pacific": 0.3, "Mountain": 0.7}.get(request.region, 0)
        
        predicted_pm25 = base_pm25 - year_effect + region_effect + (request.geographic_mean_pm25 - 12) * 0.3
        predicted_pm25 = max(predicted_pm25, 5)
        
        if predicted_pm25 < 9:
            confidence = "Good"
        elif predicted_pm25 < 12:
            confidence = "Moderate"
        elif predicted_pm25 < 15:
            confidence = "Unhealthy for Sensitive Groups"
        else:
            confidence = "Unhealthy"
        
        return PredictionResponse(
            predicted_pm25=round(predicted_pm25, 2),
            region=request.region,
            year=request.year,
            model_name=model_name,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
