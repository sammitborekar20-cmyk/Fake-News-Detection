
import pandas as pd
import joblib
import os

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "Dataset" / "real_world_test.csv"

MODEL_PATH = BASE_DIR / "Model" / "best_fake_news_model.pkl"

REPORT_DIR = BASE_DIR / "Reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOAD THE EXISTING MODEL
# --------------------------------------------------

print("\nLoading existing Fake News Detection model...")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")


# --------------------------------------------------
# 3. LOAD INDEPENDENT TEST DATASET
# --------------------------------------------------

print("\nLoading independent test dataset...")

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

df = pd.read_csv(DATASET_PATH)

required_columns = ["title", "text", "label"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Missing required column: {column}"
        )

print("Dataset loaded successfully!")

print("Total articles:", len(df))


# --------------------------------------------------
# 4. CLEAN AND VALIDATE DATA
# --------------------------------------------------

df["title"] = df["title"].fillna("").astype(str)
df["text"] = df["text"].fillna("").astype(str)

df["label"] = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Keep only valid labels
df = df[df["label"].isin(["FAKE", "REAL"])].copy()

# Remove empty articles
df = df[
    (df["title"].str.strip() != "") |
    (df["text"].str.strip() != "")
].copy()

# Remove duplicate articles
df["combined_text"] = (
    df["title"] + " " + df["text"]
).str.strip()

df = df.drop_duplicates(
    subset=["combined_text"]
).reset_index(drop=True)

if df.empty:
    raise ValueError(
        "No valid articles found in the dataset."
    )

if df["label"].nunique() != 2:
    raise ValueError(
        "The test dataset must contain both FAKE and REAL articles."
    )

print("\nDataset after validation:")
print("Total articles:", len(df))

print("\nLabel distribution:")
print(df["label"].value_counts())


# --------------------------------------------------
# 5. PREPARE INPUT DATA
# --------------------------------------------------

# Same input format as the original training script:
# title + text

X_test = df["combined_text"]

y_test = df["label"]


# --------------------------------------------------
# 6. GENERATE PREDICTIONS
# --------------------------------------------------

print("\nEvaluating model on independent articles...")

predictions = model.predict(X_test)

# Normalize predicted labels
predictions = [
    str(prediction).strip().upper()
    for prediction in predictions
]

print("Predictions completed!")


# --------------------------------------------------
# 7. CALCULATE PERFORMANCE METRICS
# --------------------------------------------------

accuracy = accuracy_score(
    y_test, predictions
)

precision = precision_score(
    y_test,
    predictions,
    pos_label="FAKE",
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    pos_label="FAKE",
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    pos_label="FAKE",
    zero_division=0
)


# --------------------------------------------------
# 8. DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 50)
print("       REAL-WORLD MODEL EVALUATION")
print("=" * 50)

print(f"Total Articles : {len(df)}")

print(f"Accuracy       : {accuracy * 100:.2f}%")

print(f"FAKE Precision : {precision * 100:.2f}%")

print(f"FAKE Recall    : {recall * 100:.2f}%")

print(f"FAKE F1-Score  : {f1 * 100:.2f}%")

print("=" * 50)


# --------------------------------------------------
# 9. CLASSIFICATION REPORT
# --------------------------------------------------

print("\nDetailed Classification Report:\n")

report = classification_report(
    y_test,
    predictions,
    labels=["FAKE", "REAL"],
    target_names=["FAKE", "REAL"],
    zero_division=0
)

print(report)


# --------------------------------------------------
# 10. CONFUSION MATRIX
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    predictions,
    labels=["FAKE", "REAL"]
)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["FAKE", "REAL"],
    yticklabels=["FAKE", "REAL"]
)

plt.title("Real-World Fake News Detection")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

plt.tight_layout()

confusion_path = REPORT_DIR / "real_world_confusion_matrix.png"

plt.savefig(confusion_path, dpi=300)

plt.close()


# --------------------------------------------------
# 11. SAVE INDIVIDUAL PREDICTIONS
# --------------------------------------------------

df["predicted_label"] = predictions

df["correct_prediction"] = (
    df["label"] == df["predicted_label"]
)

prediction_path = REPORT_DIR / "real_world_predictions.csv"

df.to_csv(prediction_path, index=False)


# --------------------------------------------------
# 12. SAVE INCORRECT PREDICTIONS
# --------------------------------------------------

incorrect_df = df[
    df["correct_prediction"] == False
].copy()

incorrect_path = REPORT_DIR / "real_world_misclassified.csv"

incorrect_df.to_csv(
    incorrect_path,
    index=False
)


# --------------------------------------------------
# 13. SAVE EVALUATION SUMMARY
# --------------------------------------------------

summary = pd.DataFrame([{
    "Total Articles": len(df),
    "Accuracy": round(accuracy * 100, 2),
    "FAKE Precision": round(precision * 100, 2),
    "FAKE Recall": round(recall * 100, 2),
    "FAKE F1 Score": round(f1 * 100, 2),
    "Correct Predictions": int(
        df["correct_prediction"].sum()
    ),
    "Incorrect Predictions": len(incorrect_df)
}])

summary_path = REPORT_DIR / "real_world_evaluation.csv"

summary.to_csv(summary_path, index=False)


# --------------------------------------------------
# 14. FINAL OUTPUT
# --------------------------------------------------

print("\nEvaluation completed successfully!")

print("\nFiles saved:")

print("1.", summary_path)

print("2.", prediction_path)

print("3.", incorrect_path)

print("4.", confusion_path)

print("\nIncorrectly classified articles:", len(incorrect_df))

print("\n" + "=" * 50)
