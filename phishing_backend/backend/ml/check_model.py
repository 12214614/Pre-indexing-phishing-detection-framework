import joblib

# load the model
model = joblib.load("rf_model.pkl")

print("Model loaded successfully!\n")

print("Model type:")
print(type(model))

print("\nModel details:")
print(model)