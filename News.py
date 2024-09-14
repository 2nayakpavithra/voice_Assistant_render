import requests
from dotenv import load_dotenv
import os

# Explicitly specify the path to the .env file
dotenv_path = 'C:/Users/dell/Desktop/Voice_assistant/apid.env'
if not load_dotenv(dotenv_path):
    print("Failed to load environment variables.")


# Fetch API key from the environment variables
News_api_key = os.getenv('News_api_key')
#print(f"News API Key: {News_api_key}")

def fetch_news(api_key, country='us', num_headlines=3):
    api_address = f"https://newsapi.org/v2/top-headlines"
    params = {
        'country': country,
        'apiKey': api_key
    }


    try:
        response = requests.get(api_address, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        json_data = response.json()
        articles = json_data["articles"]

        headlines = []
        for i in range(min(num_headlines, len(articles))):  # Ensure we don't exceed available articles
            headline = f"Number {i + 1}" + ", " + f"{articles[i]['title']}"
            headlines.append(headline)

        return headlines

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None



