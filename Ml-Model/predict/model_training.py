import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV

df = pd.read_csv("pipdf_feature_dataset.csv")

X = df.drop(columns=["label"])
y = df["label"]

print("Dataset shape:", X.shape)
print("Class distribution:\n", y.value_counts())

feature_columns = X.columns.tolist()
joblib.dump({
    "ENABLE_DNS": True,
    "ENABLE_WHOIS": True,
    "ENABLE_HTML": True
}, "feature_config.pkl")

# 2. TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

# THRESHOLD OPTIMIZATION

def find_best_threshold(y_true, y_prob):
    thresholds = np.linspace(0.1, 0.9, 81)
    best_t, best_f1 = 0.5, 0

    for t in thresholds:
        y_pred = (y_prob >= t).astype(int)
        report = classification_report(y_true, y_pred, output_dict=True)
        f1 = report["1"]["f1-score"]
        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    return best_t


def evaluate_model(name, y_true, y_prob):
    best_t = find_best_threshold(y_true, y_prob)
    y_pred = (y_prob >= best_t).astype(int)

    print(f"\n===== {name} =====")
    print(f"Best Threshold: {best_t:.2f}")
    print(classification_report(y_true, y_pred, digits=4))

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    print("Confusion Matrix:")
    print(cm)
    print("ROC-AUC:", roc_auc_score(y_true, y_prob))
    print(f"False Positive Rate (FPR): {fp / (fp + tn):.4f}")
    print(f"False Negative Rate (FNR): {fn / (fn + tp):.4f}")

    return best_t

# RANDOM FOREST

rf_base = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=5,
    max_features="sqrt",
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model = CalibratedClassifierCV(
    rf_base,
    method="isotonic",
    cv=3
)

rf_model.fit(X_train, y_train)

rf_prob = rf_model.predict_proba(X_test)[:, 1]
rf_threshold = evaluate_model("Random Forest", y_test, rf_prob)

joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(rf_threshold, "rf_threshold.pkl")
print("Saved: rf_model.pkl, rf_threshold.pkl")

# SVM

svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        class_weight="balanced",
        probability=True,
        random_state=42
    ))
])

svm_model = CalibratedClassifierCV(
    svm_pipeline,
    method="sigmoid",
    cv=3
)

svm_model.fit(X_train, y_train)

svm_prob = svm_model.predict_proba(X_test)[:, 1]
svm_threshold = evaluate_model("SVM", y_test, svm_prob)

joblib.dump(svm_model, "svm_model.pkl")
joblib.dump(svm_threshold, "svm_threshold.pkl")
print("Saved: svm_model.pkl, svm_threshold.pkl")

# ANN (MLP)

ann_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("ann", MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        alpha=0.0005,
        max_iter=600,
        early_stopping=True,
        random_state=42
    ))
])

ann_model = CalibratedClassifierCV(
    ann_pipeline,
    method="sigmoid",
    cv=3
)

ann_model.fit(X_train, y_train)

ann_prob = ann_model.predict_proba(X_test)[:, 1]
ann_threshold = evaluate_model("ANN", y_test, ann_prob)

joblib.dump(ann_model, "ann_model.pkl")
joblib.dump(ann_threshold, "ann_threshold.pkl")
print("Saved: ann_model.pkl, ann_threshold.pkl")

print("\n✅ ALL MODELS TRAINED, CALIBRATED, AND SAVED SUCCESSFULLY")
