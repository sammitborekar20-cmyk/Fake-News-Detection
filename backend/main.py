from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

model = joblib.load("Model/news_classifier.pkl")
vectorizer = joblib.load("Model/tfidf_vectorizer.pkl")

class News(BaseModel):
    text: str

@app.post("/predict")
def predict_news(news: News):
    cleaned = news.text.lower()
    transformed = vectorizer.transform([cleaned])
    prediction = model.predict(transformed)[0]
    return {"prediction": prediction}

@app.get("/")
def read_root():
    return {"message": "Fake News Detection API is running!"}



