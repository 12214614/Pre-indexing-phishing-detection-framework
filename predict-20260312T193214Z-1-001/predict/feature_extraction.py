import pandas as pd
from tqdm import tqdm
from url_feature_extraction import extract_all_features

# Load dataset
dataset = pd.read_csv("pipdf_frozen_dataset.csv")
dataset = dataset[["url", "label"]]

print(dataset.head())
print(dataset["label"].value_counts())

feature_rows = []
labels = []
failed_urls = []

for idx, row in tqdm(dataset.iterrows(), total=len(dataset)):
    url = row["url"]
    label = row["label"]

    try:
        # Extract features directly
        features = extract_all_features(url)

        if not features:
            raise ValueError("Empty feature dict")

        feature_rows.append(features)
        labels.append(label)

    except Exception as e:
        failed_urls.append((url, str(e)))

# Create feature matrix
X = pd.DataFrame(feature_rows)
y = pd.Series(labels, name="label")

print("\nFeature matrix shape:", X.shape)
print("Label vector shape:", y.shape)

# Handle missing values
print("\nMissing values per feature:")
print(X.isna().sum())

X = X.fillna(0)

# Combine features and label
feature_dataset = pd.concat([X, y], axis=1)
feature_dataset.to_csv("pipdf_feature_dataset.csv", index=False)

print("\nFeature dataset saved as pipdf_feature_dataset.csv")
print(f"Failed URLs: {len(failed_urls)}")

if failed_urls:
    print("Sample failed URL:", failed_urls[0])
