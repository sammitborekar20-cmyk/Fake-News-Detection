# Fake News Detection System

An NLP-based machine learning project that classifies news articles as **FAKE** or **REAL** using TF-IDF feature extraction and a Passive-Aggressive Classifier.

## Project Overview

The system processes news article titles and text, extracts textual features using TF-IDF, and predicts whether an article is fake or genuine.

The project also includes a FastAPI backend and a Chrome extension for collecting and submitting news content for prediction.

## Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- Natural Language Processing (NLP)
- TF-IDF Vectorization
- Passive-Aggressive Classifier
- FastAPI
- Joblib
- Chrome Extension APIs

## Dataset

The original dataset consisted of:
- Fake news records: 23,481
- Real news records: 21,417
- Total original records: 44,898
- Cleaned records after duplicate and invalid-record removal: 38,313

The cleaned dataset contains:
- REAL: 20,921
- FAKE: 17,392

## Model Performance

### Original evaluation

- Train-test split: 80:20, stratified
- Test records: 7,663
- Test accuracy: **99.60%**
- FAKE precision: 99.71%
- FAKE recall: 99.40%
- FAKE F1-score: 99.55%

### External benchmark evaluation

The existing trained model was evaluated on a separate benchmark test split containing 4,482 articles.

- External benchmark size: 4,482 articles
- Accuracy: **93.11%**
- FAKE precision: 87.59%
- FAKE recall: 99.03%
- FAKE F1-score: 92.96%

The external benchmark result is separate from the original random test split. It should not be interpreted as guaranteed live-news accuracy or fully independent generalization until dataset overlap and source differences are checked.

## Project Structure

```text
PBL/
├── backend/
├── chrome_extension/
├── Dataset/
├── Graphs/
├── Model/
├── Reports/
├── dataset_analysis.py
├── dataset_cleaning.py
├── model_comparison.py
├── model_optimization.py
├── prepare_external_dataset.py
├── evaluate_real_world.py
├── explain_prediction.py
└── README.md
```

## Model Evaluation

The project evaluates the classifier using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

The external evaluation scripts generate a performance summary, individual predictions, misclassified examples, and a confusion matrix.

## Running the Project

Activate the Python virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Prepare the external benchmark CSV:

```bash
python prepare_external_dataset.py
```

Evaluate the existing trained model:

```bash
python evaluate_real_world.py
```

## Future Improvements

- Evaluate on independently collected, verified, recent news articles.
- Investigate false-positive and false-negative predictions.
- Test generalization across different publishers, topics, and time periods.
- Improve robustness against misleading headlines and unfamiliar writing styles.

## Disclaimer

This system provides machine learning-based predictions, not definitive fact-checking. Predictions should be verified against reliable sources before being treated as factual conclusions.
