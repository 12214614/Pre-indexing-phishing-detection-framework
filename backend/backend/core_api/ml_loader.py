import glob
import os
import joblib
import pandas as pd
from django.conf import settings


def _find_predict_dir() -> str:
    """
    Locate predict folder in workspace, e.g.:
    pippf-project-updated/predict-20260312T193214Z-1-001/predict
    """
    workspace_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    candidates = glob.glob(os.path.join(workspace_root, "predict-*", "predict"))
    if not candidates:
        return ""
    # pick most recently modified folder
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]


def _load_model_assets():
    """
    Primary source: predict-*/predict/<name>_model.pkl + <name>_threshold.pkl
    Fallback source: backend/ml/rf_model.pkl + rf_threshold.pkl
    """
    requested_model = os.getenv("PIPPF_MODEL", "rf").strip().lower()
    if requested_model not in {"rf", "svm", "ann"}:
        requested_model = "rf"

    predict_dir = _find_predict_dir()
    if predict_dir:
        model_path = os.path.join(predict_dir, f"{requested_model}_model.pkl")
        threshold_path = os.path.join(predict_dir, f"{requested_model}_threshold.pkl")
        if os.path.exists(model_path) and os.path.exists(threshold_path):
            loaded_model = joblib.load(model_path)
            loaded_threshold = float(joblib.load(threshold_path))
            return loaded_model, loaded_threshold, requested_model, predict_dir

    # Fallback to old backend/ml path
    fallback_dir = os.path.join(settings.BASE_DIR, "ml")
    model_path = os.path.join(fallback_dir, "rf_model.pkl")
    threshold_path = os.path.join(fallback_dir, "rf_threshold.pkl")
    loaded_model = joblib.load(model_path)
    loaded_threshold = float(joblib.load(threshold_path))
    return loaded_model, loaded_threshold, "rf", fallback_dir


# Load model and threshold once when server starts
model, threshold, model_name, model_source_dir = _load_model_assets()

# Exact feature order the model was trained on
FEATURE_COLUMNS = (
    list(model.feature_names_in_)
    if hasattr(model, "feature_names_in_")
    else [
        'url_length', 'domain_length', 'path_length', 'path_depth',
        'digit_ratio', 'special_char_ratio', 'dot_count', 'hyphen_count',
        'subdomain_count', 'has_ip_address', 'has_https',
        'url_entropy', 'domain_entropy', 'token_count', 'max_token_length',
        'suspicious_token_ratio', 'has_query_params', 'query_param_count',
        'document_path_present', 'long_digit_sequence', 'path_numeric_ratio',
        'semantic_subdomain_depth', 'has_deep_subdomain',
        'brand_in_registered_domain', 'brand_in_subdomain', 'brand_mismatch',
        'dns_query_success', 'a_record_count', 'domain_age_days',
        'has_form', 'password_input_present', 'external_form_action',
    ]
)


def predict_url(features_dict):
    """
    Takes extracted feature dictionary, returns prediction result.
    Uses custom threshold from rf_threshold.pkl.
    """
    # Build DataFrame with exact column order the model expects
    row = {col: features_dict.get(col, 0) for col in FEATURE_COLUMNS}
    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # Get probability of phishing (class 1)
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(df)[0][1])
    else:
        probability = 0.5

    # Apply custom threshold
    prediction = 1 if probability >= threshold else 0

    return {
        "prediction": prediction,
        "probability": probability,
        "model_name": model_name,
        "threshold": threshold,
        "model_source_dir": model_source_dir,
    }
