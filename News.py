import requests
from config import News_api_key

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



