from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Lab2 MLOps API", version="1.0")

# تحميل النموذج المحفوظ
model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
try:
    model = joblib.load(model_path)
except Exception as e:
    model = None

# تعريف نموذج المدخلات باستخدام Pydantic للتحقق من الصحة
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # تجهيز المدخلات للتنبؤ
    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])
    
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}