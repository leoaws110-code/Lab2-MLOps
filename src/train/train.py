import os
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def main():
    # تحميل بيانات تجريبية (Iris)
    data = load_iris()
    X, y = data.data, data.target

    # تدريب النموذج
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # حفظ النموذج في مجلد app لتسهيل استخدامه في الـ API
    os.makedirs("src/app", exist_ok=True)
    joblib.dump(model, "src/app/model.joblib")
    print("Model trained and saved successfully as src/app/model.joblib")

if __name__ == "__main__":
    main()