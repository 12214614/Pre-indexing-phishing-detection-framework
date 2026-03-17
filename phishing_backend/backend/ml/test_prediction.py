import joblib

model = joblib.load("rf_model.pkl")

# give 32 features
sample_features = [[0]*32]

prediction = model.predict(sample_features)

print("Prediction:", prediction)