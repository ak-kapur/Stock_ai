import requests

NEWS_API_KEY = "2a81532125a742dcb9fb60a46d6538ea"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def get_news_for_ticker(ticker):
    params = {
        "q": ticker,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [f"{a['title']} - {a['source']['name']}" for a in articles]
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return ["Failed to fetch news."]

# Example usage:
if __name__ == "__main__":
    print(get_news_for_ticker("AAPL"))
