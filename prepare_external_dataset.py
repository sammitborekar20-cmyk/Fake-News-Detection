
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_PATH = (
    BASE_DIR / "datasets" / "processed" / "unified_test.tsv"
)

OUTPUT_PATH = (
    BASE_DIR / "Dataset" / "real_world_test.csv"
)

# Read the independent test split
df = pd.read_csv(INPUT_PATH, sep="\t")

# Convert labels:
# 0 = FAKE
# 1 = REAL

df["label"] = df["label"].map({
    0: "FAKE",
    1: "REAL"
})

# Match your existing evaluation script's format
result = pd.DataFrame({
    "title": "",
    "text": df["text"],
    "label": df["label"],
    "source": "Unified benchmark dataset",
    "date": ""
})

result.to_csv(OUTPUT_PATH, index=False)

print("External test dataset created!")
print("Total articles:", len(result))
print("\nLabel distribution:")
print(result["label"].value_counts())
print("\nSaved to:", OUTPUT_PATH)
