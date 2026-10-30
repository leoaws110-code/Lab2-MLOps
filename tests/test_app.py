import pytest
from fastapi.testclient import TestClient
from src.app.main import app, model

client = TestClient(app)

# 1. اختبار تحميل النموذج (Model loads)
def test_model_loaded():
    assert model is not None, "Model should be loaded successfully"

# 2. اختبار عقد الـ API لنقطة النهاية /health (API contract)[cite: 2]
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True

# 3. اختبار مخطط المدخلات الصحيح ونقطة التنبؤ (Input schema)[cite: 2]
def test_predict_endpoint_valid():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], int)

# 4. اختبار الحالة الحدية (Edge case - إرسال بيانات غير صالحة نوعاً)[cite: 2]
def test_predict_endpoint_edge_case():
    invalid_payload = {
        "sepal_length": "not-a-number",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422  # Pydantic validation error

# 5. اختبار التنبؤ الحتمي (Deterministic prediction)[cite: 2]
def test_deterministic_prediction():
    payload = {
        "sepal_length": 6.7,
        "sepal_width": 3.0,
        "petal_length": 5.2,
        "petal_width": 2.3
    }
    response1 = client.post("/predict", json=payload)
    response2 = client.post("/predict", json=payload)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()