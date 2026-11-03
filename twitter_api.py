import tweepy  
import pandas as pd  # ✅ Add this at the top

# API Credentials  
API_KEY = "aTawlNCL0wmmjdb16b34k6bXj"  
API_SECRET = "badohAWQaw1wUzjNnOcyR5UzrlQojbU0qOhmzOOOsv1FDNcfrC"  
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPQg0QEAAAAAyZQVMF21k0a2T7Ng39ynYIB2Agg%3DHPgnKDZIRL8uQzvbu1G9G69DfCrI4lNEC5N6GU3uhcJjK9FNuk"  

# Authenticate with Tweepy  
client = tweepy.Client(bearer_token=BEARER_TOKEN)  

# Fetch user data  
response = client.get_user(username="elonmusk")  
print(response.data)  

# Convert to DataFrame  
df = pd.DataFrame([response.data])  
print(df)
