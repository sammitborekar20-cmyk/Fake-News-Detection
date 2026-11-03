import praw
import requests

# Reddit API Credentials (Replace with your credentials)
REDDIT_CLIENT_ID = "NTEo4ksbqSBcyJZu5epupg"
REDDIT_CLIENT_SECRET = "QzbIdyPFcA6zN0DNojWC2Xj4333Lmw"
REDDIT_USER_AGENT = "pbl"

# FastAPI URL (Running locally on port 8000)
API_URL = "http://127.0.0.1:8000/predict/"

# Initialize PRAW (Reddit API)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Function to scrape Reddit and classify news
def scrape_and_predict(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.hot(limit=limit):  # Fetch top posts
        news_text = post.title  # Extract post title as the text to analyze
        print(f"News Title: {news_text}")

        # Send request to FastAPI for prediction
        response = requests.post(API_URL, json={"text": news_text})

        if response.status_code == 200:
            prediction = response.json()["prediction"]
            print(f"Prediction: {prediction}\n")
        else:
            print("Error: Could not get prediction\n")

# Example Usage
scrape_and_predict("worldnews", limit=5)  # Scrapes 5 posts from r/worldnews
