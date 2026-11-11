
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    StratifiedKFold
)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import (
    LogisticRegression,
    PassiveAggressiveClassifier
)

from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# -----------------------------------
# 1. Load cleaned dataset
# -----------------------------------

df = pd.read_csv("Dataset/cleaned_news.csv")

df["title"] = df["title"].fillna("")
df["text"] = df["text"].fillna("")

df["content"] = df["title"] + " " + df["text"]

X = df["content"]
y = df["label"]

# -----------------------------------
# 2. Train-test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# -----------------------------------
# 3. Create pipeline
# -----------------------------------

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LinearSVC())
])

# -----------------------------------
# 4. Define search configurations
# -----------------------------------

tfidf_parameters = {
"tfidf__max_features": [20000, 30000],
"tfidf__ngram_range": [(1, 1), (1, 2)],
"tfidf__min_df": [2, 3],
"tfidf__max_df": [0.95],
"tfidf__sublinear_tf": [True],
"tfidf__stop_words": ["english"]
}

parameter_grid = [
    {
        **tfidf_parameters,
        "classifier": [
            PassiveAggressiveClassifier(
                random_state=42,
                max_iter=2000,
                tol=1e-3
            )
        ],
        "classifier__C": [0.05, 0.1, 0.5, 1.0, 2.0]
    },
    {
        **tfidf_parameters,
        "classifier": [LinearSVC(max_iter=5000)],
        "classifier__C": [0.1, 0.5, 1.0, 2.0]
    },
    {
        **tfidf_parameters,
        "classifier": [
            LogisticRegression(
                max_iter=3000,
                random_state=42
            )
        ],
        "classifier__C": [0.1, 0.5, 1.0, 2.0]
    },
    {
        **tfidf_parameters,
        "classifier": [MultinomialNB()],
        "classifier__alpha": [0.05, 0.1, 0.5, 1.0]
    }
]

# -----------------------------------
# 5. Cross-validation
# -----------------------------------

cv = StratifiedKFold(
    n_splits=3,
    shuffle=True,
    random_state=42
)

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=parameter_grid,
    n_iter=12,
    scoring="accuracy",
    cv=cv,
    random_state=42,
    n_jobs=-2,
    verbose=2,
    return_train_score=False
)

# -----------------------------------
# 6. Optimize model
# -----------------------------------

print("\nSTARTING MODEL OPTIMIZATION...\n")

search.fit(X_train, y_train)

best_model = search.best_estimator_

# -----------------------------------
# 7. Evaluate best model
# -----------------------------------

y_pred = best_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test, y_pred, pos_label="FAKE"
)

recall = recall_score(
    y_test, y_pred, pos_label="FAKE"
)

f1 = f1_score(
    y_test, y_pred, pos_label="FAKE"
)

print("\n========== OPTIMIZED MODEL ==========")

print(best_model.named_steps["classifier"])

print("\nBEST PARAMETERS:")
print(search.best_params_)

print("\nBEST CROSS-VALIDATION ACCURACY:")
print(f"{search.best_score_ * 100:.2f}%")

print("\n========== TEST PERFORMANCE ==========")

print(f"Testing Accuracy: {accuracy * 100:.2f}%")
print(f"FAKE Precision: {precision * 100:.2f}%")
print(f"FAKE Recall: {recall * 100:.2f}%")
print(f"FAKE F1 Score: {f1 * 100:.2f}%")

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, y_pred))

print("\nCONFUSION MATRIX")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["FAKE", "REAL"]
))

# -----------------------------------
# 8. Save experimental model
# -----------------------------------

os.makedirs("Model", exist_ok=True)
os.makedirs("Reports", exist_ok=True)

# Save separately to preserve existing model
joblib.dump(
    best_model,
    "Model/optimized_fake_news_model.pkl"
)

# -----------------------------------
# 9. Save all experiment results
# -----------------------------------

results = pd.DataFrame(search.cv_results_)

results = results.sort_values(
    by="rank_test_score"
)

results.to_csv(
    "Reports/optimization_experiments.csv",
    index=False
)

summary = pd.DataFrame([{
    "Model": type(
        best_model.named_steps["classifier"]
    ).__name__,
    "Testing Accuracy": accuracy,
    "Precision FAKE": precision,
    "Recall FAKE": recall,
    "F1 FAKE": f1,
    "CV Accuracy": search.best_score_
}])

summary.to_csv(
    "Reports/optimized_model_results.csv",
    index=False
)

print("\nOptimized model saved separately.")
print("Experiment results saved in Reports/")
print("\nMODEL OPTIMIZATION COMPLETED!")
