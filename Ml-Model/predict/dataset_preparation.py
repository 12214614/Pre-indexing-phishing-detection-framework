import pandas as pd
import random
from url_feature_extraction import normalize_url

phish_df = pd.read_csv("Phishing.csv")
legi_df = pd.read_csv("Legitimate.csv")

print("Phishing columns:", phish_df.columns)
print("Legitimate columns:", legi_df.columns)

if "url" not in phish_df.columns:
    raise ValueError("Phishing dataset must contain 'url' column")

if "domain" in legi_df.columns:
    legi_df = legi_df.rename(columns={"domain": "url"})
elif "url" not in legi_df.columns:
    raise ValueError("Legitimate dataset must contain 'domain' or 'url' column")

phish_df = phish_df[phish_df["url"].notna()]
legi_df = legi_df[legi_df["url"].notna()]

phish_df["url"] = phish_df["url"].astype(str)
legi_df["url"] = legi_df["url"].astype(str)

phish_df = phish_df.drop_duplicates(subset="url")
legi_df = legi_df.drop_duplicates(subset="url")

phish_df["url"] = phish_df["url"].apply(normalize_url)
legi_df["url"] = legi_df["url"].apply(normalize_url)
def randomize_scheme(url):
    if random.random() < 0.7:
        return url.replace("http://", "https://")
    return url

legi_df["url"] = legi_df["url"].apply(randomize_scheme)

COMMON_LEGIT_PATHS = [
    "/",
    "/home",
    "/about",
    "/login",
    "/account",
    "/search?q=test",
    "/products",
    "/profile"
]

def add_realistic_path(url: str) -> str:
    if random.random() < 0.6:  
        return url.rstrip("/") + random.choice(COMMON_LEGIT_PATHS)
    return url

legi_df["url"] = legi_df["url"].apply(add_realistic_path)

N = min(len(phish_df), len(legi_df), 500)

phish_df = phish_df.sample(n=N, random_state=42)
legi_df = legi_df.sample(n=N, random_state=42)

phish_df["label"] = 1   # phishing
legi_df["label"] = 0   # legitimate

dataset = pd.concat([phish_df, legi_df], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

dataset.to_csv("pipdf_frozen_dataset.csv", index=False)

print("Dataset frozen successfully!")
print(dataset.head())
print(dataset["label"].value_counts())


