import joblib
import pandas as pd
from url_feature_extraction import extract_all_features

MODEL_PATH = "svm_model.pkl"
THRESHOLD_PATH = "svm_threshold.pkl"

model = joblib.load(MODEL_PATH)
threshold = joblib.load(THRESHOLD_PATH)


def stage1_decision(url: str) -> dict:
    try:
        features = extract_all_features(url)
        X = pd.DataFrame([features]).fillna(0)

        prob = float(model.predict_proba(X)[0][1])
        decision = 1 if prob >= threshold else 0

        return {
            "stage": 1,
            "url": url,
            "decision": decision,
            "probability": round(prob, 4),
            "label": "PHISHING" if decision == 1 else "LEGITIMATE"
        }

    except Exception as e:
        return {
            "stage": 1,
            "url": url,
            "error": str(e)
        }


if __name__ == "__main__":
    print(f"[Stage-1] Loaded model: {MODEL_PATH}")
    print(f"[Stage-1] Using threshold: {threshold:.4f}")