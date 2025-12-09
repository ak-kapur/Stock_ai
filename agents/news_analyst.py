from groq_client import chat_with_groq

def analyze_news(news_list):
    prompt = [
        {"role": "system", "content": "Analyze the sentiment and insights from financial news."},
        {"role": "user", "content": "\n".join(news_list)}
    ]
    return chat_with_groq(prompt)
